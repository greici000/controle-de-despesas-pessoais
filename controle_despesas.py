import pandas as pd
import os

ARQUIVO = "gastos.xlsx"

# -----------------------------
# Função para carregar ou criar o arquivo
# -----------------------------
def carregar_arquivo():
    if os.path.exists(ARQUIVO):
        return pd.read_excel(ARQUIVO)
    else:
        df = pd.DataFrame(columns=["Dia", "Mês", "Ano", "Categoria", "Descrição", "Valor"])
        df.to_excel(ARQUIVO, index=False)
        return df

# -----------------------------
# Função para salvar dados
# -----------------------------
def salvar_arquivo(df):
    df.to_excel(ARQUIVO, index=False)

# -----------------------------
# Cadastro de novo gasto
# -----------------------------
def cadastrar_gasto(df):
    print("\n--- CADASTRO DE GASTO ---")
    
    dia = int(input("Dia: "))
    mes = int(input("Mês: "))
    ano = int(input("Ano: "))
    
    categoria = input("Categoria (Ex: Alimentação, Transporte, Lazer...): ")
    descricao = input("Descrição do gasto: ")
    valor = float(input("Valor (R$): "))
    
    novo = {"Dia": dia, "Mês": mes, "Ano": ano,
            "Categoria": categoria, "Descrição": descricao, "Valor": valor}
    
    df = df.append(novo, ignore_index=True)
    salvar_arquivo(df)
    
    print("\nGasto registrado com sucesso!\n")
    return df

# -----------------------------
# Resumo mensal
# -----------------------------
def resumo_mensal(df):
    print("\n--- RESUMO MENSAL ---")
    mes = int(input("Informe o mês: "))
    ano = int(input("Informe o ano: "))

    filtro = df[(df["Mês"] == mes) & (df["Ano"] == ano)]
    
    if filtro.empty:
        print("\nNenhum gasto encontrado para o período.\n")
    else:
        total = filtro["Valor"].sum()
        print(f"\nTotal de gastos em {mes}/{ano}: R$ {total:.2f}\n")
        
        print("Detalhamento:")
        print(filtro[["Dia", "Categoria", "Descrição", "Valor"]])

# -----------------------------
# Menu principal
# -----------------------------
def menu():
    df = carregar_arquivo()
    
    while True:
        print("\n===== CONTROLE DE GASTOS PESSOAIS =====")
        print("1 - Cadastrar novo gasto")
        print("2 - Mostrar resumo mensal")
        print("3 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            df = cadastrar_gasto(df)
        elif opcao == "2":
            resumo_mensal(df)
        elif opcao == "3":
            print("\nSaindo... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar programa
menu()
