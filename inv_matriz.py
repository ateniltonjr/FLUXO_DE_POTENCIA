import numpy as np

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de matriz complexa 4x4 genérica
    y = np.array([
        [-9.8j,       0j,      4j,     5j],
        [   0j,    -8.3j,    2.5j,     5j],
        [   4j,     2.5j,  -15.3j,     8j],
        [   5j,       5j,      8j,   -18j]
    ])
    I = np.array([
        [-1.2j],
        [-0.72-0.96j],
        [-1.2j],
        [0]
    ])
    
    print("Matriz original:")
    print(y)
    inv_y = np.linalg.inv(y)
    print("Matriz inversa:")
    np.set_printoptions(precision=2, suppress=True)   
    print(inv_y)
    # Verificação: produto deve ser a identidade
    print("As tensões nas barras são:")
    v = np.dot(inv_y, I)
    # Exibe o resultado com duas casas decimais
    np.set_printoptions(precision=2, suppress=True)
    print(v)
