import numpy as np  # Importa a biblioteca NumPy para operações numéricas
from .utils import str_to_complex  # Importa a função str_to_complex do módulo utils

# Definição dos valores de erro em estructuras complexas
struct = "complex"  # Define o tipo de estrutura como complexo
e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14 = 1.09, 1.0, 1.01, 1.0, 1.0, 1.07, 1.09, 1, 1, 1, 1, 1, 1, 1  # Valores de tensão para cada barra
# -*- coding: utf-8 -*-  # Define a codificação do arquivo como UTF-8

# Função para resolver o fluxo de carga pelo método Gauss-Seidel
def solve_power_flow(matriz_admt, tipo_barras, impedancias, erro_max=1e-6, K_max=1000):  # Define a função principal do método Gauss-Seidel
    """Resolve o fluxo de carga pelo método Gauss-Seidel"""
    contador = 0  # Inicializa o contador de iterações
    erro = 0.0001  # Inicializa o erro

    # Preparação dos vetores
    vetor_tensao = [str_to_complex(val) for val in tipo_barras["VOLTAGE MAGNITUDE"]]  # Converte as tensões para números complexos
    vetor_pot_ativa = [  # Calcula o vetor de potência ativa líquida para cada barra
        (float(tipo_barras.iloc[i]["GENERATOR (MW)"]) - float(tipo_barras.iloc[i]["LOAD (MW)"])) / 100 # Converte MW para pu
        for i in range(len(tipo_barras))
    ]
    vetor_pot_reativa = [  # Calcula o vetor de potência reativa líquida para cada barra
        (float(tipo_barras.iloc[i]["GENERATOR (MVAR)"]) - float(tipo_barras.iloc[i]["LOAD (MVAR)"])) / 100 # Converte MVAR para pu
        if tipo_barras.index[i] != 1 else 0  # Se for barra slack, a potência reativa é zero
        for i in range(len(tipo_barras))
    ]
    carga_reativa = [float(tipo_barras.iloc[i]["LOAD (MVAR)"]) / 100 for i in range(len(tipo_barras))]  # Vetor de carga reativa

    # Iterações
    while (erro > erro_max) and (contador < K_max):  # Loop principal de iteração até atingir o erro máximo ou o número máximo de iterações
        vetor_tensao_antiga = vetor_tensao.copy()  # Salva o vetor de tensão da iteração anterior
        contador += 1  # Incrementa o contador de iterações
        erro = 0  # Reseta o erro

        for k in range(len(tipo_barras)):  # Itera sobre todas as barras
            if tipo_barras.index[k] == 1:  # Barra Slack
                continue  # Pula a barra slack

            YV = sum(matriz_admt.iloc[k, n] * vetor_tensao[n] for n in range(len(tipo_barras)) if k != n)  # Calcula a soma das admitâncias vezes as tensões das outras barras

            if tipo_barras.index[k] == 0:  # Barra PQ
                try:
                    vetor_tensao[k] = (1 / matriz_admt.iloc[k, k]) *e1* (  # Atualiza a tensão da barra PQ
                        (vetor_pot_ativa[k] + 1j * vetor_pot_reativa[k]) / vetor_tensao[k].conjugate() - YV
                    )
                except ZeroDivisionError:  # Trata divisão por zero
                    vetor_tensao[k] = vetor_tensao_antiga[k]  # Mantém o valor anterior

            elif tipo_barras.index[k] == 2:  # Barra PV
                try:
                    Q_calc = -np.imag(vetor_tensao[k].conjugate() * (YV + matriz_admt.iloc[k, k] * vetor_tensao[k]))  # Calcula a potência reativa
                    Q_liq = Q_calc - carga_reativa[k]  # Calcula a potência reativa líquida

                    vetor_tensao[k] = (1 / matriz_admt.iloc[k, k]) *e2* (  # Atualiza a tensão da barra PV
                        (vetor_pot_ativa[k] + 1j * Q_liq) / vetor_tensao[k].conjugate() - YV
                    )
                    vetor_tensao[k] = abs(vetor_tensao_antiga[k]) * (vetor_tensao[k] / abs(vetor_tensao[k]))  # Ajusta o módulo da tensão
                except ZeroDivisionError:  # Trata divisão por zero
                    vetor_tensao[k] = vetor_tensao_antiga[k]  # Mantém o valor anterior

            erro = max(erro, abs(vetor_tensao[k] - vetor_tensao_antiga[k]))  # Atualiza o erro máximo da iteração

    return vetor_tensao, contador, erro  # Retorna o vetor de tensões, número de iterações e erro final