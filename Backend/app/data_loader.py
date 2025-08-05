# app/data_loader.py
# Este módulo é responsável por todo o processo de carregamento, limpeza e
# pré-processamento dos dados dos arquivos CSV.

import pandas as pd
from typing import Dict, Any, List

# Variáveis globais para armazenar os DataFrames processados.
despesas_df: pd.DataFrame = None
materias_df: pd.DataFrame = None
atas_df: pd.DataFrame = None
vereadores_dados: Dict[str, Any] = {}

def padronizar_nome_vereador(df, coluna_nome):
    """
    Padroniza nomes de vereadores em um DataFrame para facilitar junções.
    Esta é uma etapa crucial de limpeza de dados.
    """
    if coluna_nome in df.columns:
        # Garante que a coluna é do tipo string antes de aplicar operações .str
        df[coluna_nome] = df[coluna_nome].astype(str)
        df[coluna_nome] = df[coluna_nome].str.strip().str.upper().str.replace('DO NOSSA CARA', '').str.replace('PROFESSOR ', '').str.replace('PROFESSORA ', '').str.strip()
    return df

def carregar_e_processar_dados() -> Dict[str, Any]:
    """
    Carrega os dados dos arquivos CSV, limpa, padroniza e os armazena
    em uma estrutura de dados global.
    """
    global despesas_df, materias_df, atas_df, vereadores_dados

    print("Iniciando o carregamento e pré-processamento dos dados...")

    try:
        # Carregar arquivos CSV
        # Tentando 'utf-8' primeiro, que é mais comum e pode lidar com BOM
        despesas_df = pd.read_csv("data/despesas_vereadores_2023-2024-2025_consolidado.csv", encoding='utf-8', sep=',', thousands='.', decimal=',')
        materias_df = pd.read_csv("data/materias_legislativas_extraidas.csv", encoding='utf-8', sep=',')
        atas_df = pd.read_csv("data/atas_com_detalhes_extraidos.csv", encoding='utf-8', sep=';')
    except UnicodeDecodeError:
        # Se utf-8 falhar, tenta 'latin1'
        print("UTF-8 falhou, tentando latin1 para os arquivos CSV.")
        despesas_df = pd.read_csv("data/despesas_vereadores_2023-2024-2025_consolidado.csv", encoding='latin1', sep=',', thousands='.', decimal=',')
        materias_df = pd.read_csv("data/materias_legislativas_extraidas.csv", encoding='latin1', sep=',')
        atas_df = pd.read_csv("data/atas_com_detalhes_extraidos.csv", encoding='latin1', sep=';')
    except FileNotFoundError:
        print("Erro: Verifique se os arquivos CSV estão na pasta 'data'.")
        raise

    # Limpar espaços em branco dos nomes das colunas em todos os DataFrames
    despesas_df.columns = despesas_df.columns.str.strip()
    materias_df.columns = materias_df.columns.str.strip()
    atas_df.columns = atas_df.columns.str.strip()

    # Remover o caractere BOM (Byte Order Mark) se presente nos nomes das colunas
    # O caractere BOM é '\ufeff' ou 'ï»¿' em algumas codificações
    atas_df.columns = atas_df.columns.str.replace('\ufeff', '', regex=False)
    despesas_df.columns = despesas_df.columns.str.replace('\ufeff', '', regex=False)
    materias_df.columns = materias_df.columns.str.replace('\ufeff', '', regex=False)


    # Imprimir as colunas de atas_df para depuração (agora com BOM removido)
    print("Colunas do atas_df após carregamento, limpeza de nomes e remoção de BOM:", atas_df.columns)


    # Padronizar nomes dos vereadores em todos os DataFrames
    despesas_df = padronizar_nome_vereador(despesas_df, 'Nome Vereador')
    materias_df = padronizar_nome_vereador(materias_df, 'Autor')

    # Limpar e converter dados
    for col in ['Valor Total', 'Saldo']:
        # REMOVIDO: despesas_df[col] = despesas_df[col].astype(str)
        # REMOVIDO: despesas_df[col] = despesas_df[col].str.replace('"', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        # A leitura do CSV com thousands='.' e decimal=',' já deve ter convertido para float.
        # Agora, apenas preenchemos NaN com 0.
        despesas_df[col] = despesas_df[col].fillna(0)
    
    # Processar a tabela de atas para criar uma estrutura de dados por vereador
    vereadores_dados = {}
    for _, row in atas_df.iterrows():
        # Garante que 'Ata' é string e usa o nome da coluna limpo
        dia_sessao = str(row['Ata']).split(' - ')[0] 
        
        # Garante que as colunas são strings antes de usar .split()
        presentes_str = str(row['Vereadores Presentes'])
        ausentes_str = str(row['Vereadores Ausentes'])

        presentes = [p.strip().upper() for p in presentes_str.split(',')]
        ausentes = [a.strip().upper() for a in ausentes_str.split(',')]

        for nome in presentes:
            if nome not in vereadores_dados:
                vereadores_dados[nome] = {"despesas": [], "materias_legislativas": [], "sessoes_presente": [], "sessoes_ausente": []}
            vereadores_dados[nome]["sessoes_presente"].append(dia_sessao)
        
        for nome in ausentes:
            if nome not in vereadores_dados:
                vereadores_dados[nome] = {"despesas": [], "materias_legislativas": [], "sessoes_presente": [], "sessoes_ausente": []}
            vereadores_dados[nome]["sessoes_ausente"].append(dia_sessao)

    # Processar despesas e matérias e associar aos vereadores
    for nome_vereador, grupo in despesas_df.groupby('Nome Vereador'):
        if nome_vereador not in vereadores_dados:
            vereadores_dados[nome_vereador] = {"despesas": [], "materias_legislativas": [], "sessoes_presente": [], "sessoes_ausente": []}
        
        for _, despesa_row in grupo.iterrows():
            vereadores_dados[nome_vereador]["despesas"].append(despesa_row.to_dict())

    for nome_vereador, grupo in materias_df.groupby('Autor'):
        if nome_vereador not in vereadores_dados:
            vereadores_dados[nome_vereador] = {"despesas": [], "materias_legislativas": [], "sessoes_presente": [], "sessoes_ausente": []}

        for _, materia_row in grupo.iterrows():
            vereadores_dados[nome_vereador]["materias_legislativas"].append(materia_row.to_dict())

    print("Dados carregados e processados com sucesso.")
    return vereadores_dados
