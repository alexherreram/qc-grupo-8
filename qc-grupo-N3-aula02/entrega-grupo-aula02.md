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

c) Economia anual com a lifecycle policy?

---

## 🟡 Nível 2 — Respostas + Implementação

(Respostas + diagramas + código quando aplicável)

---

## 🔴 Nível 3 — Bônus (se aplicável)

(Respostas + scripts/links)

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