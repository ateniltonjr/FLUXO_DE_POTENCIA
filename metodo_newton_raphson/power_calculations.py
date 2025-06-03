import numpy as np

def calculate_power_flows(vetor_tensao, matriz_admt, tipo_barras, impedancias):
    # ...existing code from metodo_gauss_seidel/lib/power_calculations.py...
    P_gerada = np.zeros(len(tipo_barras))
    Q_gerada = np.zeros(len(tipo_barras))
    P_consumida = [float(tipo_barras.iloc[i]["LOAD (MW)"]) / 100 for i in range(len(tipo_barras))]
    Q_consumida = [float(tipo_barras.iloc[i]["LOAD (MVAR)"]) / 100 for i in range(len(tipo_barras))]

    for i in range(len(tipo_barras)):
        I_injetada = np.dot(matriz_admt.iloc[i, :], vetor_tensao)
        S_injetada = vetor_tensao[i] * np.conj(I_injetada)
        P_gerada[i] = np.real(S_injetada) + P_consumida[i]
        Q_gerada[i] = -np.imag(S_injetada) + Q_consumida[i]

    vetor_de = [int(impedancias.iloc[i]["DE"]) - 1 for i in range(len(impedancias))]
    vetor_para = [int(impedancias.iloc[i]["PARA"]) - 1 for i in range(len(impedancias))]
    vetor_resistencia = [float(impedancias.iloc[i]["RESISTÊNCIA"]) for i in range(len(impedancias))]
    vetor_reatancia = [float(impedancias.iloc[i]["REATÂNCIA"]) for i in range(len(impedancias))]

    potencia_ativa = np.zeros(len(impedancias))
    potencia_reativa = np.zeros(len(impedancias))
    perdas_ativas = np.zeros(len(impedancias))
    perdas_reativas = np.zeros(len(impedancias))

    for i in range(len(impedancias)):
        de = vetor_de[i]
        para = vetor_para[i]
        Z = vetor_resistencia[i] + 1j * vetor_reatancia[i]
        I = (vetor_tensao[de] - vetor_tensao[para]) / Z
        potencia_ativa[i] = np.real(vetor_tensao[de] * np.conj(I))
        potencia_reativa[i] = np.imag(vetor_tensao[de] * np.conj(I))
        perdas_ativas[i] = (np.real(I)**2 + np.imag(I)**2) * vetor_resistencia[i]
        perdas_reativas[i] = (np.real(I)**2 + np.imag(I)**2) * vetor_reatancia[i]

    return {
        'P_gerada': P_gerada,
        'Q_gerada': Q_gerada,
        'fluxos_ativos': potencia_ativa,
        'fluxos_reativos': potencia_reativa,
        'perdas_ativas': perdas_ativas,
        'perdas_reativas': perdas_reativas
    }
