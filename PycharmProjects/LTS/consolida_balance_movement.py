import functions

# Caminho para a pasta contendo os arquivos CSV MOVEMENT
caminho_pasta_movement = "C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\database\\movement"

# Chama a função para ler os CSVs da pasta
df_final_movement = functions.ler_csvs_pasta_movement(caminho_pasta_movement)

# Gera um arquivo CSV com todas as informações coletadas
df_final_movement.to_csv("C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\consolidado\\dados_completos_movement.csv", index=False)


# Caminho para a pasta contendo os arquivos CSV BALANCE
caminho_pasta_balance = "C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\database\\balance"

# Chama a função para ler os CSVs da pasta
df_final_balance = functions.ler_csvs_pasta_balance(caminho_pasta_balance)

# Gera um arquivo CSV com todas as informações coletadas
df_final_balance.to_csv("C:\\Users\\luish\\OneDrive\\Área de Trabalho\\Dados\\consolidado\\dados_completos_balance.csv", index=False)