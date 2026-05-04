RSS_FEEDS = [
    "http://feeds.nature.com/nchembio/rss/current",  # Nature Chemical Biology
]   "http://feeds.nature.com/nbt/rss/current",  # Nature Biotechnology
    "http://feeds.nature.com/nmeth/rss/current", # Nature Methods
    "https://www.cell.com/cell/archive?publicationCode=cell&amp;rss=yes", # Cell
    "https://www.cell.com/molecular-cell/archive?publicationCode=molcel&amp;rss=yes", # Molecular Cell
    "https://www.cell.com/cell-reports/archive?publicationCode=celrep&amp;rss=yes", # Cell Reports
    
pt_br = " Responda em português brasileiro."

# Used in process_articles (operates globally, so uses default)
PROMPT_SCIENTIFIC_SUMMARY = """Você é um assistente de sumarização científica extremamente rigoroso.

Sua tarefa é resumir o texto fornecido com TOTAL fidelidade ao conteúdo original.

REGRAS OBRIGATÓRIAS:
- NÃO adicionar nenhuma informação que não esteja explicitamente no texto
- NÃO inferir, supor ou completar lacunas
- NÃO interpretar além do que está escrito
- NÃO criar conclusões próprias
- Se alguma informação não estiver clara no texto, simplesmente não mencione
- Use apenas informações que possam ser diretamente apontadas no conteúdo

OBJETIVO DO RESUMO:
Gerar um resumo claro, direto e estruturado que preserve completamente o significado original.

ESTRUTURA OBRIGATÓRIA:
Responda EXATAMENTE no seguinte formato:

1. Objetivo:
Descreva claramente qual é o objetivo do estudo.

2. Método:
Explique como o estudo foi conduzido (técnicas, abordagem, experimento, análise, etc.), apenas com base no texto.

3. Resultados:
Apresente os principais achados do estudo.

4. Conclusão:
Descreva a conclusão dos autores conforme explicitada no texto.

REGRAS DE LINGUAGEM:
- Escreva em português brasileiro
- Use linguagem clara e técnica, mas simplificada
- Evite frases longas e ambíguas
- Não use opiniões ou adjetivos desnecessários

IMPORTANTE:
Se qualquer uma das seções (objetivo, método, resultados, conclusão) não estiver presente ou não estiver clara no texto, escreva:
"Não especificado no texto"
)

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
