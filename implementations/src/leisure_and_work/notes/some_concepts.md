# Alguns Conceitos

Aqui, para que eu tenha local facilitado de consulta, anotarei um resumo acerca de conceitos que deverão ser aplicados nesta modelagem.

## Augmented State

O **aumento de estado** é uma técnica utilizada para **"Markovizar"** um problema onde a representação do **estado-padrão** falha ao capturar o histórico ou restrições.

Um **MDP padrão** precisa que o próximo estado dependa exclusivamente do estado e da ação atuais. Quando um ambiente possui obsevabilidade parcial, limites de tempo ou restrições dependentes do histórico, o estado-base é **Não-Markoviano**. Adicionar memória ou histórico na definição do estado **"Markoviza"** o problema novamente.

Utilizar um **Estado Aumentado** faz com que agentes otimizem objetivos respeitando limites de risco, parâmetros de segurança ou regras temporais.

### Exemplos & Aplicações

1) Memory-Augmented MDPs

2) Constrained MDPs

3) Quantile and Risk Objectives

## Horizonte Finito

## Neutralidade ao Risco
