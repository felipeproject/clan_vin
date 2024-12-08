import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Função para selecionar a pasta
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    return pasta

# Função para atribuir pontos com base na posição e kills
def calcular_pontos(rank, kills):
    # Pontuação fixa por posição
    pontuacao_por_rank = {1: 10, 2: 8, 3: 5, 4: 3, 5: 1}
    
    # Pega a pontuação pela classificação (rank), se não estiver no dicionário, assume 0 pontos
    pontos_rank = pontuacao_por_rank.get(rank, 0)
    
    # Cada kill soma 1 ponto extra
    pontos_kills = kills
    
    # Total de pontos
    total_pontos = pontos_rank + pontos_kills
    return total_pontos

# Função para formatar o ranking
def formatar_rank(rank):
    if rank == 1:
        return "1º"
    elif rank == 2:
        return "2º"
    elif rank == 3:
        return "3º"
    else:
        return f"{rank}º"

# Função para processar cada arquivo CSV e extrair os dados
def exibir_tabelas():
    # Inicializa a janela do Tkinter (não será exibida)
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Chama a função para selecionar a pasta
    pasta = selecionar_pasta()

    # Verifica se o usuário selecionou uma pasta
    if pasta:
        # Encontra todos os arquivos CSV na pasta selecionada
        arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

        # Se houver arquivos CSV, processa cada um deles
        if arquivos_csv:
            for arquivo_csv in arquivos_csv:
                caminho_arquivo = os.path.join(pasta, arquivo_csv)

                try:
                    # Lê o arquivo CSV no DataFrame
                    df = pd.read_csv(caminho_arquivo)

                    # Definir as colunas para exibição
                    columns = ["Win Place", "Kills", "Team Name"]

                    # Verifica se as colunas existem no arquivo CSV
                    if all(col in df.columns for col in columns):
                        # Remove as linhas com valores NaN nas colunas de interesse
                        df_cleaned = df[columns].dropna()

                        # Agrupa os dados pelo nome do time e soma as kills
                        grouped_df = df_cleaned.groupby("Team Name", as_index=False).agg(
                            {'Kills': 'sum', 'Win Place': 'first'}
                        )

                        # Remove o prefixo numérico (ex: "1-", "2-") dos nomes dos times
                        grouped_df["Team Name"] = grouped_df["Team Name"].str.replace(r'^\d+-', '', regex=True)

                        # Reorganiza a ordem das colunas para "Win Place", "Team Name", "Kills"
                        grouped_df = grouped_df[['Win Place', 'Team Name', 'Kills']]

                        # Renomeia as colunas para "RANK", "TIME", "KILLS"
                        grouped_df = grouped_df.rename(columns={
                            'Win Place': 'RANK',
                            'Team Name': 'TIME',
                            'Kills': 'KILLS'
                        })

                        # Converte a coluna RANK para numérico (se necessário)
                        grouped_df['RANK'] = pd.to_numeric(grouped_df['RANK'], errors='coerce')

                        # Adiciona a coluna de Pontuação (com base no rank e nas kills)
                        grouped_df['PONTOS'] = grouped_df.apply(lambda row: calcular_pontos(row['RANK'], row['KILLS']), axis=1)

                        # Exibe a tabela do arquivo CSV atual
                        print(f"\nTabela para o arquivo: {arquivo_csv}")
                        print(grouped_df[['RANK', 'TIME', 'KILLS', 'PONTOS']].to_string(index=False))

                    else:
                        print(f"As colunas {columns} não estão presentes no arquivo {arquivo_csv}.")
                except Exception as e:
                    print(f"Ocorreu um erro ao processar o arquivo {arquivo_csv}: {e}")
            
        else:
            print("Não há arquivos CSV na pasta selecionada.")
    else:
        print("Nenhuma pasta selecionada.")

# Chama a função para exibir as tabelas
exibir_tabelas()
