

# "Qual a probabilidade de chegarmos no estado s', dado que estamos partindo de s
# e estamos tomando a ação a?
# Pr(s'|s, a) -> Versão genérica para o problema, onde são arbitrários:
#  1) nro. de estados,
#  2) nro. aritrário de faces nos dados,
#  3) valores para cada face,
#  4) estado final.
# --------------------------------------------------------------------------------
# start_state: estado de onde estamos partindo
# target_state: estado onde supostamente vamos chegar
# final_state: diz respeito ao estado onde, ao chegarmos, finalizamos o jogo (nosso objetivo final)
# states: nossa lista de estados, precisamos dela para termos noção a respeito da
# quantidade total de estados
# action_results: lista com todas as faces (resultados possíveis) dos dados,
# logo todos os resultados possíveis da ação escolhida

def transition_function(
    start_state : int,
    target_state : int,
    final_state : int,
    states : list[int],
    action_results : list[int]):

    # Caso já estejamos no estado final, o jogo já acabou. Não preciso tomar ação
    if start_state == final_state and start_state == target_state:
        return 1 # Caso o meu alvo seja o estado final, eu já estou nele. Então a prob é 1
    elif start_state == final_state and start_state != target_state:
        return 0 # Caso o meu alvo não seja o final, não poderei ir para lá de maneira alguma. Pois, já acabou

    prob_number = 0.0 # Aqui será o nosso valor retornado pela iteração para cada resultado

    for result in action_results:
        # Se o deslocamento obtido no resultado consegue parar no meu estado-alvo (ida e volta)
        if(start_state + result) == target_state or (len(states) -  1 - abs(len(states) - 1 - (start_state + result))) == target_state:
            prob_number += 1/len(action_results) # Vamos acumular tendo como base a prob de cair aquela face

    return prob_number
