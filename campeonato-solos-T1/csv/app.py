import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import pytz
import re

# Função para abrir a caixa de diálogo e selecionar a pasta
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    return pasta

# Função para converter o horário UTC para horário de Brasília (BRT)
def converter_para_brasilia(utc_time):
    # Define o timezone de Brasília (considerando o horário de verão automaticamente)
    brt_timezone = pytz.timezone('America/Sao_Paulo')
    # Localiza a hora UTC
    utc_time = pytz.utc.localize(utc_time)
    # Converte para o horário de Brasília
    brt_time = utc_time.astimezone(brt_timezone)
    return brt_time

# Função para extrair a data do nome do arquivo e organizar os CSVs por data e hora
def listar_csv_organizados_por_data(pasta):
    # Verifica se a pasta existe
    if not os.path.exists(pasta):
        print("A pasta especificada não existe.")
        return

    # Lista todos os arquivos na pasta
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.csv')]

    # Cria uma lista de tuplas (data extraída do nome do arquivo, nome do arquivo)
    arquivos_com_data = []
    for arquivo in arquivos:
        try:
            # Usamos uma expressão regular para encontrar a data e hora no formato correto
            # A regex vai procurar por uma sequência como: 2024_11_14_00h07h43
            match = re.search(r'(\d{4})_(\d{2})_(\d{2})_(\d{2})h(\d{2})h(\d{2})', arquivo)
            
            if not match:
                print(f"Formato de nome de arquivo inválido: {arquivo}")
                continue
            
            # Se encontramos a data, reorganizamos para o formato YYYY-MM-DD HH:MM:SS
            ano = match.group(1)
            mes = match.group(2)
            dia = match.group(3)
            hora = match.group(4)
            minuto = match.group(5)
            segundo = match.group(6)
            
            # Criamos a string no formato YYYY-MM-DD HH:MM:SS
            data_extraida_str = f"{ano}-{mes}-{dia} {hora}:{minuto}:{segundo}"

            # Converte a data extraída para datetime
            data_extraida = datetime.strptime(data_extraida_str, '%Y-%m-%d %H:%M:%S')

            # Converte a data extraída para horário de Brasília (BRT)
            data_brasilia = converter_para_brasilia(data_extraida)
            arquivos_com_data.append((data_brasilia, arquivo))
        except Exception as e:
            # Caso não consiga extrair a data, ignora o arquivo e imprime o erro
            print(f"Erro ao processar o arquivo: {arquivo} | Erro: {e}")
            continue

    # Ordena os arquivos pela data extraída (em ordem crescente)
    arquivos_com_data.sort()

    # Exibe os arquivos organizados por data
    print("Arquivos CSV organizados por data (Horário de Brasília):")
    for data_brasilia, arquivo in arquivos_com_data:
        # Exibe a data formatada em horário de Brasília
        data_formatada = data_brasilia.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{data_formatada} - {arquivo}")

    # Salva o backup com as datas e horas em um arquivo de texto
    salvar_backup(arquivos_com_data)

# Função para salvar o backup dos arquivos
def salvar_backup(arquivos_com_data):
    try:
        # Define o caminho para o arquivo de backup
        backup_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt"), ("CSV", "*.csv")], title="Salvar Backup")

        # Se o usuário escolheu um caminho válido
        if backup_path:
            with open(backup_path, 'w', encoding='utf-8') as f:
                # Escreve o cabeçalho do arquivo de backup
                f.write("Data (Horário de Brasília) - Arquivo\n")
                # Escreve as informações dos arquivos organizados
                for data_brasilia, arquivo in arquivos_com_data:
                    data_formatada = data_brasilia.strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{data_formatada} - {arquivo}\n")

            print(f"Backup salvo com sucesso em: {backup_path}")
    except Exception as e:
        print(f"Erro ao salvar o backup: {e}")

# Função principal
def main():
    # Cria a janela Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    
    # Pede para o usuário selecionar uma pasta
    pasta = selecionar_pasta()
    
    # Lista e organiza os arquivos CSV por data
    if pasta:
        listar_csv_organizados_por_data(pasta)

# Executa o programa
if __name__ == "__main__":
    main()
