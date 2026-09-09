# main.py
from mdp_python.MDecisionProcess import PyDynamicProgramming


def main():
    print(" Importando a biblioteca compilada...")

    # Instanciando o nosso motor C++ (rewardValue, discountRate, threshold)
    motor_dp = PyDynamicProgramming(0.0, 0.9, 0.001)

    print(" Motor instanciado com sucesso!")
    print(f"-> Limite de convergência (Threshold): {motor_dp.threshold}")
    print(f"-> Taxa de Desconto (Gamma): {motor_dp.discount_rate}")

    # Se chegamos até aqui sem erros, a ponte Python <-> C++ está perfeita!
    print("\n Tudo pronto para rodar os algoritmos de MDP!")


if __name__ == "__main__":
    main()
