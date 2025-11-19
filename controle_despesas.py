import pandas as pd
import os
from datetime import datetime
import sys

# --- Variáveis de Configuração ---
# Nome do arquivo principal de dados (será lido e atualizado)
FILE_NAME = 'lancamentos.xlsx'

# Lista de categorias predefinidas para o usuário escolher
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


# --- Funções Auxiliares de Dados e Formatação ---

def formatar_brl(valor):
    """Formata um float para o padrão monetário brasileiro (R$ X.XXX,XX)."""
    # Garante a substituição correta de separadores de milhares e decimais
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def carregar_dados():
    """Tenta carregar os dados do arquivo Excel. Se não existir, cria um DataFrame vazio."""
    
    colunas = ['data', 'categoria', 'descrição', 'valor']
    
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            print(f"Dados carregados com sucesso de {FILE_NAME}")
            
            # Garante que a coluna 'valor' seja numérica e 'data' seja tratada corretamente
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            # Converte a data e garante que esteja no formato YYYY-MM-DD
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.strftime('%Y-%m-%d')
            
            # Remove linhas com valores inválidos (NaN)
            df.dropna(subset=['valor', 'data'], inplace=True)
            
            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo Excel ({FILE_NAME}). Iniciando com dados vazios. Erro: {e}")
            return pd.DataFrame(columns=colunas)
    else:
        print(f"Arquivo {FILE_NAME} não encontrado. Criando novo controle de despesas.")
        return pd.DataFrame(columns=colunas)

def salvar_dados(df):
    """Salva o DataFrame principal no arquivo Excel de lançamentos (Atualização)."""
    try:
        # Garante que o arquivo seja fechado antes de tentar salvar
        df.to_excel(FILE_NAME, index=False)
        print(f"\nTodos os lançamentos foram salvos em '{FILE_NAME}'.")
    except Exception as e:
        print(f"ERRO: Não foi possível salvar os dados. Feche o arquivo {FILE_NAME} se estiver aberto. Erro: {e}")


# --- Funções de Análise e Exportação ---

def somar_por_categoria(df):
    """Soma e exibe o valor total gasto por cada categoria."""
    if df.empty:
        print("\nNenhuma despesa para analisar.")
        return

    resumo = df.groupby('categoria')['valor'].sum().reset_index()
    
    print("\n--- Resumo de Gastos por Categoria (Total Geral) ---")
    
    resumo['Valor Gasto'] = resumo['valor'].apply(formatar_brl)
    
    print(resumo[['categoria', 'Valor Gasto']].to_string(index=False))

def calcular_total_mensal(df):
    """
    Calcula e exibe a soma total de todas as despesas ou o total para um mês específico.
    (REQUISITO: Soma dos gastos no mês correspondente)
    """
    if df.empty:
        print("\nTotal Geral de Despesas Registradas: R$ 0,00")
        return 0
    
    # Pergunta qual mês o usuário quer analisar
    mes_analise_str = input("\nDigite o MÊS e ANO para o resumo (MM/YYYY, Ex: 05/2025). Deixe em branco para o total geral: ").strip()
    
    if not mes_analise_str:
        # Se estiver em branco, calcula o total geral
        total = df['valor'].sum()
        print(f"\nTotal Geral de Despesas Registradas: {formatar_brl(total)}")
        return total

    try:
        # Tenta converter a entrada do usuário para o formato de data (MM/YYYY)
        mes_analise = datetime.strptime(mes_analise_str, '%m/%Y')
        
        # Cria uma coluna de 'Mês/Ano' no DataFrame para filtrar
        # Convertemos para string antes de extrair o Mês/Ano para evitar problemas de tipo
        df_filtrado = df.copy()
        df_filtrado['data'] = pd.to_datetime(df_filtrado['data'])
        df_filtrado['mes_ano'] = df_filtrado['data'].dt.strftime('%m/%Y')
        
        # Filtra os dados apenas para o mês/ano desejado
        df_mes = df_filtrado[df_filtrado['mes_ano'] == mes_analise.strftime('%m/%Y')]
        
        if df_mes.empty:
            print(f"\nNenhum gasto encontrado para o mês {mes_analise_str}.")
            return 0
            
        # Calcula o total para o mês
        total_mes = df_mes['valor'].sum()
        print(f"\nTotal de Despesas para {mes_analise_str}: {formatar_brl(total_mes)}")
        
        # Opcional: Mostra o resumo por categoria DENTRO do mês
        resumo_mes = df_mes.groupby('categoria')['valor'].sum().reset_index()
        resumo_mes['Valor Gasto'] = resumo_mes['valor'].apply(formatar_brl)
        print("\n--- Detalhe por Categoria (no Mês) ---")
        print(resumo_mes[['categoria', 'Valor Gasto']].to_string(index=False))
        
        return total_mes
        
    except ValueError:
        print("Formato de mês/ano inválido. Por favor, use MM/YYYY (Ex: 05/2025).")
        return 0


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
        print(f"\nResumo de gastos exportado com sucesso para '{output_file}'!")
    except Exception as e:
        print(f"Erro ao exportar o arquivo. Feche o arquivo '{output_file}' se estiver aberto. Erro: {e}")


# --- Função de Interação com Categorias (Atualizada e Validada) ---

def inserir_despesa(df):
    """Permite ao usuário inserir uma nova despesa, escolhendo a categoria, digitando a data, a descrição e o valor."""
    
    print("\n--- Inserir Nova Despesa ---")
    
    # 1. Obter Categoria (Com Menu de Opções - REQUISITO)
    while True:
        print("\nEscolha a Categoria:")
        # Exibe as categorias com números
        for i, cat in enumerate(CATEGORIAS_PADRAO, 1):
            print(f"{i}. {cat}")
        
        escolha_cat = input("Digite o número da categoria: ").strip()
        
        try:
            indice = int(
