import pandas as pd
import os
from datetime import datetime
import sys


FILE_NAME = 'lancamentos.xlsx'


CATEGORIAS_PADRAO = [
    "Alimentação", 
    "Transporte", 
    "Moradia", 
    "Saúde", 
    "Educação", 
    "Lazer", 
    "Serviços", 
    "Outros"
]



def formatar_brl(valor):
    """Formata um float para o padrão monetário brasileiro (R$ X.XXX,XX)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def carregar_dados():
    """Tenta carregar os dados do arquivo Excel. Se não existir, cria um DataFrame vazio."""
    
    colunas = ['data', 'categoria', 'descrição', 'valor']
    
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            print(f" Dados carregados com sucesso de {FILE_NAME}")
            
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.strftime('%Y-%m-%d')
            
            df.dropna(subset=['valor', 'data'], inplace=True)
            
            return df
        except Exception as e:
            print(f" Erro ao ler o arquivo Excel ({FILE_NAME}). Iniciando com dados vazios. Erro: {e}")
            return pd.DataFrame(columns=colunas)
    else:
        print(f" Arquivo {FILE_NAME} não encontrado. Criando novo controle de despesas.")
        return pd.DataFrame(columns=colunas)

def salvar_dados(df):
    """Salva o DataFrame principal no arquivo Excel de lançamentos (Atualização)."""
    try:
        df.to_excel(FILE_NAME, index=False)
        print(f"\n Todos os lançamentos foram salvos em '{FILE_NAME}'.")
    except Exception as e:
        print(f" ERRO: Não foi possível salvar os dados. Feche o arquivo {FILE_NAME} se estiver aberto. Erro: {e}")




def somar_por_categoria(df):
    """Soma e exibe o valor total gasto por cada categoria."""
    if df.empty:
        print("\nNenhuma despesa para analisar.")
        return

    resumo = df.groupby('categoria')['valor'].sum().reset_index()
    
    print("\n--- Resumo de Gastos por Categoria ---")
    
    resumo['Valor Gasto'] = resumo['valor'].apply(formatar_brl)
    
    print(resumo[['categoria', 'Valor Gasto']].to_string(index=False))

def calcular_total_mensal(df):
    """Calcula e exibe a soma total de todas as despesas."""
    if df.empty:
        print("\n Total Geral de Despesas Registradas: R$ 0,00")
        return 0
        
    total = df['valor'].sum()
    print(f"\n Total Geral de Despesas Registradas: {formatar_brl(total)}")
    return total

def exportar_resumo(df):
    """Exporta o resumo de gastos por categoria para um novo arquivo Excel."""
    
    if df.empty:
        print("\nNenhuma despesa para exportar o resumo.")
        return
        
    resumo_df = df.groupby('categoria')['valor'].sum().reset_index()
    resumo_df.columns = ['Categoria', 'Total Gasto (R$)']
    
    output_file = 'resumo_gastos_exportado.xlsx'
    
    try:
        resumo_df.to_excel(output_file, index=False)
        print(f"\n Resumo de gastos exportado com sucesso para '{output_file}'!")
    except Exception as e:
        print(f" Erro ao exportar o arquivo. Feche o arquivo '{output_file}' se estiver aberto. Erro: {e}")



def inserir_despesa(df):
    """Permite ao usuário inserir uma nova despesa, escolhendo a categoria, digitando a data, a descrição e o valor."""
    
    print("\n--- Inserir Nova Despesa ---")
    

    while True:
        print("\nEscolha a Categoria:")
        
        for i, cat in enumerate(CATEGORIAS_PADRAO, 1):
            print(f"{i}. {cat}")
        
        escolha_cat = input("Digite o número da categoria: ").strip()
        
        try:
            indice = int(escolha_cat) - 1
            if 0 <= indice < len(CATEGORIAS_PADRAO):
                categoria = CATEGORIAS_PADRAO[indice]
                print(f"Categoria selecionada: {categoria}")
                break
            else:
                print(" Número fora do intervalo. Por favor, escolha um número da lista.")
        except ValueError:
            print(" Entrada inválida. Por favor, digite apenas o número da opção.")
            
   
    descricao = input("Descrição do Gasto: ").strip()

    
    while True:
        data_str = input("Data do Gasto (Formato YYYY-MM-DD, Ex: 2025-01-25): ").strip()
        try:
            
            data_validada = datetime.strptime(data_str, '%Y-%m-%d')
            data = data_validada.strftime('%Y-%m-%d') # Salva no formato padronizado
            break
        except ValueError:
            print(" Formato de data inválido. Use o formato YYYY-MM-DD (Ano-Mês-Dia).")
    
    
    while True:
        try:
            valor_str = input("Valor (Use ponto como separador decimal, Ex: 50.80): ").replace(",", ".")
            valor = float(valor_str)
            if valor <= 0:
                 raise ValueError("O valor deve ser positivo.")
            break
        except ValueError as e:
            print(f" Entrada inválida. O valor deve ser um número positivo. Erro: {e}")
            
    
    nova_despesa = pd.Series({
        'data': data,
        'categoria': categoria,
        'descrição': descricao,
        'valor': valor
    })
    
   
    df_atualizado = pd.concat([df, nova_despesa.to_frame().T], ignore_index=True)
    
    print(f"\n Despesa '{descricao}' ({formatar_brl(valor)}) adicionada à categoria '{categoria}' na data {data}.")
    
    return df_atualizado




def menu_principal():
    """Função principal que gerencia o fluxo do programa, exibindo o menu."""
    
    df_despesas = carregar_dados()
    
    while True:
        print("\n==================================")
        print("       CONTROLE DE DESPESAS")
        print("==================================")

# Bloco de Execução Principal
if __name__ == "__main__":
    menu_principal()