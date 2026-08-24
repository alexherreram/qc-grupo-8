# Entrega Aula <XX> — Grupo <NN>

**Disciplina:** Cloud & Cognitive Environments — FIAP MBA AI Engineering & Multi-Agents
**Turma:** <código da sua turma>
**Data de entrega:** <DD/MM/AAAA>

## Grupo

| # | Nome completo | GitHub | E-mail FIAP |
|---|---------------|--------|-------------|
| 1 | Alex Herrera Martins|https://github.com/alexherreram |rm373253@fiap.com.br |
| 2 | Renata Brasil Silva               |        | RM373353@fiap.com.br |
| 3 | Rodolfo Avelino da Fonseca Vieira |        | RM373195@fiap.com.br |
| 4 | Rodrigo Paolo Terra de Oliveira   |        | RM313739@fiap.com.br |

## Distribuição do trabalho

| Membro | Nível assumido | Item específico |
|--------|----------------|-----------------|
| Rodrigo Paolo | 🟢 N1 | Exercícios 1.1, 1.2, 1.3 |
| Renata e Rodolfo | 🟡 N2 | Exercício 2.1 — Arquitetura QC |
| Alex | 🟡 N2 | Exercício 2.2 — Comparativo |
| Alex | 🔴 N3 (bônus) | Exercício 3.1 — IaC avançado |
| Todos | 🟢 N1 (apoio) | Revisão das respostas N1 |

> Regra: cada membro deve ter pelo menos uma contribuição. O **rodízio entre aulas** (quem fez N1 antes faz N2 depois) é incentivado e vale o ponto do Critério 4 (ver [rubrica.md](rubrica.md)).

---

## 🟢 Nível 1 — Respostas

### Exercício 1.1

| Cenário | Tipo | Justificativa |
|---|---|---|
| Hospedar imagens de produtos do e-commerce QC (5M de SKUs) | Object storage | Escala para milhões de arquivos, alta durabilidade e acesso via HTTP/CDN, sem exigir gerenciamento de servidores ou volumes. |
| Disco onde roda o sistema operacional de uma VM de banco | Block storage | Oferece um volume persistente de baixa latência, conectado diretamente à VM e adequado ao sistema operacional. |
| Pasta compartilhada entre 10 VMs de um time de DevOps | File storage | Permite que várias VMs acessem simultaneamente os mesmos diretórios e arquivos por meio de um sistema de arquivos compartilhado. |
| Backup mensal de bancos de dados (retenção 7 anos) | Object storage de arquivamento | É econômico para retenção longa, oferece alta durabilidade e permite aplicar políticas de ciclo de vida para mover os backups a classes de armazenamento frio. |
| Storage de modelos `.pkl` do time de ML para serving | Object storage | Centraliza os artefatos versionados, facilita o compartilhamento entre ambientes e permite que os servidores de serving baixem os modelos sob demanda. |
| Dump diário de logs de aplicação para análise futura | Object storage | É adequado para grandes volumes de dados gerados continuamente, com retenção configurável e integração com ferramentas de análise posteriormente. |

### Exercício 1.2

A Quantum Commerce armazena 2 TB de logs de compras. Os primeiros 30 dias os logs são consultados para detecção de fraude (Hot). Depois disso, viram dados arquivados de compliance LGPD (Archive, retenção 5 anos).

a) Quanto custaria 1 mês desses logs se mantidos 100% em Hot tier? (Use ~$0,018/GB/mês)

**Resposta: 2.048 GB × $0,018 = $36,86/mês (~$442/ano)**

b) Quanto custaria 1 mês desses logs com lifecycle: 30 dias Hot + Archive depois? (Archive ~$0,002/GB/mês)

**Resposta:** 

**-Hot: 2048 × 30/365 × $0,018 = $3,03/mês (média anual)**

**-Archive: 2048 × 335/365 × $0,002 = $3,76/mês (média anual)**

**Total de aproximadamente 6,79 por mês.**


c) Economia anual com a lifecycle policy?

**($36,86 - $6,79) × 12 = ~$360/ano.**

### Exercício 1.3

| Caso de uso | Relacional (Azure SQL) | NoSQL doc (Cosmos) | Vector DB (AI Search) | Justificativa |
|---|---|---|---|---|
| Carrinho de compras ativo do usuário | — | X | — | O documento pode ter esquema variável para diferentes itens e permite leitura e atualização rápidas por chave do usuário. |
| Catálogo de produtos com SKU, preço, estoque | X | — | — | SKU, preço e estoque possuem estrutura definida e precisam de consistência nas atualizações de inventário. |
| Reviews dos clientes (texto livre + score) | — | X | — | O formato pode variar e o documento acomoda bem texto livre, nota, autor e metadados da avaliação. |
| "Encontre produtos similares a este" (recomendação) | — | — | X | A busca vetorial compara embeddings de produtos para encontrar itens semanticamente semelhantes. |
| Histórico de pedidos para faturamento | X | — | — | Pedidos e itens faturáveis exigem relacionamentos, integridade referencial e transações confiáveis. |
| Sessão do usuário (chave-valor, expira em 30min) | — | X | — | O modelo NoSQL atende ao acesso rápido por chave e permite configurar TTL de 30 minutos. |
| Logs de comportamento de navegação | — | X | — | O volume é alto e o esquema pode evoluir, tornando documentos flexíveis mais adequados para ingestão e consulta. |

### Exercício 1.4

| Perfil | Role no Key Vault | Justificativa |
|---|---|---|
| Você (criador do Vault, faz dev e ops) | Key Vault Secrets Officer | Precisa criar, ler, atualizar e excluir segredos durante as atividades de desenvolvimento e operações. Essa role evita conceder administração completa do cofre. |
| Azure Function que consulta `T_PRODUTOS` precisa ler a connection string | Key Vault Secrets User | Permite ler o valor dos segredos, necessário para obter a connection string, sem conceder permissão para alterá-los. |
| Engenheiro de segurança que audita os segredos sem alterá-los | Key Vault Reader | Permite consultar o cofre e os metadados dos segredos para auditoria, sem acesso ao conteúdo nem permissão para alterá-los. |
| Pipeline de CI/CD que injeta novos segredos automaticamente | Key Vault Secrets Officer | Permite criar e atualizar segredos para a automação do pipeline, sem conceder controle administrativo sobre o cofre. |
| Time de FinOps que precisa ver custo do Vault sem ver segredos | Reader | Permite visualizar o recurso e seus metadados, sem acesso ao conteúdo dos segredos; a análise de custos deve ser autorizada também no escopo de cobrança adequado. |


---

## 🟡 Nível 2 — Respostas + Implementação

### Exercício 2.1 — Modelagem de dados da QC (em grupo)


| Domínio | Serviço Azure escolhido | SKU/Configuração | Justificativa em 1-2 frases |
|---|---|---|---|
| Produtos | Azure Cosmos DB for NoSQL | Particionamento por `categoriaId` ou `sku`, autoscale e índice para SKU | O catálogo tem grande volume e acesso distribuído, e o modelo de documentos facilita a evolução dos atributos dos produtos. O autoscale absorve variações nas consultas do e-commerce. |
| Clientes | Azure Cosmos DB for NoSQL | Particionamento por `clienteId`, autoscale e alta disponibilidade entre regiões | O perfil, endereço e preferências formam um documento consultado frequentemente por cliente. A distribuição por `clienteId` escala os cerca de 50 milhões de registros. |
| Pedidos | Azure SQL Database | Tier Business Critical, zone-redundant e backups com retenção adequada | Pedidos exigem transações ACID, integridade referencial e consistência forte para faturamento. O tier Business Critical oferece baixa latência e alta disponibilidade. |
| Carrinhos ativos | Azure Cosmos DB for NoSQL | Particionamento por `clienteId`, autoscale e TTL de 24 horas | O carrinho é um documento de leitura e atualização rápida por usuário, com esquema flexível. O TTL remove automaticamente carrinhos abandonados após 24 horas. |
| Reviews | Azure Cosmos DB for NoSQL | Particionamento por `produtoId`, autoscale e integração com Azure AI Language | Documentos acomodam texto livre, score e metadados variáveis em grande escala. As reviews podem ser processadas posteriormente para análise de sentimento. |
| Busca de produtos | Azure AI Search | Réplicas para disponibilidade, partições para escala e índices semântico e vetorial | O serviço combina busca textual, semântica e vetorial para consultas do frontend e dos agentes. Réplicas aumentam a capacidade de consulta e a disponibilidade. |
| Sessões | Azure Cache for Redis | Premium, replicação e TTL de 30 minutos | Redis oferece acesso em memória com baixa latência para sessões ativas e dados temporários. O TTL evita manter sessões expiradas e reduz o consumo de memória. |
| Histórico de navegação | Azure Event Hubs + Azure Data Lake Storage Gen2 | Event Hubs particionado para ingestão e Data Lake em Parquet com lifecycle | Event Hubs absorve bilhões de eventos com ingestão distribuída, enquanto o Data Lake armazena o histórico de forma durável e econômica para análises futuras. |
| Modelos de ML | Azure Machine Learning | Workspace com Model Registry, Blob Storage e endpoints gerenciados com autoscale | O Model Registry versiona e promove os modelos de recomendação, classificação e churn entre ambientes. Os endpoints gerenciados permitem serving escalável e monitorado. |


![Diagrama da arquitetura e modelagem de dados da QC](../diagramas/diagrama.drawio.png)


### Exercício 2.2 — Plano de migração de dados

#### Plano de migração em 12 meses

| Período | Atividades principais | Resultado esperado |
|---|---|---|
| Meses 1-2 | Inventariar os 8 TB do Oracle, os 50 TB do NAS e as fitas; classificar dados pessoais, definir RTO/RPO, requisitos LGPD, orçamento e critérios de sucesso. | Escopo aprovado, riscos conhecidos e arquitetura de destino definida. |
| Mês 3 | Provisionar Azure SQL Database, Cosmos DB, Blob Storage/Data Lake, AI Search e Azure Machine Learning. Configurar regiões, rede privada, RBAC, Key Vault, criptografia, monitoramento e políticas de backup. | Landing zone pronta e validada para receber os dados. |
| Meses 4-5 | Fazer piloto do Oracle com uma base não crítica. Usar Azure Database Migration Service em modo online para carga inicial e replicação contínua; validar schema, desempenho, integridade e aplicações. | Procedimento de migração testado e plano de rollback aprovado. |
| Meses 6-7 | Migrar o Oracle de forma incremental por domínio, começando por produtos e clientes e depois pedidos. Manter a replicação, executar testes de reconciliação e preparar o cutover com dual-write ou fila de alterações. | Dados atuais disponíveis no Azure sem interrupção do sistema. |
| Meses 8-9 | Copiar as imagens do NAS para Blob Storage com AzCopy, preservando estrutura e metadados. Usar cópia inicial, sincronizações incrementais, validação por hash e CDN para distribuição. | 50 TB de imagens conferidos e servidos pelo novo storage. |
| Meses 10-11 | Restaurar as fitas gradualmente em uma área de staging, validar checksums e catalogar os 200 TB. Enviar em lotes para Blob Storage/Data Lake, aplicar Archive tier e configurar retenção e imutabilidade para compliance fiscal. | Histórico recuperado, catalogado e protegido contra exclusão indevida. |
| Mês 12 | Executar o cutover final do Oracle, trocar endpoints, monitorar por 30 dias e manter o ambiente legado em modo somente leitura até cumprir o período de rollback. Desativar fontes antigas somente após aceite formal e teste de restauração. | Operação estabilizada, custos medidos e migração encerrada com evidências de auditoria. |


#### a) 6 Rs por repositório

| Repositório | 6 R escolhido | Motivo |
|---|---|---|
| Produtos (catálogo) | Replatform | Migrar para Cosmos DB for NoSQL, mantendo a lógica principal, mas adotando um modelo de documentos escalável. |
| Clientes | Replatform | Usar Cosmos DB for NoSQL com particionamento por `clienteId`, reduzindo a necessidade de administrar servidores. |
| Pedidos | Replatform | Migrar para Azure SQL Database com alta disponibilidade, preservando o modelo relacional e as transações ACID. |
| Carrinhos ativos | Refactor | Adaptar o acesso para Cosmos DB com TTL de 24 horas, aproveitando o padrão de documento e a escala elástica. |
| Reviews | Replatform | Armazenar os documentos no Cosmos DB e integrar o processamento de sentimento ao Azure AI Language. |
| Busca de produtos | Refactor | Reestruturar a indexação para Azure AI Search, incluindo busca semântica e vetorial. |
| Sessões | Replatform | Mover o armazenamento temporário para Azure Cache for Redis, sem alterar o comportamento funcional da aplicação. |
| Histórico de navegação | Replatform | Direcionar eventos para Event Hubs e armazenamento analítico no Data Lake Storage Gen2. |
| Modelos de ML | Replatform | Centralizar versões e endpoints no Azure Machine Learning, preservando os artefatos e o ciclo de serving. |

#### b) Serviços Azure por repositório

| Repositório | Serviço Azure | Configuração considerando custo e criticidade |
|---|---|---|
| Produtos | Azure Cosmos DB for NoSQL | Autoscale, particionamento por `sku` ou `categoriaId`, backup contínuo e CDN para imagens. |
| Clientes | Azure Cosmos DB for NoSQL | Particionamento por `clienteId`, criptografia, autoscale e redundância entre regiões conforme o RTO/RPO. |
| Pedidos | Azure SQL Database | Business Critical, zone redundancy, Always Encrypted para dados sensíveis e backups com retenção definida. |
| Carrinhos ativos | Azure Cosmos DB for NoSQL | Autoscale, particionamento por `clienteId` e TTL de 24 horas para evitar custo de retenção desnecessário. |
| Reviews | Azure Cosmos DB for NoSQL + Azure AI Language | Autoscale, particionamento por `produtoId` e processamento assíncrono de sentimento. |
| Busca de produtos | Azure AI Search | Partições conforme o volume do índice e réplicas conforme a carga de consultas; habilitar busca semântica e vetorial. |
| Sessões | Azure Cache for Redis | Standard ou Premium conforme a necessidade de replicação, com TTL de 30 minutos. |
| Histórico de navegação | Azure Event Hubs + Data Lake Storage Gen2 | Event Hubs particionado para ingestão e Data Lake em Parquet, com lifecycle para camadas frias. |
| Modelos de ML | Azure Machine Learning + Blob Storage | Model Registry, armazenamento de artefatos e endpoints gerenciados com autoscale. |

#### c) Migração sem downtime

1. Inventariar os dados, executar uma migração piloto. Criar os recursos Azure, configurar as replicações necessárias antes da cópia.
2. Para bancos relacionais, usar o Azure Database Migration Service em modo online: fazer carga inicial, manter a replicação contínua das alterações e monitorar o lag.
3. Para imagens e arquivos, usar o AzCopy em uma cópia inicial e depois sincronizações incrementais.
4. Em uma janela controlada, pausar apenas as escritas por alguns segundos, aplicar o delta final, validar a consistência, trocar o endpoint e manter o ambiente antigo disponível para rollback.

#### d) Estimativa de egress das imagens

Assumindo 50 TB decimais, aproximadamente 50.000 GB, uma saída inicial para a Internet a US$ 0,087/GB custaria cerca de **US$ 4.350**. Considerando 100 GB gratuitos, a estimativa fica em aproximadamente **US$ 4.341,30**; o valor real varia por região, destino e contrato Azure, e a transferência entre serviços Azure na mesma região pode ter cobrança diferente.

Obs: Considerando o dolar a 5, ficaria próximo de 22mil reais..


#### e) Compliance LGPD

Manter dados pessoais e bancos primários de brasileiros em regiões Azure no Brasil, preferencialmente Brazil South, restringindo replicações e backups a regiões aprovadas. Aplicar criptografia em trânsito e em repouso, RBAC com menor privilégio, Key Vault para segredos, Private Link, logs de auditoria, políticas de retenção e anonimização/pseudonimização para análises. Transferências internacionais devem ter base legal e garantias contratuais adequadas, além de atender aos direitos dos titulares e às políticas da ANPD.


### Exercício 2.3 — Particionamento no Cosmos DB

No lab da Aula 2, o container reviews foi particionado por produto_id. Responda:

#### a) Chaves que não seriam boas opções

**`id` da review (3 razões):**

1. Tem cardinalidade muito alta, normalmente um valor único por documento, distribuindo cada review em uma partição lógica diferente.
2. Consultas como “todas as reviews de um produto” não informariam a partition key, exigindo uma consulta cross-partition, mais cara e menos previsível.
3. Não agrupa as reviews que são relacionadas, que acaba atrapalhando paginação e aalise detalhada por produto, por exemplo.

**`score` de 1 a 5 (2 razões):**

1. Tem cardinalidade muito baixa: quase todos os documentos ficariam concentrados em apenas cinco valores de chave.
2. A distribuição desigual pode criar partições quentes e limitar a escala quando muitos usuários consultarem ou gravarem reviews com o mesmo score.

**`data_da_review` (timestamp) (2 razões):**

1. Timestamps atuais são valores com alta cardinalidade e fazem novas gravações se concentrarem no intervalo de tempo mais recente, criando hotspot.
2. Consultas por produto não seriam direcionadas a uma única partição; seria necessário consultar várias partições para reunir as reviews daquele produto.

#### b) Limitação de `produto_id`

`produto_id` funciona razoavelmente bem porque agrupa as reviews do mesmo produto e direciona consultas comuns, como listar ou calcular a média de avaliações de um produto. O problema é a distribuição desigual: um produto muito popular pode acumular muitas escritas e leituras em uma única partição lógica, criando uma partição quente e limitando a escala daquele produto.

#### c) Estratégia para consultar reviews de um cliente

Usaria uma chave hierárquica com `cliente_id` como primeiro nível, por exemplo `/cliente_id`, `/produto_id` e `/review_id`. Assim, consultas que informam o `cliente_id` conseguem ser roteadas pelo prefixo da chave e as reviews de um cliente ficam organizadas sob esse valor; `produto_id` e `review_id` ajudam a distribuir clientes com muitos documentos.

Essa decisão deve ser baseada no padrão dominante de consulta: ela otimiza “todas as reviews de um cliente”, mas torna menos eficiente o padrão “todas as reviews de um produto” quando apenas `produto_id` é informado. Para suportar os dois padrões com baixa latência, a alternativa é manter uma segunda projeção/container desnormalizado particionado por `produto_id`, aceitando o custo de duplicação e sincronização.

#### d) Tamanho aproximado da partição lógica

Assumindo que cada documento de review ocupe aproximadamente 1 KB, incluindo campos JSON e metadados relevantes:

**50.000 reviews × 1 KB ≈ 50.000 KB ≈ 49 MB (aproximadamente 50 MB).**

Comparando com a quota de 20 GB por partição lógica:

**50 MB ÷ 20.480 MB × 100 ≈ 0,24%.**

Portanto, um produto com 50.000 reviews está muito abaixo do limite de 20 GB. O risco principal nesse cenário não é o tamanho, mas o hotspot de operações se esse produto receber tráfego muito superior ao dos demais.


---

## 🔴  Nível 3 — Avançado: Vector Search Real e Analytics

### Exercício 3.1 — Vector search verdadeira no AI Search

### Parte A

**-Resultado vector search:**

=== Vector search: 'preciso de uma cadeira boa para minha coluna' ===

    [0.6849] Cadeira Gamer Vermelha
    [0.6840] Cadeira Home Office Confortável
    [0.6665] Camiseta Polo Masculina

=== Vector search: 'algo para acompanhar séries' ===

    [0.6240] Camiseta Polo Masculina
    [0.6075] Mochila para Notebook 15.6
    [0.5945] Cafeteira Italiana 6 Xícaras

=== Vector search: 'presente para um amigo que ama café' ===

    [0.6821] Cafeteira Italiana 6 Xícaras
    [0.6783] Cafeteira Nespresso Essenza Mini
    [0.6133] Cadeira Gamer Vermelha

**-Resultado lab:**

Busca por keyword: “cadeira escritório”

    [8.44] Cadeira Ergonômica DXRacer
    [5.68] Cadeira Home Office Confortável
    [5.49] Cadeira Gamer Vermelha

Busca semântica: “algo para trabalhar em pé”

    [2.22] Mesa de Escritório com Regulagem de Altura — Mesa em pé com motor elétrico e tampo 140x70cm...
    [1.77] Calça Jeans Slim — Calça jeans slim fit elastano para conforto...
    [1.75] Cadeira Gamer Vermelha — Cadeira giratória com encosto reclinável e apoio para braços...

Filtro por categoria “moveis” + ordenação por preço

    R$ 79,00 — Cadeira Home Office Confortável
    R$ 129,00 — Cadeira Gamer Vermelha
    R$ 149,90 — Cadeira Ergonômica DXRacer
    R$ 289,00 — Mesa de Escritório com Regulagem de Altura


**Resposta:**

---lab: melhor para entender o que o cliente quer em linguagem natural;

---vector search: melhor para encontrar itens semanticamente próximos em escala real;

---ambos falham sem filtros por categoria e contexto.

## Parte B

1) Por que o modelo all-MiniLM-L6-v2 é uma má escolha para produção da Quantum Commerce?

    R:  Porque ele foi desenhado para desempenho geral, não para qualidade de produção em um catálogo de e-commerce em português, com alta escala e exigência de precisão.

2) Que serviço da Azure você usaria para gerar embeddings em produção?

    R: Azure OpenAI com o modelo text-embedding-3-large

3) Como manter os embeddings atualizados quando produtos novos chegam?

    R: Usaria um pipeline incremental, em vez de regenerar tudo de novo.

    Resumo, para novos produtos, embedar imediatamente. Quado alterados, re-embeddar. Para produtos antigos reprocessar periodicamente.

4) Quanto custaria gerar embeddings para 5M de produtos da QC com Azure OpenAI?

    R: Em uma estimativa realista do Azure OpenAI, usando text-embedding-3-large, o custo de geração inicial fica na faixa de US$ 130 a US$ 350 para 5 milhões de produtos, dependendo do tamanho médio do texto embutido (nome, descrição, atributos e categoria). Isso equivale a cerca de US$ 0,03 a US$ 0,07 por produto em média, antes de custos de armazenamento, indexação e consultas. Em produção, esse processo é feito de forma incremental, reprocessando apenas produtos novos ou alterados, o que mantém o custo controlado.
---

## Reflexão coletiva

3-5 parágrafos respondendo:

1. O que o grupo aprendeu de mais importante nesta aula?
2. Como isso se conecta com a arquitetura cloud de uma plataforma agentic?
3. Que decisão arquitetural vocês fariam diferente se começassem o projeto QC hoje?

---

## Artefatos do ZIP

- Diagrama: `diagramas/arquitetura-qc-aulaXX.png`
- Código IaC: `terraform/`
- Scripts: `scripts/`
- Endpoint ativo (se houver): URL pública sem credenciais — apenas para demonstração durante a janela de correção