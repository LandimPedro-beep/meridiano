BLOCK_ID = "horizonte"
BLOCK_NAME = "Horizonte"
BLOCK_DESCRIPTION = (
    "Bloco semanal de panorama cientifico amplo. "
    "Este bloco deve privilegiar artigos cientificos publicados nos ultimos 7 dias "
    "com relevancia global nas diversas areas da quimica e fronteiras relacionadas."
)
EDITORIAL_CADENCE = "weekly"
PUBLICATION_WINDOW_DAYS = 7
TARGET_WEEKLY_ARTICLE_COUNT = 15

RSS_FEEDS = [
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aaembp",  # ACS Applied Materials & Interfaces
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aaemcq",  # ACS Applied Energy Materials
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aanmf6",  # ACS Applied Nano Materials
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=accacs",  # ACS Catalysis
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=acncdm",  # ACS Chemical Neuroscience
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aesccq",  # ACS Earth and Space Chemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aeclc7",  # ACS Electrochemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aidcbc",  # ACS Infectious Diseases
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=cmatex",  # Chemistry of Materials
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aoiab5",  # ACS Organic & Inorganic Au
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=ancham",  # Analytical Chemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=asbcd6",  # ACS Synthetic Biology
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=crtoec",  # Chemical Research in Toxicology
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=inocaj",  # Inorganic Chemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=jacsat",  # JACS
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=jctcce",  # Journal of Chemical Theory and Computation
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=jcisd8",  # Journal of Chemical Information and Modeling
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=jmcmar",  # Journal of Medicinal Chemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=joceah",  # Journal of Organic Chemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=jpcafh",  # Journal of Physical Chemistry A
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=orgnd7",  # Organometallics
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=pstoco",  # Macromolecules / polymers feed family
    "http://feeds.nature.com/nbt/rss/current",  # Nature Biotechnology
    "http://feeds.nature.com/nm/rss/current",  # Nature Materials
    "http://feeds.nature.com/bjc/rss/current",  # British Journal of Cancer
    "http://feeds.nature.com/celldisc/rss/current",  # Cell Discovery
    "http://feeds.nature.com/srep/rss/current",  # Scientific Reports
    "http://science.sciencemag.org/rss/current.xml",  # Science
    "http://bmccancer.biomedcentral.com/articles/most-recent/rss.xml",  # BMC Cancer
    "http://bmccellbiol.biomedcentral.com/articles/most-recent/rss.xml",  # BMC Cell Biology
    "http://bmcgenet.biomedcentral.com/articles/most-recent/rss.xml",  # BMC Genetics
    "http://journal.frontiersin.org/journal/chemistry/rss",  # Frontiers in Chemistry
    "http://iopscience.iop.org/1674-0068/?rss=1",  # Chinese Journal of Chemical Physics
    "http://rss.sciencedirect.com/publication/science/18785352",  # Arabian Journal of Chemistry
    "http://rss.sciencedirect.com/publication/science/00039861",  # Archives of Biochemistry and Biophysics
    "http://rss.sciencedirect.com/publication/science/10018417",  # Chinese Chemical Letters
    "http://rss.sciencedirect.com/publication/science/2210271X",  # Computational and Theoretical Chemistry
    "http://rss.sciencedirect.com/publication/science/02235234",  # European Journal of Medicinal Chemistry
    "http://rss.sciencedirect.com/publication/science/09924361",  # European Journal of Organic Chemistry
    "http://rss.sciencedirect.com/publication/science/13877003",  # Inorganic Chemistry Communications
]

FEED_KEYWORDS = [
    "quimica organica",
    "quimica inorganica",
    "quimica analitica",
    "fisico-quimica",
    "quimica de materiais",
    "catálise",
    "biologia quimica",
    "quimica medicinal",
    "metodos computacionais",
    "novidades cientificas amplas",
]

PROMPT_ARTICLE_KEYWORD_LABELING = """
Analise rapidamente este artigo cientifico e retorne apenas JSON valido.

Palavras-chave prioritarias deste bloco:
{feed_keywords_text}

Contexto do bloco:
- O bloco Horizonte cobre novidades cientificas amplas no universo da quimica.
- Priorize artigos que ajudem a mapear tendencias, avancos metodologicos e temas de impacto amplo.
- Defina "matched" como true somente se o artigo fizer sentido como panorama cientifico relevante.

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
Priorize area cientifica, descoberta principal, tecnica ou implicacao ampla para a comunidade.
Inclua apenas o resumo final, em portugues brasileiro.

Artigo:
{article_content}
"""

PROMPT_IMPACT_RATING = """
Analise o resumo do artigo e estime sua relevancia para o bloco Horizonte.

Considere:
- alcance para a comunidade cientifica
- potencial de sinalizar tendencia importante
- amplitude tematica dentro da quimica
- relevancia metodologica ou interdisciplinar
- interesse para pesquisadores fora do nicho imediato do artigo

Use uma escala de 1 a 10:
1-2: interesse muito localizado e pouco util como panorama.
3-4: relevancia limitada a um nicho estreito.
5-6: artigo relevante para uma subarea, com valor moderado para o panorama.
7-8: forte relevancia ampla, com bom valor de atualizacao cientifica geral.
9-10: artigo raro, transversal e altamente importante para mapear o estado da ciencia.

Resumo:
"{summary}"

Retorne SOMENTE o numero inteiro de 1 a 10.
"""

PROMPT_CLUSTER_ANALYSIS = """
Estes sao resumos de artigos cientificos potencialmente relacionados do bloco semanal '{feed_profile}'.

{cluster_summaries_text}

Identifique qual tendencia, eixo metodologico ou frente cientifica ampla organiza o grupo.
Resuma em 3 a 5 frases o que este conjunto revela sobre o panorama cientifico atual.
Se os artigos nao forem realmente relacionados, diga isso claramente.

Responda em portugues brasileiro.
"""

PROMPT_BRIEF_SYNTHESIS = """
Voce esta escrevendo a sintese semanal do bloco Horizonte em Markdown.
Este bloco deve oferecer panorama amplo das novidades mais importantes no universo da quimica.

Com base apenas nos grupos analisados:
- apresente primeiro as tendencias cientificas mais amplas da semana
- depois organize topicos curtos por area, metodo ou direcao emergente
- encerre com uma leitura de conjunto sobre para onde o panorama cientifico parece estar se movendo

Mantenha tom tecnico, claro e objetivo.
Nao especule e nao invente informacoes.

Grupos analisados:
{cluster_analyses_text}
"""
