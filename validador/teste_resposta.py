import requests
from bs4 import BeautifulSoup
import json

def verificar_perfil(nome_jogador):
    # Monta a URL com o nome do jogador
    url = f"https://pubg.op.gg/user/{nome_jogador}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        # Faz uma requisição GET com o cabeçalho "User-Agent"
        response = requests.get(url, headers=headers)
        
        # Verifica o status code da resposta
        if response.status_code == 200:
            # Usa BeautifulSoup para analisar o conteúdo HTML
            if "The player is not registered at OP.GG" in response.text:
                return f"Perfil '{nome_jogador}' não encontrado."
            else:
                return f"Perfil '{nome_jogador}' encontrado! URL acessível."
        else:
            return f"Erro ao acessar o perfil '{nome_jogador}'. Status Code: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o site: {e}"

def validar_jogadores_de_json(arquivo_json):
    try:
        # Lê o arquivo JSON
        with open(arquivo_json, 'r') as f:
            data = json.load(f)
        
        # Listas para armazenar resultados
        nao_encontrados = []
        encontrados = []
        
        # Itera sobre a lista de jogadores e verifica cada um
        for jogador in data['jogadores']:
            resultado = verificar_perfil(jogador)
            if "não encontrado" in resultado:
                nao_encontrados.append(resultado)
            else:
                encontrados.append(resultado)
        
        # Exibe os resultados
        if nao_encontrados:
            print("Jogadores não encontrados:")
            for msg in nao_encontrados:
                print(msg)
        else:
            print("Todos os jogadores foram encontrados.")
        
        if encontrados:
            print("\nJogadores encontrados:")
            for msg in encontrados:
                print(msg)

    except FileNotFoundError:
        print(f"Arquivo '{arquivo_json}' não encontrado.")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{arquivo_json}'.")

# Executa a função para validar jogadores
validar_jogadores_de_json('jogadores.json')
