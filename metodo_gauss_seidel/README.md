# PowerFlow Solver (Fluxo de Carga)
## 📌 Visão Geral
Este projeto implementa um solver de fluxo de carga para sistemas elétricos de potência utilizando o método iterativo Gauss-Seidel. Desenvolvido em Python, ele calcula tensões nas barras, fluxos de potência e perdas nas linhas a partir de dados de entrada em arquivos Excel.

## 📋 Requisitos
Python 3.8+

Bibliotecas listadas em requirements.txt

## 🛠 Instalação
Clone o repositório:

bash

git clone https://github.com/ateniltonjr/SEP.git

cd powerflow-solver

Crie e ative um ambiente virtual (recomendado):

bash

python -m venv venv

source venv/bin/activate  # Linux/Mac

.\venv\Scripts\activate  # Windows

Instale as dependências:

bash

pip install -r requirements.txt

## 🏗 Estrutura do Projeto
powerflow_solver/

data/   # Arquivos de entrada

    Matriz Admitância.xlsx

    Barras.xlsx

    impedância.xlsx

lib/                      # Módulos do projeto
    __init__.py

    file_reader.py        # Leitura de arquivos

    gauss_seidel.py       # Método numérico
    
    power_calculations.py # Cálculos de potência

    utils.py              # Funções auxiliares

    main.py               # Script principal

    requirements.txt      # Dependências

## 📊 Entrada de Dados
Prepare três arquivos Excel na pasta data/:

Matriz Admitância.xlsx: Matriz Ybus do sistema

Barras.xlsx: Dados das barras (slack, PV, PQ)

impedância.xlsx: Dados das linhas (resistência e reatância)

## ▶️ Execução

bash

python main.py

## 📈 Saída do Programa

### O programa gera:

- Tensões nas barras (módulo e ângulo)
- Fluxos de potência ativa e reativa nas linhas
- Perdas totais no sistema
- Número de iterações e tempo de execução

## 🧪 Exemplo de Saída
### Tensões nas barras:

Barra 1: 1.000+0.000j pu | 1.000 pu ∠ 0.000°

Barra 2: 0.982-0.035j pu | 0.983 pu ∠ -2.050°

...

### Fluxos nas linhas:

Linha 1-2: P = 125.32 MW | Q = 45.67 MVar

...

### Perdas totais:

P = 5.4321 MW

Q = 12.8765 MVar

## 🛠 Melhorias Futuras

Interface gráfica para entrada de dados

Visualização da rede elétrica

Exportação de relatórios em PDF
