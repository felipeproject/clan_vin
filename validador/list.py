import pandas as pd
import json  # Certifique-se de importar o módulo json

# Carregar o arquivo CSV
df = pd.read_csv('phoneContacts.csv')

# 1. Remover a coluna NUMBER
if 'NUMBER' in df.columns:
    df.drop(columns=['NUMBER'], inplace=True)

# 2. Remover linhas duplicadas
df.drop_duplicates(inplace=True)

# 3. Filtrar linhas que não têm [VIN] no nome
df = df[df['NAME'].str.contains(r'\[VIN\]', na=False)]

# 4. Remover o prefixo [VIN]
df['NAME'] = df['NAME'].str.replace(r'\[VIN\]\s*', '', regex=True)

# 5. Criar a estrutura desejada para o JSON
resultados = {
    "jogadores": df['NAME'].tolist()  # Converte a coluna 'NAME' em uma lista
}

# Salvar o resultado em um arquivo JSON
with open('jogadores.json', 'w') as json_file:
    json.dump(resultados, json_file, indent=4)

print("Processamento concluído. O arquivo 'resultado.json' foi gerado.")
