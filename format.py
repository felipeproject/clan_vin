import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Função para extrair as colunas desejadas
def extrair_colunas_csv(caminho_entrada, caminho_saida):
    try:
        # Carregar o arquivo CSV
        df = pd.read_csv(caminho_entrada)
        
        # Verificar se as colunas existem no CSV
        colunas_desejadas = ["Name", "Win Place", "Kills"]
        if all(coluna in df.columns for coluna in colunas_desejadas):
            # Selecionar apenas as colunas desejadas
            df_selecionado = df[colunas_desejadas]
            
            # Salvar o novo CSV na pasta de saída
            nome_arquivo = os.path.basename(caminho_entrada)
            caminho_saida_arquivo = os.path.join(caminho_saida, nome_arquivo)
            df_selecionado.to_csv(caminho_saida_arquivo, index=False)
            messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo}' formatado com sucesso!")
        else:
            messagebox.showerror("Erro", "As colunas 'Name', 'Win Place' e 'Kills' não estão presentes no CSV.")
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
