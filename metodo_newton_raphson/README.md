# Fluxo de Carga pelo Método de Newton-Raphson

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Power Systems](https://img.shields.io/badge/Power-Systems-orange)

Um solucionador de fluxo de potência para sistemas elétricos utilizando o método numérico de Newton-Raphson.

## 📋 Descrição

Este projeto implementa um algoritmo para cálculo do fluxo de potência em sistemas elétricos de potência, capaz de:
- Modelar barras PV, PQ e Slack
- Calcular tensões nas barras e fluxos nas linhas
- Determinar perdas no sistema
- Visualizar a convergência do método

## 📦 Estrutura do Projeto
metodo_newton_rapshon/
    powerflow1.py    # Classe principal NR com a implementação do método

    main1.py         # Script de exemplo com caso de teste

    README.md        # Este arquivo

    requirements.txt # Dependências do projeto


## ⚙️ Instalação

Clone o repositório:

bash

git clone https://github.com/ateniltonjr/SEP.git

cd metodo_newton_rapshon

Instale as dependências:

bash

pip install -r requirements.txt

## 🚀 Como Usar

Configure seu caso no arquivo main1.py:

python

from powerflow1 import NR

## Cria objeto Grid
Grid = NR()

# Adiciona barras (Slack, PV, PQ)
Grid.setBarras(1, 1, 1.06, 0.0, carga, geracao)  # Slack

Grid.setBarras(2, 3, 1.045, 0.0, carga, geracao)  # PV

Grid.setBarras(3, 2, 1.0, 0.0, carga, geracao)    # PQ

## Configura ligações entre barras
Grid.setLigacoes(1, 2, impedancia=0.01938+0.05914j)

Execute o fluxo de carga:

bash

python main1.py

## 📊 Saídas do Programa

- Matriz admitância do sistema
- Potências especificadas por barra
- Resíduos em cada iteração
- Tensões e ângulos finais
- Fluxos de potência nas linhas
- Perdas totais do sistema

## 🛠️ Dependências

- Python 3.8+
- NumPy
- SciPy

## 📌 Exemplo de Caso de Teste
- O arquivo main1.py inclui um caso teste com 14 barras do IEEE. Para executar:
- bash
- python main1.py

## 📈 Resultados Esperados

Exemplo de Saída Gráfica

## 🤝 Contribuições
Contribuições são bem-vindas! Siga estes passos:

Faça um fork do projeto

Crie sua branch (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Adiciona nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request
