import pandas as pd  # Importa a biblioteca pandas para manipulação de dados em tabelas
from .utils import str_to_complex, print_matrix  # Importa funções auxiliares do módulo utils

def load_admittance_matrix(filepath):  # Define função para carregar matriz de admitância
    """Carrega a matriz de admitância"""
    try:
        matriz = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        for i in range(matriz.shape[0]):  # Itera sobre as linhas da matriz
            for j in range(matriz.shape[1]):  # Itera sobre as colunas da matriz
                matriz.iloc[i, j] = str_to_complex(matriz.iloc[i, j])  # Converte cada elemento para número complexo
        #print(f"Dimensões da matriz: {matriz.shape}")  # Exibe as dimensões da matriz
        #print_matrix(matriz, "Matriz de Admitância")  # Imprime a matriz formatada
        return matriz  # Retorna a matriz carregada
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar matriz de admitância: {e}")  # Lança exceção personalizada

def load_bus_data(filepath):  # Define função para carregar dados das barras
    """Carrega dados das barras"""
    try:
        dados = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        print("\nDados das barras carregados com sucesso!")  # Mensagem de sucesso
        return dados  # Retorna os dados carregados
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar dados das barras: {e}")  # Lança exceção personalizada

def load_impedance_data(filepath):  # Define função para carregar dados de impedância
    """Carrega dados de impedância"""
    try:
        dados = pd.read_excel(filepath, index_col=0, header=0)  # Lê arquivo Excel em um DataFrame, usando a primeira coluna como índice
        print("\nDados de impedância carregados com sucesso!")  # Mensagem de sucesso
        return dados  # Retorna os dados carregados
    except Exception as e:  # Captura exceções
        raise Exception(f"Erro ao carregar dados de impedância: {e}")  # Lança exceção personalizada
