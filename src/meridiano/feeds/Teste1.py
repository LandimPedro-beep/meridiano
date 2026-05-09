BLOCK_ID = "vetor"
BLOCK_NAME = "Vetor"
BLOCK_DESCRIPTION = (
    "Bloco semanal de novidades altamente relevantes para a linha de pesquisa do usuario. "
    "Este bloco deve privilegiar artigos cientificos publicados nos ultimos 7 dias."
)
EDITORIAL_CADENCE = "weekly"
PUBLICATION_WINDOW_DAYS = 7
TARGET_WEEKLY_ARTICLE_COUNT = 10

RSS_FEEDS = [
    "http://feeds.nature.com/ncb/rss/current",  # Nature Cell Biology
    "http://feeds.nature.com/nchem/rss/current",  # Nature Chemistry
]

FEED_KEYWORDS = [
    "bioquimica",
    "biologia molecular",
    "biotecnologia",
    "enzimas",
    "proteinas",
    "genetica",
    "genomica",
    "metabolismo",
    "sinalizacao celular",
    "metodos experimentais",
]

PROMPT_ARTICLE_KEYWORD_LABELING = """
Analise rapidamente este artigo cientifico e retorne apenas JSON valido.

Palavras-chave prioritarias deste bloco:
{feed_keywords_text}

Contexto do bloco:
- O bloco Vetor reune novidades altamente relevantes para a linha de pesquisa do usuario.
- Priorize artigos cientificos atuais e alinhados ao nucleo tematico do feed.
- Defina "matched" como true somente se o artigo for claramente relevante para esta linha de pesquisa.

Formato obrigatorio:
{{"labels":["rotulo 1","rotulo 2"],"matched":true}}

Titulo:
{article_title}

Artigo:
{article_content}

Responda em portugues brasileiro.
"""

PROMPT_ARTICLE_SUMMARY = """
Resuma os pontos-chave deste artigo cientifico em 3 a 5 frases objetivas.
Se atenha ao conteudo do artigo, sem extrapolar e sem adicionar informacoes externas.
Priorize descoberta principal, metodo, sistema estudado e relevancia cientifica imediata.
Inclua apenas o resumo final, em portugues brasileiro.

Artigo:
{article_content}
"""

PROMPT_IMPACT_RATING = """
Analise o resumo do artigo e estime sua relevancia cientifica para o bloco Vetor.

Considere:
- alinhamento com a linha de pesquisa do feed
- novidade do resultado
- potencial de abrir novas frentes experimentais
- relevancia metodologica
- interesse imediato para pesquisadores da area

Use uma escala de 1 a 10:
1-2: relevancia muito baixa para a linha de pesquisa.
3-4: relevancia limitada ou muito periferica.
5-6: relevancia boa, mas sem sinal claro de destaque excepcional.
7-8: alta relevancia tematica e novidade cientifica consistente.
9-10: artigo raro, extremamente relevante e potencialmente definidor de tendencia.

Resumo:
"{summary}"

Retorne SOMENTE o numero inteiro de 1 a 10.
"""

PROMPT_CLUSTER_ANALYSIS = """
Estes sao resumos de artigos cientificos potencialmente relacionados do bloco semanal '{feed_profile}'.

{cluster_summaries_text}

Identifique o tema cientifico central do grupo.
Resuma os principais avancos, tecnicas, sistemas biologicos ou quimicos envolvidos e a relevancia do conjunto em 3 a 5 frases.
Se os artigos nao forem realmente relacionados, deixe isso claro.

Responda em portugues brasileiro.
"""

PROMPT_BRIEF_SYNTHESIS = """
Voce esta escrevendo a sintese semanal do bloco Vetor em Markdown.
Este bloco representa as novidades mais relevantes para a linha de pesquisa do usuario.

Com base apenas nos grupos analisados:
- comece pelos 3 a 5 eixos cientificos mais importantes da semana
- depois apresente topicos curtos com os principais artigos ou tendencias
- encerre com uma sintese sobre o que mudou na fronteira da area

Mantenha tom tecnico, claro e objetivo.
Nao especule e nao invente informacoes.

Grupos analisados:
{cluster_analyses_text}
"""
