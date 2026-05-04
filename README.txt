O projeto **Vértice** é uma plataforma digital voltada para **curadoria, organização e atualização contínua de conhecimento científico**, com foco inicial em pesquisadores da área de **Química (especialmente bioquímica e biologia molecular)** que atuam em ambiente acadêmico e/ou laboratorial.

### CONTEXTO GERAL

O Vértice nasce da necessidade de resolver um problema central:
o excesso de informação científica disponível e a dificuldade de transformar esse volume massivo de dados em **conhecimento útil, organizado e acionável no dia a dia do pesquisador**.

Pesquisadores, especialmente em áreas como bioquímica, lidam com:

* dezenas de artigos publicados diariamente
* múltiplas revistas científicas relevantes
* preprints, revisões sistemáticas, papers experimentais
* necessidade constante de atualização

No entanto, o processo atual é:

* fragmentado (várias fontes, RSS, plataformas isoladas)
* manual (triagem e leitura consomem muito tempo)
* pouco estruturado (sem organização baseada em contexto real de pesquisa)

O Vértice propõe uma solução integrada baseada em **curadoria inteligente + estruturação semântica + IA aplicada**.

---

### OBJETIVO PRINCIPAL

Criar um sistema que:

1. **Capture conteúdos científicos automaticamente** (via RSS, APIs, scraping estruturado)
2. **Organize esses conteúdos em blocos semanais**
3. **Classifique por relevância contextual para o pesquisador**
4. **Resuma sem distorcer o conteúdo original**
5. **Permita navegação eficiente e contínua pelo conhecimento**

---

### ARQUITETURA CONCEITUAL

O sistema é estruturado em **blocos semanais de atualização**, organizados em três grandes pilares:

#### 1. BLOCO VETOR - ESPECIALIZADO NOVO (INTERESSE DIRETO) 

Conteúdos novos alinhados com a linha de pesquisa do usuário, altamente relevantes para a área específica do pesquisador lançado naquela semana em especifico.

Contexto:

É o jornal do pesquisador, aparecerá tendencias que o docente tem que estar por dentro sempre, a leva de artigos é atualizada toda semana.

Critérios:

* alta relevância temática
* a novidade da área

---

#### 2. BLOCO MATRIZ - TOP TIER

 Conteúdos maduros alinhados com a linha de pesquisa do usuário, altamente relevantes para a área específica do pesquisador lançado em 10-15 anos, são materiais já relevantes academicamente e muito citados, material que tem que ser conhecido e DOMINADO pelo pesquisador da área.  

Contexto:

Uma lista de 10 artigos modernos que já se provaram relevantes no ambiente academico atualizados toda semana. O pesquisador deve conhecer e atualizar-se sobre estes conteúdos para se manter vivo cientificamente. Inclui artigos de revisão.

Critérios:

* artigos amplamente citados
* relevância academica inquestionável
* publicação ter 10 a 15 anos

---

#### 3. BLOCO HORIZONTE - GLOBAL (PANORAMA CIENTÍFICO)

Conteúdos novos de todas as áreas da química, sem relação pessoal com a área de pesquisa do usuário, apenas para atualizações semanais de artigos cientificos diversos

Exemplo:

 Conteúdos amplos e estruturais de química, engloba todas as áreas da química, um pesquisador independente da área tem que estar atento a tendencias no meio cientifico e saber o que existe de mais novo. Área de novidades, tendo sempre artigos novos toda semana com atualizações do universo cientifico no geral.  

Critérios:

* relevância global
* impacto científico amplo
* Situar-se novidade nas áreas de química orgânica, química inorgânica, química analítica, fisico-química, química de materiais, biologia, etc..

---

### FLUXO DE FUNCIONAMENTO

1. **Ingestão de dados**

   * RSS de revistas científicas (Nature, Science, etc.)
   * repositórios (arXiv, PubMed)
   * outras fontes confiáveis

2. **Filtragem inicial**

   * remoção de duplicatas
   * seleção por palavras-chave
   * classificação preliminar

3. **Processamento com IA**

   * sumarização fiel (sem extrapolação)
   * possível uso de embeddings para clustering semântico
   * classificação contextual
   * rating de impacto dos artigos definido por critérios específicos para cada bloco

4. **Organização semanal**

   * distribuição nos 3 blocos
   * limite de artigos por bloco (curadoria forte, não volume)
   * agrupamento de artigos/tópicos interseccionais mensais que estimulem a fusão de pesquisas

5. **Entrega ao usuário**

   * interface estilo dashboard
   * leitura fluida
   * navegação por blocos

---

### PRINCÍPIOS DO PROJETO

* **Fidelidade ao conteúdo original**

  * nada de alucinação de IA
  * resumos devem respeitar estritamente o texto

* **Curadoria > quantidade**

  * poucos artigos bem escolhidos valem mais que muitos irrelevantes

* **Organização cognitiva**

  * estrutura pensada para como o pesquisador aprende e se atualiza

* **Eficiência**

  * reduzir tempo de triagem
  * maximizar absorção de conhecimento

---

### TECNOLOGIA E EXPERIMENTAÇÃO

O projeto está em fase experimental e envolve:

* uso de LLMs locais (ex: Mistral, Phi-3 via Ollama)
* testes com embeddings (ainda em exploração)
* arquitetura modular (evitar acoplamento forte com provedores específicos)
* backend com manipulação intensiva de texto
* ingestão automatizada de conteúdo científico

Há também preocupação com:

* performance (rodar localmente)
* independência de APIs externas
* escalabilidade futura

---

### RELAÇÃO COM O PROJETO MERIDIANO

O Vértice pode ser entendido como uma evolução conceitual do projeto anterior (**Meridiano**), herdando:

* estrutura de processamento de conteúdo
* base de experimentação com IA
* desafios arquiteturais (acoplamento, configuração de modelos, etc.)

Porém, o Vértice avança no sentido de:

* maior clareza de propósito
* foco no usuário pesquisador
* estrutura editorial mais definida

---

### DESAFIOS ATUAIS

* definir pipeline robusto de ingestão de dados
* melhorar qualidade de sumarização
* organizar classificação semântica eficiente
* formar critérios reais para prompts das IAs
* criar uma interface funcional e limpa
* garantir consistência semanal do conteúdo
* armazenar e organizar dados com uso a longo prazo
* personalização de linha de interesse fluída

---

### VISÃO FUTURA

O Vértice pode evoluir para:

* sistema adaptativo ao perfil do pesquisador
* recomendação baseada em histórico
* mapas de conhecimento
* integração com workflow acadêmico (Zotero, Notion, etc.)
* alertas inteligentes de descoberta científica

---

### RESUMO FINAL

O Vértice não é apenas um agregador de artigos.

Ele é um **sistema de curadoria científica orientado por estrutura cognitiva**, que transforma um fluxo caótico de publicações em um **processo contínuo, organizado e eficiente de atualização intelectual para pesquisadores**.

O objetivo final é simples, mas profundo:

> Permitir que o pesquisador se mantenha atualizado com o máximo de qualidade e o mínimo de esforço.

---
