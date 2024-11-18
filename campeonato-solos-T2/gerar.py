import os
import csv

# Nome da pasta onde os arquivos serão criados
pasta = "partidas"

# Criar a pasta se não existir
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Lista dos arquivos com os nomes dos jogos
arquivos = [
    "partida-1-Erangel.csv",
    "partida-2-Karakin.csv",
    "partida-3-Sanhok.csv",
    "partida-4-Miramar.csv",
    "partida-5-Taego.csv",
    "partida-6-Deston.csv",
    "partida-7-Vikendi.csv",
    "partida-8-Paramo.csv",
    "partida-9-Miramar.csv",
    "partida-10-Taego.csv"
]

# Dados a serem escritos nos arquivos
dados = [
    ["Jogador", "Kills", "Posição", "Pontos"],
    ["Jogador1", 0, 0, 0],
    ["Jogador2", 0, 0, 0],
    ["Jogador3", 0, 0, 0],
    ["Jogador4", 0, 0, 0],
    ["Jogador5", 0, 0, 0],
    ["Jogador6", 0, 0, 0],
    ["Jogador7", 0, 0, 0],
    ["Jogador8", 0, 0, 0],
    ["Jogador9", 0, 0, 0],
    ["Jogador10", 0, 0, 0]
]

# Criar os arquivos CSV
for nome_arquivo in arquivos:
    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    
    # Criar o arquivo CSV e escrever os dados
    with open(caminho_arquivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(dados)

print(f"Arquivos CSV criados na pasta '{pasta}' com sucesso!")
