BLOCK_ID = "matriz"
BLOCK_NAME = "Matriz"
BLOCK_DESCRIPTION = (
    "Bloco semanal de artigos maduros, canonicos e academicamente consolidados. "
    "Este bloco deve privilegiar artigos cientificos publicados entre 10 e 15 anos atras "
    "e com forte relevancia para a area de interesse do usuario."
)
EDITORIAL_CADENCE = "weekly"
PUBLICATION_MIN_AGE_YEARS = 10
PUBLICATION_MAX_AGE_YEARS = 15
TARGET_WEEKLY_ARTICLE_COUNT = 10

RSS_FEEDS = [
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=chreay",  # Chemical Reviews
    "http://feeds.nature.com/nrc/rss/current",  # Nature Reviews Cancer
    "http://feeds.nature.com/nrdp/rss/current",  # Nature Reviews Disease Primers
    "http://feeds.nature.com/nrg/rss/current",  # Nature Reviews Genetics
    "http://feeds.nature.com/nrmicro/rss/current",  # Nature Reviews Microbiology
    "http://feeds.nature.com/nrm/rss/current",  # Nature Reviews Molecular Cell Biology
    "http://iopscience.iop.org/0036-021X/?rss=1",  # Russian Chemical Reviews
]

FEED_KEYWORDS = [
    "bioquimica",
    "biologia molecular",
    "quimica biologica",
    "genetica",
    "genomica",
    "sinalizacao celular",
    "metabolismo",
    "estrutura de proteinas",
    "metodos fundamentais",
    "artigo de revisao",
]

PROMPT_ARTICLE_KEYWORD_LABELING = """
Analise rapidamente este artigo cientifico e retorne apenas JSON valido.

Palavras-chave prioritarias deste bloco:
{feed_keywords_text}

Contexto do bloco:
- O bloco Matriz reune artigos maduros e academicamente incontornaveis.
- Priorize artigos de revisao, sinteses conceituais, marcos metodologicos e trabalhos de referencia.
- Defina "matched" como true somente se o artigo for central para a area e fizer sentido como leitura de dominio.

Formato obrigatorio:
{{"labels":["rotulo 1","rotulo 2"],"matched":true}}

Titulo:
{article_title}

Artigo:
{article_content}

Responda em portugues brasileiro.
"""

PROMPT_ARTICLE_SUMMARY = """
Resuma este artigo cientifico em 3 a 5 frases, com foco em sua contribuicao conceitual e durabilidade academica.
Se atenha ao conteudo do artigo e nao adicione informacoes externas.
Priorize ideia central, sintese do campo, marco metodologico ou consolidacao teorica.
Inclua apenas o resumo final, em portugues brasileiro.

Artigo:
{article_content}
"""

PROMPT_IMPACT_RATING = """
Analise o resumo do artigo e estime sua relevancia para o bloco Matriz.

Considere:
- potencial de ser referencia obrigatoria da area
- valor de consolidacao conceitual
- importancia metodologica
- abrangencia do impacto academico
- utilidade para formacao solida do pesquisador

Use uma escala de 1 a 10:
1-2: relevancia baixa ou muito periferica.
3-4: artigo util, mas nao essencial.
5-6: artigo importante, porem nao claramente canonico.
7-8: artigo forte, com papel consolidado na area.
9-10: artigo de referencia, leitura obrigatoria ou marco intelectual evidente.

Resumo:
"{summary}"

Retorne SOMENTE o numero inteiro de 1 a 10.
"""

PROMPT_CLUSTER_ANALYSIS = """
Estes sao resumos de artigos cientificos potencialmente relacionados do bloco semanal '{feed_profile}'.

{cluster_summaries_text}

Identifique qual eixo conceitual, metodologico ou de revisao organiza o grupo.
Resuma em 3 a 5 frases por que esse conjunto e estrutural para a formacao e atualizacao do pesquisador.
Se os artigos nao forem realmente relacionados, diga isso claramente.

Responda em portugues brasileiro.
"""

PROMPT_BRIEF_SYNTHESIS = """
Voce esta escrevendo a sintese semanal do bloco Matriz em Markdown.
Este bloco representa artigos maduros, de dominio obrigatorio, para a area do usuario.

Com base apenas nos grupos analisados:
- apresente os principais eixos conceituais e metodologicos selecionados na semana
- destaque quais leituras parecem mais formativas ou estruturais
- feche com uma sintese do que o pesquisador precisa dominar ou revisitar

Mantenha tom tecnico, objetivo e editorial.
Nao especule e nao invente informacoes.

Grupos analisados:
{cluster_analyses_text}
"""
