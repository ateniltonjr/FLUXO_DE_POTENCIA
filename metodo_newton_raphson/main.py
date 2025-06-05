import time # Importa módulo time para medir tempo de execução
import numpy as np # Importa a biblioteca NumPy para operações numéricas
import pandas as pd # Importa a biblioteca Pandas para manipulação de dados

def str_to_complex(val):
    """Converte string para número complexo com tratamento de erro"""
    try:
        s = str(val).strip().replace(",", ".").replace("i", "j") # Ajusta formato para número complexo Python
        if not s or s == 'nan' or s == 'None':
            return 0 + 0j # Retorna zero se valor inválido
        return complex(s) # Converte para número complexo
    except (ValueError, AttributeError):
        return 0 + 0j # Retorna zero em caso de erro

def format_complex(z):
    """Formata número complexo para impressão"""
    return f"{z.real:.3f}{'+' if z.imag >= 0 else ''}{z.imag:.3f}j" # Formata parte real e imaginária

def print_matrix(matrix, name="Matriz"):
    """Imprime matriz formatada"""
    print(f"\n{name.upper()}:")
    print("Barra\t" + "\t".join([f"{col+1}" for col in range(matrix.shape[1])])) # Cabeçalho
    for i in range(matrix.shape[0]):
        linha = [format_complex(matrix.iloc[i, j]) for j in range(matrix.shape[1])] # Formata cada elemento
        print(f"{i+1}\t" + "\t".join(linha)) # Imprime linha

def load_admittance_matrix(filepath):  # Define função para carregar matriz de admitância
    """Carrega a matriz de admitância"""
    try:
        matriz = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        for i in range(matriz.shape[0]):  # Itera sobre as linhas da matriz
            for j in range(matriz.shape[1]):  # Itera sobre as colunas da matriz
                matriz.iloc[i, j] = str_to_complex(matriz.iloc[i, j])  # Converte cada elemento para número complexo
        return matriz  # Retorna a matriz carregada
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar matriz de admitância: {e}")  # Lança exceção personalizada

def load_bus_data(filepath):  # Define função para carregar dados das barras
    """Carrega dados das barras"""
    try:
        dados = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        return dados  # Retorna os dados carregados
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar dados das barras: {e}")  # Lança exceção personalizada

def load_impedance_data(filepath):  # Define função para carregar dados de impedância
    """Carrega dados de impedância"""
    try:
        dados = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        return dados  # Retorna os dados carregados
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar dados de impedância: {e}")  # Lança exceção personalizada

from power_calculations import calculate_power_flows # Importa função de cálculo de fluxo de potência

def newton_raphson_power_flow(Ybus, bus_data, max_iter=30, tol=1e-6, damping=1.0):
    n = len(bus_data) # Número de barras
    # Inicialização correta do vetor de tensão
    V = np.array([float(v) for v in bus_data["VOLTAGE MAGNITUDE"]]) # Vetor de módulos de tensão
    theta = np.zeros(n) # Vetor de ângulos de tensão inicializados em zero
    P = (bus_data["GENERATOR (MW)"] - bus_data["LOAD (MW)"]).values / 100 # Vetor de potências ativas líquidas (pu)
    Q = (bus_data["GENERATOR (MVAR)"] - bus_data["LOAD (MVAR)"]).values / 100 # Vetor de potências reativas líquidas (pu)
    tipo = bus_data["TIPO DE BARRA"].values if "TIPO DE BARRA" in bus_data.columns else bus_data.index.values # Tipos de barra
    slack_idx = np.where(tipo == 1)[0][0] # Índice da barra slack
    PV_idx = np.where(tipo == 2)[0] # Índices das barras PV
    PQ_idx = np.where(tipo == 0)[0] # Índices das barras PQ
    var_theta = np.concatenate([PQ_idx, PV_idx]) # Variáveis de ângulo (exceto slack)
    var_V = PQ_idx # Variáveis de módulo (apenas PQ)
    n_theta = len(var_theta) # Número de variáveis de ângulo
    n_V = len(var_V) # Número de variáveis de módulo
    for it in range(max_iter): # Loop de iterações
        P_calc = np.zeros(n) # Potências ativas calculadas
        Q_calc = np.zeros(n) # Potências reativas calculadas
        for i in range(n):
            for k in range(n):
                P_calc[i] += V[i]*V[k]*(Ybus.iloc[i,k].real*np.cos(theta[i]-theta[k]) + Ybus.iloc[i,k].imag*np.sin(theta[i]-theta[k])) # Calcula P
                Q_calc[i] += V[i]*V[k]*(Ybus.iloc[i,k].real*np.sin(theta[i]-theta[k]) - Ybus.iloc[i,k].imag*np.cos(theta[i]-theta[k])) # Calcula Q
        dP = P[np.concatenate([PQ_idx, PV_idx])] - P_calc[np.concatenate([PQ_idx, PV_idx])] # Mismatch de P
        dQ = Q[PQ_idx] - Q_calc[PQ_idx] # Mismatch de Q
        mismatch = np.concatenate([dP, dQ]) # Vetor de mismatches
        if np.max(np.abs(mismatch)) < tol: # Critério de convergência
            break
        # Jacobiana
        J = np.zeros((n_theta + n_V, n_theta + n_V)) # Inicializa Jacobiana
        # dP/dTheta e dP/dV
        for i, idx_i in enumerate(var_theta):
            for j, idx_j in enumerate(var_theta):
                if idx_i == idx_j:
                    J[i, j] = -Q_calc[idx_i] - V[idx_i]**2 * Ybus.iloc[idx_i, idx_i].imag # Derivada diagonal
                else:
                    J[i, j] = V[idx_i]*V[idx_j]*(Ybus.iloc[idx_i, idx_j].real*np.sin(theta[idx_i]-theta[idx_j]) - Ybus.iloc[idx_i, idx_j].imag*np.cos(theta[idx_i]-theta[idx_j])) # Derivada fora da diagonal
        for i, idx_i in enumerate(var_theta):
            for j, idx_j in enumerate(var_V):
                if idx_i == idx_j:
                    J[i, n_theta + j] = P_calc[idx_i]/V[idx_i] + V[idx_i]*Ybus.iloc[idx_i, idx_i].real # Derivada diagonal
                else:
                    J[i, n_theta + j] = V[idx_i]*(Ybus.iloc[idx_i, idx_j].real*np.cos(theta[idx_i]-theta[idx_j]) + Ybus.iloc[idx_i, idx_j].imag*np.sin(theta[idx_i]-theta[idx_j])) # Derivada fora da diagonal
        # dQ/dTheta e dQ/dV
        for i, idx_i in enumerate(var_V):
            for j, idx_j in enumerate(var_theta):
                if idx_i == idx_j:
                    J[n_theta + i, j] = P_calc[idx_i] - V[idx_i]**2 * Ybus.iloc[idx_i, idx_i].real # Derivada diagonal
                else:
                    J[n_theta + i, j] = -V[idx_i]*V[idx_j]*(Ybus.iloc[idx_i, idx_j].real*np.cos(theta[idx_i]-theta[idx_j]) + Ybus.iloc[idx_i, idx_j].imag*np.sin(theta[idx_i]-theta[idx_j])) # Derivada fora da diagonal
        for i, idx_i in enumerate(var_V):
            for j, idx_j in enumerate(var_V):
                if idx_i == idx_j:
                    J[n_theta + i, n_theta + j] = Q_calc[idx_i]/V[idx_i] - V[idx_i]*Ybus.iloc[idx_i, idx_i].imag # Derivada diagonal
                else:
                    J[n_theta + i, n_theta + j] = V[idx_i]*(Ybus.iloc[idx_i, idx_j].real*np.sin(theta[idx_i]-theta[idx_j]) - Ybus.iloc[idx_i, idx_j].imag*np.cos(theta[idx_i]-theta[idx_j])) # Derivada fora da diagonal
        dx = np.linalg.solve(J, mismatch) # Resolve sistema linear
        # Fator de relaxação para evitar saltos grandes
        theta[var_theta] += damping * dx[:n_theta] # Atualiza ângulos
        V[var_V] += damping * dx[n_theta:] # Atualiza módulos
        # Limita as tensões PQ para o intervalo físico
        V[var_V] = np.clip(V[var_V], 0.9, 1.1)
    return V * np.exp(1j*theta), it+1, np.max(np.abs(mismatch)) # Retorna tensões, número de iterações e erro final

def main():
    start_time = time.time() # Marca tempo inicial
    try:
        matriz_admt = load_admittance_matrix("dados_excel/Matriz Admitância.xlsx") # Carrega matriz de admitância
        tipo_barras = load_bus_data("dados_excel/Barras.xlsx") # Carrega dados das barras
        impedancias = load_impedance_data("dados_excel/impedância.xlsx") # Carrega dados de impedâncias
    except Exception as e:
        print(f"\nErro: {e}") # Imprime erro de leitura
        return
    n_barras = len(tipo_barras) # Número de barras
    if matriz_admt.shape[0] != n_barras or matriz_admt.shape[1] != n_barras:
        print(f"\nErro: A matriz deve ser {n_barras}x{n_barras}") # Verifica dimensão da matriz
        return
    print("\nIniciando cálculo do fluxo de carga pelo método de Newton-Raphson...")
    try:
        vetor_tensao, iteracoes, erro = newton_raphson_power_flow(matriz_admt, tipo_barras) # Executa Newton-Raphson
    except NotImplementedError as e:
        print(e)
        return
    print(f"\nTempo de execução: {time.time() - start_time:.2f} segundos") # Tempo de execução
    print(f"\nConvergiu após {iteracoes} iterações com erro: {erro:.8f}") # Iterações e erro
    print("\nTensões nas barras:")
    for i, tensao in enumerate(vetor_tensao):
        print(f"Barra {i+1}: {format_complex(tensao)} pu | {abs(tensao):.3f} pu ∠ {np.degrees(np.angle(tensao)):.3f}°") # Imprime tensão em cada barra
    # Adicional: imprimir vetor de tensões em formato CSV para comparação
    print("\nVetor de tensões finais (CSV):")
    print("Barra | Modulo | Angulo_graus")
    for i, tensao in enumerate(vetor_tensao):
        print(f"     {i+1}, {abs(tensao):.4f},   {np.degrees(np.angle(tensao)):.4f}") # Imprime CSV
    resultados = calculate_power_flows(vetor_tensao, matriz_admt, tipo_barras, impedancias) # Calcula fluxos de potência
    print("\nPotências geradas:")
    for i in range(n_barras):
        print(f"Barra {i+1}: P = {resultados['P_gerada'][i]*100:.2f} MW | Q = {resultados['Q_gerada'][i]*100:.2f} MVar") # Imprime potências geradas
    print("\nFluxos nas linhas:")
    for i in range(len(impedancias)):
        de = int(impedancias.iloc[i]["DE"]) # Barra de origem
        para = int(impedancias.iloc[i]["PARA"]) # Barra de destino
        print(f"Linha {i+1} (Da Barra {de} para a Barra {para}): P = {resultados['fluxos_ativos'][i]*100:.2f} MW | Q = {resultados['fluxos_reativos'][i]*100:.2f} MVar | Perdas: {resultados['perdas_ativas'][i]*100:.2f} MW, {resultados['perdas_reativas'][i]*100:.2f} MVar") # Imprime fluxos e perdas
    print("\nPerdas totais de potência:")
    print(f"Perdas totais de P: {np.sum(resultados['perdas_ativas'])*100:.2f} MW") # Soma perdas ativas
    print(f"Perdas totais de Q: {np.sum(resultados['perdas_reativas'])*100:.2f} MVar") # Soma perdas reativas

if __name__ == "__main__":
    main() # Executa função principal
