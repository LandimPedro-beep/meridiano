RSS_FEEDS = [
    "http://feeds.nature.com/nchembio/rss/current",  # Nature Chemical Biology
   "http://feeds.nature.com/nbt/rss/current",  # Nature Biotechnology
    "http://feeds.nature.com/nmeth/rss/current", # Nature Methods
    "https://www.cell.com/cell/archive?publicationCode=cell&amp;rss=yes", # Cell
    "https://www.cell.com/molecular-cell/archive?publicationCode=molcel&amp;rss=yes", # Molecular Cell
    "https://www.cell.com/cell-reports/archive?publicationCode=celrep&amp;rss=yes", # Cell Reports
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
PROMPT_IMPACT_RATING = """Analise o resumo da notícia a seguir e estime seu impacto no contexto brasileiro.
Considere fatores como noticiabilidade, relevância para o público brasileiro, abrangência geográfica
(local, regional ou nacional), número de pessoas afetadas, gravidade e potenciais consequências a longo prazo
para o Brasil. Seja extremamente crítico e conservador ao atribuir pontuações — pontuações mais altas devem
refletir eventos verdadeiramente excepcionais ou raros dentro da realidade brasileira.

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
