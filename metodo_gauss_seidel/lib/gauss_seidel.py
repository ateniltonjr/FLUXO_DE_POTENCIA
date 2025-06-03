import numpy as np
from .utils import str_to_complex

def solve_power_flow(matriz_admt, tipo_barras, impedancias, erro_max=1e-6, K_max=1000):
    """Resolve o fluxo de carga pelo método Gauss-Seidel"""
    contador = 0
    erro = 1
    
    # Preparação dos vetores
    vetor_tensao = [str_to_complex(val) for val in tipo_barras["VOLTAGE MAGNITUDE"]]
    vetor_pot_ativa = [
        (float(tipo_barras.iloc[i]["GENERATOR (MW)"]) - float(tipo_barras.iloc[i]["LOAD (MW)"])) / 100
        for i in range(len(tipo_barras))
    ]
    vetor_pot_reativa = [
        (float(tipo_barras.iloc[i]["GENERATOR (MVAR)"]) - float(tipo_barras.iloc[i]["LOAD (MVAR)"])) / 100
        for i in range(len(tipo_barras))
    ]
    carga_reativa = [float(tipo_barras.iloc[i]["LOAD (MVAR)"]) / 100 for i in range(len(tipo_barras))]
    
    # Iterações
    while (erro > erro_max) and (contador < K_max):
        vetor_tensao_antiga = vetor_tensao.copy()
        contador += 1
        erro = 0

        for k in range(len(tipo_barras)):
            if tipo_barras.index[k] == 1:  # Barra Slack
                continue

            YV = sum(matriz_admt.iloc[k, n] * vetor_tensao[n] for n in range(len(tipo_barras)) if k != n)

            if tipo_barras.index[k] == 0:  # Barra PQ
                try:
                    vetor_tensao[k] = (1 / matriz_admt.iloc[k, k]) * (
                        (vetor_pot_ativa[k] + 1j * vetor_pot_reativa[k]) / vetor_tensao[k].conjugate() - YV
                    )
                except ZeroDivisionError:
                    vetor_tensao[k] = vetor_tensao_antiga[k]

            elif tipo_barras.index[k] == 2:  # Barra PV
                try:
                    Q_calc = -np.imag(vetor_tensao[k].conjugate() * (YV + matriz_admt.iloc[k, k] * vetor_tensao[k]))
                    Q_liq = Q_calc - carga_reativa[k]

                    vetor_tensao[k] = (1 / matriz_admt.iloc[k, k]) * (
                        (vetor_pot_ativa[k] + 1j * Q_liq) / vetor_tensao[k].conjugate() - YV
                    )
                    vetor_tensao[k] = abs(vetor_tensao_antiga[k]) * (vetor_tensao[k] / abs(vetor_tensao[k]))
                except ZeroDivisionError:
                    vetor_tensao[k] = vetor_tensao_antiga[k]

            erro = max(erro, abs(vetor_tensao[k] - vetor_tensao_antiga[k]))

    return vetor_tensao, contador, erro