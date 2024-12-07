import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import re
import os

# Mapeamento das traduções dos termos
traducoes = {
    "Name": "Nome",
    "Win Place": "Colocação na vitória",
    "Kill Place": "Colocação nas mortes",
    "Kills": "Kills (Mortes)",
    "Bot Kills": "Kills de bots",
    "Kill Streaks": "Sequências de kills",
    "Headshot Kills": "Kills de cabeça",
    "Damage Dealt": "Dano causado",
    "Assists": "Assistências",
    "Knocks": "Nocks (Jogadores derrubados)",
    "Heals": "Curativos",
    "Boosts": "Boosts (Aumentos de performance)",
    "Death Type": "Tipo de morte",
    "Revives": "Revives (Reanimações)",
    "Team Kills": "Kills de equipe",
    "Longest Kill": "Maior distância de kill",
    "Weapons Acquired": "Armas adquiridas",
    "Time Survived": "Tempo sobrevivido",
    "Distance Traveled": "Distância percorrida",
    "Walk Distance": "Distância percorrida a pé",
    "Ride Distance": "Distância percorrida de veículo",
    "Swim Distance": "Distância percorrida nadando",
    "Team Name": "Nome da equipe"
}

# Variável global para armazenar o caminho do arquivo carregado
caminho_arquivo = ""

# Função para arredondar os valores de dano
def arredondar_damage(valor):
    if isinstance(valor, (int, float)):
        return round(valor / 50) * 50
    return valor

# Função para extrair o número do nome da equipe
def extrair_numero_time(nome_time):
    match = re.match(r"^(\d+)-", nome_time)  # Captura o número no início do nome da equipe
    if match:
        return f"TEAM #{match.group(1)}"  # Retorna a string com o número da equipe
    return nome_time  # Caso não encontre, retorna o nome original

# Função para calcular os pontos
def calcular_pontos(row):
    # Pontos por posição
    pontos_posicao = {
        1: 10,
        2: 8,
        3: 5,
        4: 3,
        5: 1
    }
    pontos_posicao_total = pontos_posicao.get(row['Win Place'], 0)
    
    # Pontos por kills
    pontos_kills = row['Kills']
    
    # Total de pontos
    total_pontos = pontos_posicao_total + pontos_kills
    return total_pontos

def carregar_csv():
    global caminho_arquivo  # Definir o caminho_arquivo como global
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    if caminho_arquivo:
        try:
            global tabela_original  # Tornar a tabela disponível globalmente
            tabela_original = pd.read_csv(caminho_arquivo)
            
            colunas_para_remover = [
                "Bot Kills", "Longest Kill", "Weapons Acquired", "Time Survived",
                "Distance Traveled ", "Walk Distance ", "Ride Distance ", "Swim Distance ",
                "Kill Streaks", "Headshot Kills", "Heals", "Boosts", "Death Type", "Revives", "Team Kills"
            ]
            
            tabela_original = tabela_original.drop(columns=[col for col in colunas_para_remover if col in tabela_original.columns])
            
            colunas_iniciais = ["Team Name", "Name", "Win Place"]
            outras_colunas = [col for col in tabela_original.columns if col not in colunas_iniciais]
            tabela_original = tabela_original[colunas_iniciais + outras_colunas]

            exibir_tabela()

        except FileNotFoundError:
            texto_resultado.delete(1.0, tk.END)
            texto_resultado.insert(tk.END, "Erro: Arquivo não encontrado.")
        except pd.errors.EmptyDataError:
            texto_resultado.delete(1.0, tk.END)
            texto_resultado.insert(tk.END, "Erro: O arquivo está vazio.")
        except pd.errors.ParserError:
            texto_resultado.delete(1.0, tk.END)
            texto_resultado.insert(tk.END, "Erro: Não foi possível ler o arquivo. Verifique se o formato é CSV.")

# Função para exibir a tabela
def exibir_tabela():
    if agrupar_times.get():
        # Agrupar pela "Win Place" e "Team Name" e somar as "Kills"
        tabela_agrupada = tabela_original.groupby(["Win Place", "Team Name"], as_index=False)["Kills"].sum()
        colunas_agrupadas = ["Win Place", "Team Name", "Kills"]
        tabela_agrupada = tabela_agrupada[colunas_agrupadas]

        # Arredondar a coluna "Damage Dealt" se existir
        colunas_dano = ["Damage Dealt"]
        for col in colunas_dano:
            if col in tabela_agrupada.columns:
                tabela_agrupada[col] = tabela_agrupada[col].apply(arredondar_damage)

        # Ordenar pela "Win Place"
        tabela_agrupada = tabela_agrupada.sort_values(by="Win Place", ascending=True)
        tabela_agrupada["Team Name"] = tabela_agrupada["Team Name"].apply(extrair_numero_time)
        
        # Calcular os pontos para cada linha
        tabela_agrupada['Pontos'] = tabela_agrupada.apply(calcular_pontos, axis=1)
    else:
        tabela_agrupada = tabela_original

    # Remover a coluna "Kill Place" se existir
    if "Kill Place" in tabela_agrupada.columns:
        tabela_agrupada = tabela_agrupada.drop(columns=["Kill Place"])

    # Limpar os itens atuais da treeview
    for item in treeview.get_children():
        treeview.delete(item)
    
    treeview["columns"] = list(tabela_agrupada.columns)
    treeview["show"] = "headings"
    
    # Exibir os cabeçalhos da tabela com tradução
    for col in tabela_agrupada.columns:
        treeview.heading(col, text=traducoes.get(col, col))

    # Ajuste das larguras das colunas
    for col in tabela_agrupada.columns:
        if col == "Team Name":
            treeview.column(col, width=200, anchor="w")
        elif col == "Name":
            treeview.column(col, width=150, anchor="w")
        else:
            treeview.column(col, width=100, anchor="w")

    # Inserir os dados da tabela na Treeview
    for _, row in tabela_agrupada.iterrows():
        treeview.insert("", "end", values=list(row))

# Função para alternar o agrupamento
def alternar_agrupamento():
    agrupar_times.set(not agrupar_times.get())
    if agrupar_times.get():
        botao_agrupamento.config(text="Não Agrupar Times")
    else:
        botao_agrupamento.config(text="Agrupar Times")

    exibir_tabela()

# Função para exportar os dados para um novo CSV
def exportar_csv():
    if 'tabela_original' in globals():
        # Verifica se a pasta "Exportados" existe, se não, cria
        pasta_exportados = os.path.join(os.path.dirname(caminho_arquivo), "Exportados")
        if not os.path.exists(pasta_exportados):
            os.makedirs(pasta_exportados)

        # Definir o nome do arquivo exportado (com sufixo '_formatted')
        nome_arquivo = os.path.basename(caminho_arquivo).replace(".csv", ".csv")
        caminho_exportado = os.path.join(pasta_exportados, nome_arquivo)
        
        # Agrupar os dados conforme o estado de agrupamento
        if agrupar_times.get():
            tabela_agrupada = tabela_original.groupby(["Win Place", "Team Name"], as_index=False)["Kills"].sum()
            colunas_agrupadas = ["Win Place", "Team Name", "Kills"]
            tabela_agrupada = tabela_agrupada[colunas_agrupadas]
            tabela_agrupada["Team Name"] = tabela_agrupada["Team Name"].apply(extrair_numero_time)
            
            # Calcular os pontos para cada linha
            tabela_agrupada['Pontos'] = tabela_agrupada.apply(calcular_pontos, axis=1)
        else:
            tabela_agrupada = tabela_original
        
        # Salvar no CSV
        tabela_agrupada.to_csv(caminho_exportado, index=False)
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, f"Arquivo exportado com sucesso: {caminho_exportado}")

# Criando a interface gráfica
root = tk.Tk()
root.title("Analisador de Campeonato")

# Variável para controlar o estado do agrupamento
agrupar_times = tk.BooleanVar()

# Botão para alternar entre agrupar ou não os times
botao_agrupamento = tk.Button(root, text="Agrupar Times", command=alternar_agrupamento)
botao_agrupamento.pack(pady=10)

# Botão para exportar os dados para CSV
botao_exportar = tk.Button(root, text="Exportar CSV", command=exportar_csv)
botao_exportar.pack(pady=20)

# Botão para carregar o arquivo CSV
botao_carregar = tk.Button(root, text="Carregar CSV", command=carregar_csv)
botao_carregar.pack(pady=10)

# Frame para exibir a tabela
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Barra de rolagem vertical
barra_rolagem_vertical = tk.Scrollbar(frame, orient="vertical")
barra_rolagem_horizontal = tk.Scrollbar(frame, orient="horizontal")

# Treeview para exibir a tabela
treeview = ttk.Treeview(frame, yscrollcommand=barra_rolagem_vertical.set, xscrollcommand=barra_rolagem_horizontal.set)
treeview.pack(fill=tk.BOTH, expand=True)

# Associar a barra de rolagem
barra_rolagem_vertical.config(command=treeview.yview)
barra_rolagem_vertical.pack(side=tk.RIGHT, fill=tk.Y)
barra_rolagem_horizontal.config(command=treeview.xview)
barra_rolagem_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

# Caixa de texto para exibir resultados
texto_resultado = tk.Text(root, height=4, wrap=tk.WORD)
texto_resultado.pack(padx=10, pady=10)

# Iniciar o loop principal
root.mainloop()
