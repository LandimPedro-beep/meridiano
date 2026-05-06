RSS_FEEDS = [
    "http://feeds.nature.com/nchembio/rss/current",  # Nature Chemical Biology
   "http://feeds.nature.com/nbt/rss/current",  # Nature Biotechnology
    "http://feeds.nature.com/nmeth/rss/current", # Nature Methods
    "https://www.cell.com/cell/archive?publicationCode=cell&amp;rss=yes", # Cell
    "https://www.cell.com/molecular-cell/archive?publicationCode=molcel&amp;rss=yes", # Molecular Cell
    "https://www.cell.com/cell-reports/archive?publicationCode=celrep&amp;rss=yes", # Cell Reports
    "https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=achre4", # ACS Chemical Research
    "hhttps://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=abmcb8", # ACS Bio & Med Chem Au
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=acbcct", # ACS Chemical Biology
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=bichaw" # ACS Biochemistry
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=bomaf6", # ACS Biomacromolecules
    "http://feeds.nature.com/ncb/rss/current", # Nature Cell Biology
    "http://feeds.nature.com/nchem/rss/current", # Nature Chemistry
    "http://feeds.nature.com/ng/rss/current", # Nature Genetics
    "http://feeds.nature.com/nmicrobiol/rss/current", # Nature Microbiology
    "http://feeds.nature.com/nsmb/rss/current", # Nature Structural & Molecular Biology
    "http://bmcbiochem.biomedcentral.com/articles/most-recent/rss.xml", # BMC Biochemistry
    "http://bmcbiol.biomedcentral.com/articles/most-recent/rss.xml", # BMC Biology
    "http://bmcmicrobiol.biomedcentral.com/articles/most-recent/rss.xml", # BMC Microbiology
    "http://bmcmolbiol.biomedcentral.com/articles/most-recent/rss.xml", # BMC Molecular Biology
    "https://academic.oup.com/rss/site_5303/3169.xml", #The Journal of Biochemistry
    "http://rss.sciencedirect.com/publication/science/00063061", # Science Direct Bioinorcanical Chemistry
    "http://rss.sciencedirect.com/publication/science/09680896", # Science Direct Bioorganic & Medical Chemistry
    "http://rss.sciencedirect.com/publication/science/0960894X", # Science Direct Bioorganic & Medical Chemistry Letters
    "http://rss.sciencedirect.com/publication/science/0020711X", # Science Direct Journal of Biochemistry
    "http://rss.sciencedirect.com/publication/science/01620134", # Science Direct Journal of Inorganic Biochemistry
    "http://rss.sciencedirect.com/publication/science/0022328X", # Science Direct Journal of Oranometallic Chemistry
    "http://rss.sciencedirect.com/publication/science/13595113", # Science Direct Process Biochemistry

]   
pt_br = " Responda em português brasileiro."
FEED_KEYWORDS = [
    "bioquímica",
    "biologia molecular",
    "biotecnologia",
    "enzimas",
    "proteínas",
    "genética",
    "genômica",
    "metabolismo",
    "sinalização celular",
    "métodos experimentais",
]

PROMPT_ARTICLE_KEYWORD_LABELING = (
    "Analise rapidamente este artigo científico e retorne apenas JSON válido.\n\n"
    "Palavras-chave prioritárias deste feed:\n"
    "{feed_keywords_text}\n\n"
    "Instruções:\n"
    "- Gere rótulos curtos para os principais temas do artigo.\n"
    "- Defina \"matched\" como true somente se o artigo for relevante para as palavras-chave prioritárias do feed.\n"
    "- Os rótulos podem incluir temas úteis mesmo que não estejam na lista prioritária.\n"
    "- Não explique nada fora do JSON.\n\n"
    "Formato obrigatório:\n"
    "{{\"labels\":[\"rótulo 1\",\"rótulo 2\"],\"matched\":true}}\n\n"
    "Título:\n{article_title}\n\n"
    "Artigo:\n{article_content}" + pt_br
)

# Used in process_articles (operates globally, so uses default)
PROMPT_ARTICLE_SUMMARY = ("Resuma os pontos-chave do abstract deste artigo objetivamente em 3-5 frases. Se atenha apenas ao conteúdo do artigo, sem adicionar informações externas. O objetivo é criar um resumo conciso e informativo que capture os aspectos mais importantes do artigo, sem incluir opiniões ou análises. Adicione quebras de linha duplas entre os parágrafos para melhorar a legibilidade. Identifique os principais tópicos abordados no artigo. Inclua apenas o resultado da sumarização, sem prefaciar com nenhum texto adicional. Escreva em português brasileiro.\n\nArtigo:\n{article_content}" + pt_br)

# Used in rate_articles (operates globally, so uses default)
PROMPT_IMPACT_RATING = """Analise o resumo do artigo a seguir e estime seu impacto no 
contexto cientifico daquela área.
Considere fatores como impacto da revista publicada, relevância de resultados, objetivo do 
estudo, potencial de avanço científico, autores renomados e interesse da comunidade. Classifique o impacto em 
uma escala de 1 a 10, onde 1 representa um impacto mínimo e 10 representa um impacto 
extraordinário. Seja crítico e conservador ao atribuir pontuações — pontuações mais altas 
devem refletir estudos verdadeiramente excepcionais ou inovadores dentro do campo científico.

Avalie o impacto em uma escala de 1 a 10, usando estas diretrizes:

1-2: Significância mínima. Interesse de nicho ou notícias locais sem relevância mais ampla.
Exemplo: Um evento cultural local ou a abertura de um pequeno comércio.

3-4: Notável regionalmente. Acontecimentos de relevância em um estado ou região específica.
Exemplo: Mudanças na administração de uma cidade importante ou eventos regionais de grande participação.

5-6: Significativo nacionalmente. Afeta múltiplos estados ou tem relevância nacional moderada.
Exemplo: Greves de categorias importantes ou mudanças significativas em políticas públicas regionais.

7-8: Altamente significativo no Brasil. Grande relevância nacional, interrupções significativas ou
implicações de longo alcance. Exemplo: Um desastre natural em grande escala, crises políticas de grande
impacto ou escândalos nacionais.

9-10: Extraordinário e histórico no contexto brasileiro. Implicações nacionais graves e duradouras.
Exemplo: Mudanças constitucionais marcantes, crises econômicas severas ou eventos históricos que redefinem o país.

Lembrete importante: Pontuações de 9 a 10 devem ser extremamente raras e reservadas para eventos que
definem o Brasil. Sempre opte por uma pontuação menor, a menos que o impacto seja inegavelmente significativo.

Resumo:
"{summary}"

Digite SOMENTE o número inteiro que representa sua classificação (1 a 10).
"""

# Used in generate_brief (can be overridden per profile)
PROMPT_CLUSTER_ANALYSIS = (
    """
Estes são resumos de artigos de notícias potencialmente relacionados de um contexto '{feed_profile}':

{cluster_summaries_text}

Qual é o evento ou tópico principal discutido? Resuma os principais desenvolvimentos e a importância em 3 a 5 frases,
com base *apenas* no texto fornecido. Se os artigos parecerem não relacionados, informe isso claramente.
"""
    + pt_br
)

# Used in generate_brief (can be overridden per profile)
PROMPT_BRIEF_SYNTHESIS = """
Você é um assistente de IA escrevendo um briefing diário de inteligência no estilo presidencial usando Markdown,
especificamente para a categoria '{feed_profile}'.
Sintetize os seguintes grupos de notícias analisados em um resumo executivo coerente e de alto nível que será
apresentado em formato profssional.

Comece com os 4 ou 5 temas abrangentes mais críticos em relação ao Brasil ou dentro desta categoria,
com base *apenas* nestas informações.

Em seguida, forneça tópicos concisos resumindo os principais desenvolvimentos dentro dos grupos mais significativos
(aproximadamente 5 a 7 grupos).
Mantenha um tom objetivo e analítico relevante para o contexto '{feed_profile}'. Evite especulações.

Grupos de Notícias Analisados (Mais significativos primeiro):
{cluster_analyses_text}
"""
