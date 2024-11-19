import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Função para calcular a pontuação com base na posição "Posição"
def calcular_pontos(posicao, kills):
    # Definindo a pontuação de acordo com a "Posição"
    pontuacoes = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1}
    
    # Se a "Posição" estiver entre 1 e 10, usamos a pontuação, caso contrário, 0 pontos
    pontos = pontuacoes.get(posicao, 0)
    
    # A pontuação total será a soma de pontos + kills
    return pontos + kills

# Função para abrir o gerenciador de arquivos e selecionar o arquivo CSV
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")))
    return arquivo

# Função principal
def processar_csv():
    # Solicitar o arquivo CSV ao usuário
    arquivo_csv = selecionar_arquivo()

    # Verifica se um arquivo foi selecionado
    if not arquivo_csv:
        print("Nenhum arquivo selecionado. O programa será encerrado.")
        return

    # Carregar o arquivo CSV usando pandas
    try:
        df = pd.read_csv(arquivo_csv)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    # Verificar se as colunas necessárias estão presentes no CSV
    if not all(col in df.columns for col in ['Win Place', 'Name', 'Kills']):
        print("Erro: O arquivo CSV não contém as colunas necessárias ('Win Place', 'Name', 'Kills').")
        return

    # Renomear as colunas para os nomes em português
    df.rename(columns={'Win Place': 'Posição', 'Name': 'Jogador'}, inplace=True)

    # Calcular a coluna "Pontos"
    df['Pontos'] = df.apply(lambda row: calcular_pontos(row['Posição'], row['Kills']), axis=1)

    # Selecionar as colunas que serão salvas
    df_resultado = df[['Posição', 'Jogador', 'Kills', 'Pontos']]

    # Solicitar o caminho para salvar o arquivo resultante
    arquivo_saida = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")], title="Salvar arquivo como")

    # Verificar se um caminho foi fornecido
    if not arquivo_saida:
        print("Nenhum local para salvar o arquivo foi selecionado.")
        return

    # Salvar o resultado no arquivo CSV
    try:
        df_resultado.to_csv(arquivo_saida, index=False)
        print(f"Arquivo CSV salvo com sucesso em: {arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")

if __name__ == "__main__":
    processar_csv()
