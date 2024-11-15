import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime, timedelta

# Função para calcular a pontuação posicional e a pontuação total
def calcular_pontuacao_posicional(row, posicao):
    # Sistema de pontuação baseado na posição
    pontos_posicao = {
        1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1
    }

    # Pontuação baseada na posição
    pontuacao_posicional = pontos_posicao.get(posicao, 0)  # Se a posição for acima de 10, recebe 0 pontos
    
    # Adicionar pontos pelas kills (1 ponto por kill)
    total = pontuacao_posicional + row['Kills']
    
    return pontuacao_posicional, total

# Função para gerar o novo nome do arquivo (sem conversão de horário)
def gerar_nome_arquivo(arquivo_original):
    try:
        # Extrair o horário UTC do nome original
        parte_nome, utc_time_str = arquivo_original.split("t")
        utc_time_str = utc_time_str.replace("+00_00.csv", "")
    
        # Criar o novo nome do arquivo
        nome_map = parte_nome.split("-")[0].capitalize()  # Mapa (ex: Miramar)
        nome_jogo = "_".join(parte_nome.split("-")[1:]).replace("-", "_")
        novo_nome = f"{nome_map}_{nome_jogo}_{utc_time_str.replace('_', 'h').replace(' ', '')}_UTC.csv"
        return novo_nome
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o nome do arquivo: {e}")
        return None

# Função para extrair as colunas desejadas e calcular a pontuação
def extrair_colunas_csv(caminho_entrada, caminho_saida):
    try:
        # Carregar o arquivo CSV
        df = pd.read_csv(caminho_entrada)
        
        # Verificar se as colunas essenciais existem no CSV
        colunas_desejadas = ["Name", "Win Place", "Kills"]
        if not all(coluna in df.columns for coluna in colunas_desejadas):
            messagebox.showerror("Erro", "As colunas 'Name', 'Win Place' e 'Kills' não estão presentes no CSV.")
            return
        
        # Ordenar os jogadores pela posição (classificação)
        df.sort_values(by='Win Place', ascending=True, inplace=True)
        
        # Calcular a pontuação posicional e a pontuação total para cada jogador
        df['Pontuação Posicional'], df['Total'] = zip(*df.apply(lambda row: calcular_pontuacao_posicional(row, row['Win Place']), axis=1))

        # Criar uma coluna 'Rank' com base na posição
        df['Rank'] = df['Win Place'].apply(lambda x: f"#{x}")

        # Reorganizar as colunas conforme o formato solicitado
        df = df[["Rank", "Name", "Kills", "Pontuação Posicional", "Total"]]

        # Gerar o novo nome do arquivo
        nome_arquivo = os.path.basename(caminho_entrada)
        nome_arquivo_novo = gerar_nome_arquivo(nome_arquivo)

        if nome_arquivo_novo is None:
            return

        # Caminho de saída com o novo nome do arquivo
        caminho_saida_arquivo = os.path.join(caminho_saida, nome_arquivo_novo)
        df.to_csv(caminho_saida_arquivo, index=False)

        messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo_novo}' formatado e pontuado com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}")

# Função para listar os arquivos CSV na pasta
def listar_arquivos_csv():
    # Caminho da pasta
    pasta_csv = './partidas_csv'
    
    # Listar arquivos CSV na pasta
    if not os.path.exists(pasta_csv):
        os.makedirs(pasta_csv)

    arquivos_csv = [f for f in os.listdir(pasta_csv) if f.endswith('.csv')]
    return arquivos_csv

# Função para processar o arquivo selecionado
def processar_arquivo_selecionado(nome_arquivo):
    # Caminho completo do arquivo selecionado
    caminho_entrada = os.path.join('./partidas_csv', nome_arquivo)

    # Criar a pasta de saída /partidas_csv_formatadas, caso não exista
    caminho_saida = './partidas_csv_formatadas'
    if not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida)

    # Processar o arquivo CSV selecionado
    extrair_colunas_csv(caminho_entrada, caminho_saida)

# Função para atualizar a lista de arquivos na interface gráfica
def atualizar_lista_arquivos():
    arquivos_csv = listar_arquivos_csv()

    # Limpar a lista atual de arquivos
    lista_arquivos.delete(0, tk.END)

    # Adicionar novos arquivos CSV à lista
    for arquivo in arquivos_csv:
        lista_arquivos.insert(tk.END, arquivo)

# Criar a interface gráfica
def criar_interface():
    global lista_arquivos
    
    # Janela principal
    root = tk.Tk()
    root.title("Escolher e Processar Arquivo CSV")
    root.geometry("500x300")
    
    # Instrução para o usuário
    label_instrucoes = tk.Label(root, text="Escolha um arquivo CSV da lista abaixo para formatar", padx=10, pady=10)
    label_instrucoes.pack()

    # Lista de arquivos CSV na pasta
    lista_arquivos = tk.Listbox(root, height=10, width=50)
    lista_arquivos.pack(padx=10, pady=10)

    # Botão para atualizar a lista de arquivos
    botao_atualizar = tk.Button(root, text="Atualizar Lista", command=atualizar_lista_arquivos, padx=10, pady=10)
    botao_atualizar.pack()

    # Função para selecionar e processar o arquivo escolhido
    def selecionar_arquivo():
        try:
            # Obter o arquivo selecionado
            indice_selecionado = lista_arquivos.curselection()
            if not indice_selecionado:
                messagebox.showerror("Erro", "Por favor, selecione um arquivo da lista.")
                return
            nome_arquivo = lista_arquivos.get(indice_selecionado[0])
            
            # Processar o arquivo
            processar_arquivo_selecionado(nome_arquivo)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    # Botão para processar o arquivo selecionado
    botao_processar = tk.Button(root, text="Processar Arquivo Selecionado", command=selecionar_arquivo, padx=10, pady=10)
    botao_processar.pack()

    # Inicializar a lista de arquivos
    atualizar_lista_arquivos()

    # Iniciar a interface gráfica
    root.mainloop()

# Iniciar o aplicativo
if __name__ == "__main__":
    criar_interface()
