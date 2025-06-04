import time  # Importa o módulo time para medir o tempo de execução
import numpy as np  # Importa o numpy para operações numéricas
from lib.file_reader import load_admittance_matrix, load_bus_data, load_impedance_data  # Funções para ler arquivos de dados
from lib.gauss_seidel import solve_power_flow  # Função para resolver o fluxo de potência pelo método de Gauss-Seidel
from lib.power_calculations import calculate_power_flows  # Função para calcular fluxos de potência
from lib.utils import format_complex  # Função utilitária para formatar números complexos

def main():
    start_time = time.time()  # Marca o tempo inicial
    
    # Carregar dados
    try:
        matriz_admt = load_admittance_matrix("dados_excel/Matriz Admitância.xlsx")  # Carrega a matriz de admitância
        tipo_barras = load_bus_data("dados_excel/Barras.xlsx")  # Carrega os dados das barras
        impedancias = load_impedance_data("dados_excel/impedância.xlsx")  # Carrega os dados de impedância das linhas
    except Exception as e:
        print(f"\nErro: {e}")  # Exibe erro caso algum arquivo não seja carregado corretamente
        return

    # Verificar consistência
    n_barras = len(tipo_barras)  # Número de barras
    if matriz_admt.shape[0] != n_barras or matriz_admt.shape[1] != n_barras:
        print(f"\nErro: A matriz deve ser {n_barras}x{n_barras}") # Verifica se a matriz de admitância é quadrada e compatível
        return

    # Resolver fluxo de carga
    print("\nIniciando cálculo do fluxo de carga...")
    vetor_tensao, iteracoes, erro = solve_power_flow(matriz_admt, tipo_barras, impedancias)  # Executa o método de Gauss-Seidel
    
    # Resultados
    print(f"\nTempo de execução: {time.time() - start_time:.2f} segundos")  # Exibe o tempo de execução
    print(f"\nConvergiu após {iteracoes} iterações com erro: {erro:.8f}")  # Exibe número de iterações e erro final

    # Tensões
    print("\nTensões nas barras:")
    for i, tensao in enumerate(vetor_tensao):
        print(f"Barra {i+1}: {format_complex(tensao)} pu | {abs(tensao):.3f} pu ∠ {np.degrees(np.angle(tensao)):.3f}°")  # Exibe tensão em cada barra
    # Adicional: imprimir vetor de tensões em formato CSV para comparação
    print("\nVetor de tensões finais (CSV):")
    print("Barra | Modulo | Angulo_graus")
    for i, tensao in enumerate(vetor_tensao):
        print(f"     {i+1}, {abs(tensao):.4f} , {np.degrees(np.angle(tensao)):.4f}")  # Exibe tensões em formato CSV

    # Cálculos de potência
    resultados = calculate_power_flows(vetor_tensao, matriz_admt, tipo_barras, impedancias)  # Calcula fluxos de potência

    # Potências geradas
    print("\nPotências geradas:")
    for i in range(n_barras):
        print(f"Barra {i+1}: P = {resultados['P_gerada'][i]*100:.2f} MW | Q = {resultados['Q_gerada'][i]*100:.2f} MVar")  # Exibe potência ativa e reativa gerada em cada barra
    print("\nFluxos nas linhas:")
    for i in range(len(impedancias)):
        de = int(impedancias.iloc[i]["DE"])  # Barra de origem
        para = int(impedancias.iloc[i]["PARA"])  # Barra de destino
        print(f"Linha {i+1} (Da Barra {de} para a Barra {para}): P = {resultados['fluxos_ativos'][i]*100:.2f} MW | Q = {resultados['fluxos_reativos'][i]*100:.2f} MVar | Perdas: {resultados['perdas_ativas'][i]*100:.2f} MW, {resultados['perdas_reativas'][i]*100:.2f} MVar")  # Exibe fluxos e perdas nas linhas
    print("\nPerdas totais de potência:")
    print(f"Perdas totais de P: {np.sum(resultados['perdas_ativas'])*100:.2f} MW")  # Exibe perdas totais de potência ativa
    print(f"Perdas totais de Q: {np.sum(resultados['perdas_reativas'])*100:.2f} MVar")  # Exibe perdas totais de potência reativa

if __name__ == "__main__":
    main()  # Executa a função principal se o script for chamado diretamente