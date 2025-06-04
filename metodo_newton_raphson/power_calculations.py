import numpy as np  # Importa a biblioteca NumPy para operações numéricas

def calculate_power_flows(vetor_tensao, matriz_admt, tipo_barras, impedancias):
    P_gerada = np.zeros(len(tipo_barras))  # Inicializa vetor de potência ativa gerada
    Q_gerada = np.zeros(len(tipo_barras))  # Inicializa vetor de potência reativa gerada
    P_consumida = [float(tipo_barras.iloc[i]["LOAD (MW)"]) / 100 for i in range(len(tipo_barras))]  # Potência ativa consumida
    Q_consumida = [float(tipo_barras.iloc[i]["LOAD (MVAR)"]) / 100 for i in range(len(tipo_barras))]  # Potência reativa consumida

    for i in range(len(tipo_barras)):
        I_injetada = np.dot(matriz_admt.iloc[i, :], vetor_tensao)  # Calcula corrente injetada na barra i
        S_injetada = vetor_tensao[i] * np.conj(I_injetada)  # Calcula potência complexa injetada
        P_gerada[i] = np.real(S_injetada) + P_consumida[i]  # Potência ativa gerada na barra i
        Q_gerada[i] = -np.imag(S_injetada) + Q_consumida[i]  # Potência reativa gerada na barra i

    vetor_de = [int(impedancias.iloc[i]["DE"]) - 1 for i in range(len(impedancias))]  # Vetor de barras de origem das linhas
    vetor_para = [int(impedancias.iloc[i]["PARA"]) - 1 for i in range(len(impedancias))]  # Vetor de barras de destino das linhas
    vetor_resistencia = [float(impedancias.iloc[i]["RESISTÊNCIA"]) for i in range(len(impedancias))]  # Vetor de resistências das linhas
    vetor_reatancia = [float(impedancias.iloc[i]["REATÂNCIA"]) for i in range(len(impedancias))]  # Vetor de reatâncias das linhas

    potencia_ativa = np.zeros(len(impedancias))  # Inicializa vetor de fluxos ativos nas linhas
    potencia_reativa = np.zeros(len(impedancias))  # Inicializa vetor de fluxos reativos nas linhas
    perdas_ativas = np.zeros(len(impedancias))  # Inicializa vetor de perdas ativas nas linhas
    perdas_reativas = np.zeros(len(impedancias))  # Inicializa vetor de perdas reativas nas linhas

    for i in range(len(impedancias)):
        de = vetor_de[i]  # Índice da barra de origem
        para = vetor_para[i]  # Índice da barra de destino
        Z = vetor_resistencia[i] + 1j * vetor_reatancia[i]  # Impedância da linha
        I = (vetor_tensao[de] - vetor_tensao[para]) / Z  # Corrente na linha
        potencia_ativa[i] = np.real(vetor_tensao[de] * np.conj(I))  # Fluxo ativo na linha
        potencia_reativa[i] = np.imag(vetor_tensao[de] * np.conj(I))  # Fluxo reativo na linha
        perdas_ativas[i] = (np.real(I)**2 + np.imag(I)**2) * vetor_resistencia[i]  # Perda ativa na linha
        perdas_reativas[i] = (np.real(I)**2 + np.imag(I)**2) * vetor_reatancia[i]  # Perda reativa na linha

    return {
        'P_gerada': P_gerada,  # Potências ativas geradas nas barras
        'Q_gerada': Q_gerada,  # Potências reativas geradas nas barras
        'fluxos_ativos': potencia_ativa,  # Fluxos ativos nas linhas
        'fluxos_reativos': potencia_reativa,  # Fluxos reativos nas linhas
        'perdas_ativas': perdas_ativas,  # Perdas ativas nas linhas
        'perdas_reativas': perdas_reativas  # Perdas reativas nas linhas
    }
