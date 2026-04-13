# query_expander.py
import os
import json

# Domínios técnicos com vocabulário especializado que o modelo deve conhecer
DOMAIN_HINTS = {
    "eletromagnético": "EMI EMC EIRP radiated emissions field strength spectrum RF antenna",
    "electromagnetic": "EMI EMC EIRP radiated emissions field strength spectrum RF antenna",
    "emiss": "radiated conducted emissions spectrum monitoring EIRP antenna power density",
    "espectro": "spectrum frequency allocation RF monitoring ITU FCC ANATEL band",
    "spectrum": "spectrum frequency allocation RF monitoring ITU FCC ANATEL band",
    "rf": "radio frequency spectrum emissions EIRP antenna propagation path loss",
    "radar": "radar cross section RCS SAR synthetic aperture clutter detection",
    "antena": "antenna gain radiation pattern directivity beamwidth VSWR",
    "água": "water quality pH turbidity dissolved oxygen conductivity",
    "water": "water quality pH turbidity dissolved oxygen conductivity",
    "clima": "weather temperature precipitation wind humidity INMET NOAA",
    "climate": "weather temperature precipitation wind humidity NOAA ERA5",
    "saúde": "epidemiology mortality morbidity DATASUS SIM SINAN",
    "health": "epidemiology mortality morbidity WHO CDC incidence prevalence",
}


def _detectar_dicas(keywords: list[str]) -> str:
    """Retorna dicas de vocabulário do domínio com base nas keywords."""
    kws_lower = " ".join(keywords).lower()
    hints = []
    for trigger, vocab in DOMAIN_HINTS.items():
        if trigger in kws_lower:
            hints.append(vocab)
    return " | ".join(hints) if hints else ""


def expandir_query(keywords: list[str], intencao: str = "") -> list[str]:
    """
    Uses Groq to generate search query variants from keywords and user intent.
    Returns a list of query strings optimized for different sources.
    Falls back to returning the original keywords joined if Groq is unavailable.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return [" ".join(keywords)]

    dicas = _detectar_dicas(keywords)
    dicas_bloco = (
        f"\nVocabulário técnico do domínio (use estes termos nas variantes): {dicas}"
        if dicas else ""
    )

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        kws_str = ", ".join(keywords)
        contexto = f"Intenção do usuário: {intencao}\n" if intencao else ""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": (
                    f"{contexto}"
                    f"Gere 6 variantes de busca para encontrar datasets sobre: {kws_str}\n"
                    f"{dicas_bloco}\n\n"
                    "Regras:\n"
                    "- Inclua termos técnicos precisos em inglês (siglas, normas, grandezas físicas)\n"
                    "- Inclua pelo menos 1 variante em português\n"
                    "- Inclua 1 variante focada em fontes regulatórias (FCC, ANATEL, ITU, IEEE)\n"
                    "- Inclua 1 variante com sufixo 'dataset' ou 'open data'\n"
                    "- Cada variante deve ter 2-6 palavras\n"
                    "- Responda APENAS um array JSON de strings, sem explicação\n"
                    'Exemplo EMC: ["radiated emissions dataset", "EMI field strength monitoring", '
                    '"FCC spectrum database", "emissoes eletromagneticas dados abertos", '
                    '"EMC compliance test data", "RF interference open dataset"]'
                )
            }],
        )
        content = response.choices[0].message.content.strip()
        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            variantes = json.loads(content[start:end])
            base = " ".join(keywords)
            if base not in variantes:
                variantes.insert(0, base)
            return variantes[:7]

    except Exception as e:
        print(f"[query_expander] Erro: {e}")

    return [" ".join(keywords)]
