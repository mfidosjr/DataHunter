# query_expander.py
import os
import json


def expandir_query(keywords: list[str], intencao: str = "") -> list[str]:
    """
    Uses Groq to generate search query variants from keywords and user intent.
    Returns a list of query strings optimized for different sources.
    Falls back to returning the original keywords joined if Groq is unavailable.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return [" ".join(keywords)]

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        kws_str = ", ".join(keywords)
        contexto = f"Intenção do usuário: {intencao}\n" if intencao else ""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    f"{contexto}"
                    f"Gere 5 variantes de busca para encontrar datasets sobre: {kws_str}\n\n"
                    "Regras:\n"
                    "- Inclua termos técnicos em inglês\n"
                    "- Inclua pelo menos 1 variante em português\n"
                    "- Inclua sinônimos do domínio\n"
                    "- Cada variante deve ser uma string de busca curta (2-5 palavras)\n"
                    "- Responda APENAS um array JSON de strings, sem explicação\n"
                    "Exemplo: [\"water quality dataset\", \"pH turbidity monitoring\", \"qualidade agua dados\"]"
                )
            }],
        )
        content = response.choices[0].message.content.strip()
        # Extrai o JSON mesmo que venha com texto ao redor
        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            variantes = json.loads(content[start:end])
            # Garante que as keywords originais estão incluídas
            base = " ".join(keywords)
            if base not in variantes:
                variantes.insert(0, base)
            return variantes[:6]

    except Exception as e:
        print(f"[query_expander] Erro: {e}")

    return [" ".join(keywords)]
