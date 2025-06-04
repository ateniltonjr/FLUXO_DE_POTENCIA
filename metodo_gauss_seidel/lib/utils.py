import numpy as np

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