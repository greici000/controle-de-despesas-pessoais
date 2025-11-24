import pandas as pd
import os

ARQUIVO = "gastos.xlsx"


CATEGORIAS = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Serviços"
]


def carregar_arquivo():
    if os.path.exists(ARQUIVO):
        return pd.read_excel(ARQUIVO)
    else:
        df = pd.DataFrame(columns=["Dia", "Mês", "Ano", "Categoria", "Descrição", "Valor"])
        df.to_excel(ARQUIVO, index=False)
        return df


def salvar_arquivo(df):
    df.to_excel(ARQUIVO, index=False)


def cadastrar_gasto(df):
    print("\n--- CADASTRO DE GASTO ---")

    data_str = input("Data do gasto (dd/mm/aaaa): ")

    try:
        dia, mes, ano = map(int, data_str.split("/"))
    except:
        print("\n❌ Data inválida! Use o formato dd/mm/aaaa.\n")
        return df

    
    print("\nEscolha a categoria:")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"{i} - {cat}")

    try:
        opc = int(input("Opção: "))
        categoria = CATEGORIAS[opc - 1]
    except:
        print("\n❌ Categoria inválida!\n")
        return df

    descricao = input("Descrição do gasto: ")
    valor = float(input("Valor (R$): "))

    novo = pd.DataFrame([{
        "Dia": dia,
        "Mês": mes,
        "Ano": ano,
        "Categoria": categoria,
        "Descrição": descricao,
        "Valor": valor
    }])

  
    df = pd.concat([df, novo], ignore_index=True)
    salvar_arquivo(df)

    print("\n✅ Gasto registrado com sucesso!\n")
    return df


def resumo_mensal(df):
    print("\n--- RESUMO MENSAL ---")

    try:
        mes = int(input("Informe o mês: "))
        ano = int(input("Informe o ano: "))
    except:
        print("\n❌ Mês ou ano inválido!\n")
        return

    filtro = df[(df["Mês"] == mes) & (df["Ano"] == ano)]

    if filtro.empty:
        print("\nNenhum gasto encontrado neste mês.\n")
        return

    total = filtro["Valor"].sum()

    print(f"\n📌 Total de gastos em {mes}/{ano}: R$ {total:.2f}\n")
    print("Detalhamento:\n")
    print(filtro[["Dia", "Categoria", "Descrição", "Valor"]].to_string(index=False))


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
            print("\nSaindo... até a próxima!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
