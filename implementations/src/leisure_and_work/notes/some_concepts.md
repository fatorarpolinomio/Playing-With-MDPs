# Alguns Conceitos

Aqui, para que eu tenha local facilitado de consulta, anotarei um resumo acerca de conceitos que deverão ser aplicados nesta modelagem.

## Equação de Bellman

## Augmented State

O **aumento de estado** é uma técnica utilizada para **"Markovizar"** um problema onde a representação do **estado-padrão** falha ao capturar o histórico ou restrições.

Um **MDP padrão** precisa que o próximo estado dependa exclusivamente do estado e da ação atuais. Quando um ambiente possui obsevabilidade parcial, limites de tempo ou restrições dependentes do histórico, o estado-base é **Não-Markoviano**. Adicionar memória ou histórico na definição do estado **"Markoviza"** o problema novamente.

Utilizar um **Estado Aumentado** faz com que agentes otimizem objetivos respeitando limites de risco, parâmetros de segurança ou regras temporais.

### Exemplos & Aplicações

1) Memory-Augmented MDPs

2) Constrained MDPs

3) Quantile and Risk Objectives

## Horizonte Finito

> Será que ele falou a respeito de horizonte finito justamente porque eu trouxe como opção para modelagem o agente "sobreviver" a uma quantidade limitada de *timestamps*?

De acordo com o professor:

Com relação ao horizonte para o qual se estende o processo,
pode-se ter três opções: horizonte finito, horizonte infinito, e ho-
rizonte indeterminado. No caso do horizonte finito, é definido um
horizonte máximo N , de tal forma que o processo continua enquanto t menor ou igual a N . No caso do horizonte infinito, o processo nunca
para. Finalmente, no horizonte indeterminado, considera-se estados absorvedores, usualmente um conjunto de estados metas G, de
tal forma que o processo acaba quando st pertence a G.

Existem versões alternativas dos algoritmos aprendidos. Temos um **ValueIteration** para Horizonte finito, **Policy Iteration**, etc.

Imagino que, caso seja optado por seguir essa vertente, terei de implementar as versões alternativas.

# Teoria da Utilidade Esperada

## Função de Utilidade

## Neutralidade ao Risco
