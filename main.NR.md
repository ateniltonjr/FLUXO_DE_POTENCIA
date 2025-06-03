import time
import numpy as np
import pandas as pd

def str_to_complex(val):
    """Converte string para número complexo com tratamento de erro"""
    try:
        s = str(val).strip().replace(",", ".").replace("i", "j")
        if not s or s == 'nan' or s == 'None':
            return 0 + 0j
        return complex(s)
    except (ValueError, AttributeError):
        return 0 + 0j
    
def format_complex(z):
    """Formata número complexo para impressão"""
    return f"{z.real:.3f}{'+' if z.imag >= 0 else ''}{z.imag:.3f}j"

def print_matrix(matrix, name="Matriz"):
    """Imprime matriz formatada"""
    print(f"\n{name.upper()}:")
    print("Barra\t" + "\t".join([f"{col+1}" for col in range(matrix.shape[1])]))
    for i in range(matrix.shape[0]):
        linha = [format_complex(matrix.iloc[i, j]) for j in range(matrix.shape[1])]
        print(f"{i+1}\t" + "\t".join(linha))

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

from power_calculations import calculate_power_flows

def newton_raphson_power_flow(Ybus, bus_data, max_iter=20, tol=1e-6):
    n = len(bus_data)
    V = np.array([float(v) for v in bus_data["VOLTAGE MAGNITUDE"]])
    theta = np.zeros(n)
    P = (bus_data["GENERATOR (MW)"] - bus_data["LOAD (MW)"]).values / 100
    Q = (bus_data["GENERATOR (MVAR)"] - bus_data["LOAD (MVAR)"]).values / 100
    tipo = bus_data["TIPO DE BARRA"].values if "TIPO DE BARRA" in bus_data.columns else bus_data.index.values
    slack_idx = np.where(tipo == 1)[0][0]
    PV_idx = np.where(tipo == 2)[0]
    PQ_idx = np.where(tipo == 0)[0]
    var_theta = np.concatenate([PQ_idx, PV_idx])
    var_V = PQ_idx
    n_theta = len(var_theta)
    n_V = len(var_V)
    for it in range(max_iter):
        P_calc = np.zeros(n)
        Q_calc = np.zeros(n)
        for i in range(n):
            for k in range(n):
                P_calc[i] += V[i]*V[k]*(Ybus.iloc[i,k].real*np.cos(theta[i]-theta[k]) + Ybus.iloc[i,k].imag*np.sin(theta[i]-theta[k]))
                Q_calc[i] += V[i]*V[k]*(Ybus.iloc[i,k].real*np.sin(theta[i]-theta[k]) - Ybus.iloc[i,k].imag*np.cos(theta[i]-theta[k]))
        dP = P[np.concatenate([PQ_idx, PV_idx])] - P_calc[np.concatenate([PQ_idx, PV_idx])]
        dQ = Q[PQ_idx] - Q_calc[PQ_idx]
        mismatch = np.concatenate([dP, dQ])
        if np.max(np.abs(mismatch)) < tol:
            break
        # Jacobiana
        J = np.zeros((n_theta + n_V, n_theta + n_V))
        # dP/dTheta e dP/dV
        for i, idx_i in enumerate(var_theta):
            for j, idx_j in enumerate(var_theta):
                if idx_i == idx_j:
                    J[i, j] = -Q_calc[idx_i] - V[idx_i]**2 * Ybus.iloc[idx_i, idx_i].imag
                else:
                    J[i, j] = V[idx_i]*V[idx_j]*(Ybus.iloc[idx_i, idx_j].real*np.sin(theta[idx_i]-theta[idx_j]) - Ybus.iloc[idx_i, idx_j].imag*np.cos(theta[idx_i]-theta[idx_j]))
        for i, idx_i in enumerate(var_theta):
            for j, idx_j in enumerate(var_V):
                if idx_i == idx_j:
                    J[i, n_theta + j] = P_calc[idx_i]/V[idx_i] + V[idx_i]*Ybus.iloc[idx_i, idx_i].real
                else:
                    J[i, n_theta + j] = V[idx_i]*(Ybus.iloc[idx_i, idx_j].real*np.cos(theta[idx_i]-theta[idx_j]) + Ybus.iloc[idx_i, idx_j].imag*np.sin(theta[idx_i]-theta[idx_j]))
        # dQ/dTheta e dQ/dV
        for i, idx_i in enumerate(var_V):
            for j, idx_j in enumerate(var_theta):
                if idx_i == idx_j:
                    J[n_theta + i, j] = P_calc[idx_i] - V[idx_i]**2 * Ybus.iloc[idx_i, idx_i].real
                else:
                    J[n_theta + i, j] = -V[idx_i]*V[idx_j]*(Ybus.iloc[idx_i, idx_j].real*np.cos(theta[idx_i]-theta[idx_j]) + Ybus.iloc[idx_i, idx_j].imag*np.sin(theta[idx_i]-theta[idx_j]))
        for i, idx_i in enumerate(var_V):
            for j, idx_j in enumerate(var_V):
                if idx_i == idx_j:
                    J[n_theta + i, n_theta + j] = Q_calc[idx_i]/V[idx_i] - V[idx_i]*Ybus.iloc[idx_i, idx_i].imag
                else:
                    J[n_theta + i, n_theta + j] = V[idx_i]*(Ybus.iloc[idx_i, idx_j].real*np.sin(theta[idx_i]-theta[idx_j]) - Ybus.iloc[idx_i, idx_j].imag*np.cos(theta[idx_i]-theta[idx_j]))
        dx = np.linalg.solve(J, mismatch)
        theta[var_theta] += dx[:n_theta]
        V[var_V] += dx[n_theta:]
    return V * np.exp(1j*theta), it+1, np.max(np.abs(mismatch))

def main():
    start_time = time.time()
    try:
        matriz_admt = load_admittance_matrix("metodo_newton_raphson/data/Matriz Admitância.xlsx")
        tipo_barras = load_bus_data("metodo_newton_raphson/data/Barras.xlsx")
        impedancias = load_impedance_data("metodo_newton_raphson/data/impedância.xlsx")
    except Exception as e:
        print(f"\nErro: {e}")
        return
    n_barras = len(tipo_barras)
    if matriz_admt.shape[0] != n_barras or matriz_admt.shape[1] != n_barras:
        print(f"\nErro: A matriz deve ser {n_barras}x{n_barras}")
        return
    print("\nIniciando cálculo do fluxo de carga pelo método de Newton-Raphson...")
    try:
        vetor_tensao, iteracoes, erro = newton_raphson_power_flow(matriz_admt, tipo_barras)
    except NotImplementedError as e:
        print(e)
        return
    print(f"\nTempo de execução: {time.time() - start_time:.2f} segundos")
    print(f"\nConvergiu após {iteracoes} iterações com erro: {erro:.8f}")
    print("\nTensões nas barras:")
    for i, tensao in enumerate(vetor_tensao):
        print(f"Barra {i+1}: {format_complex(tensao)} pu | {abs(tensao):.3f} pu ∠ {np.degrees(np.angle(tensao)):.3f}°")
    resultados = calculate_power_flows(vetor_tensao, matriz_admt, tipo_barras, impedancias)
    print("\nPotências geradas:")
    for i in range(n_barras):
        print(f"Barra {i+1}: P = {resultados['P_gerada'][i]*100:.2f} MW | Q = {resultados['Q_gerada'][i]*100:.2f} MVar")
    print("\nFluxos nas linhas:")
    for i in range(len(impedancias)):
        de = int(impedancias.iloc[i]["DE"])
        para = int(impedancias.iloc[i]["PARA"])
        print(f"Linha {i+1} (Barra {de} -> Barra {para}): P = {resultados['fluxos_ativos'][i]*100:.2f} MW | Q = {resultados['fluxos_reativos'][i]*100:.2f} MVar | Perdas: {resultados['perdas_ativas'][i]*100:.2f} MW, {resultados['perdas_reativas'][i]*100:.2f} MVar")
    print("\nPerdas totais:")
    print(f"Perdas totais de P: {np.sum(resultados['perdas_ativas'])*100:.2f} MW")
    print(f"Perdas totais de Q: {np.sum(resultados['perdas_reativas'])*100:.2f} MVar")

if __name__ == "__main__":
    main()
