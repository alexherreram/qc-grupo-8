# README do material da aula

## Resumo

Usamos os arquivos Terraform do próprio laboratório. Não criei nenhum Terraform novo.

O material foi montado a partir do que já estava pronto no ambiente da aula, e a maior dificuldade foi sincronizar as criações, os recursos e as sessões para que tudo ficasse consistente.

## O que mais deu trabalho

O ponto mais difícil foi a coordenação entre:

- criação dos recursos do laboratório;
- execução das sessões;
- uso dos arquivos Terraform existentes;
- organização das evidências e do material final.

Além disso, o Synapse acabou sendo mais difícil do que parecia por causa do Terraform: a configuração do ambiente e a ordem de criação dos recursos ficaram bem mais delicadas do que o enunciado sugeria. Terminei ajustando grande parte da parte de Synapse manualmente porque a automação do Terraform não ficou estável no fluxo do laboratório.

Também houve um problema no código Python do AI Search vector: o parâmetro da busca estava errado e foi preciso ajustar a sintaxe para a API correta do Azure Search. Isso exigiu revisão do script e correção de compatibilidade antes da busca funcionar corretamente.

Em outras palavras, o problema não foi criar infraestrutura nova, e sim alinhar tudo para que o resultado final refletisse o que foi realmente executado no laboratório.

## Observação final

Todos os artefatos foram reaproveitados do exercício em laboratório. Não houve necessidade de construir um Terraform novo. O maior esforço foi garantir que as criações e o contexto da aula estivessem sincronizados antes de organizar o material final, e o Synapse + o ajuste no script do AI Search foram os pontos mais delicados do processo.
