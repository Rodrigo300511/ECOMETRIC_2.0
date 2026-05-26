"""
analytics_export.py - Análise de Dados e Exportação

Script responsável por:
- Extrair dados do banco para DataFrame
- Criar análises por categoria de veículo
- Gerar relatórios em Excel com múltiplas abas
- Criar visualizações de dados
"""

import pandas as pd
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from src.database import conectar, fechar_conexao


def extrair_dados_completos():
    """
    Extrai dados completos do banco para análise.
    
    Returns:
        dict: Dicionário com múltiplos DataFrames
    """
    
    conn = conectar()
    
    # =========================================================
    # EXTRAIR DADOS
    # =========================================================
    
    # Dados de impacto por veículo e data
    df_impacto = pd.read_sql_query("""
        SELECT
            i.placa,
            m.nome as modelo,
            m.marca,
            c.nome as categoria,
            i.tipo,
            i.tempo_poupado,
            i.combustivel_poupado_ml,
            i.co2_evitar_g,
            i.data_hora,
            CAST(substr(i.data_hora, 1, 7) as TEXT) as mes
        FROM impacto_ambiental i
        JOIN veiculos v ON i.placa = v.placa
        JOIN modelos m ON v.modelo_id = m.id
        JOIN categorias c ON m.categoria_id = c.id
        ORDER BY i.data_hora DESC
    """, conn)
    
    # Dados de passagens
    df_passagens = pd.read_sql_query("""
        SELECT
            p.placa,
            m.nome as modelo,
            m.marca,
            c.nome as categoria,
            p.tipo,
            p.capcoins_ganhos,
            p.data_hora,
            CAST(substr(p.data_hora, 1, 7) as TEXT) as mes
        FROM passagens p
        JOIN veiculos v ON p.placa = v.placa
        JOIN modelos m ON v.modelo_id = m.id
        JOIN categorias c ON m.categoria_id = c.id
        ORDER BY p.data_hora DESC
    """, conn)
    
    # Dados de saldos
    df_saldos = pd.read_sql_query("""
        SELECT
            s.placa,
            m.nome as modelo,
            m.marca,
            c.nome as categoria,
            s.saldo as capcoins,
            v.data_cadastro
        FROM saldo_capcoins s
        JOIN veiculos v ON s.placa = v.placa
        JOIN modelos m ON v.modelo_id = m.id
        JOIN categorias c ON m.categoria_id = c.id
        ORDER BY s.saldo DESC
    """, conn)
    
    # Convertendo datas para datetime
    df_impacto['data_hora'] = pd.to_datetime(df_impacto['data_hora'])
    df_passagens['data_hora'] = pd.to_datetime(df_passagens['data_hora'])
    df_saldos['data_cadastro'] = pd.to_datetime(df_saldos['data_cadastro'])
    
    fechar_conexao(conn)
    
    return {
        'impacto': df_impacto,
        'passagens': df_passagens,
        'saldos': df_saldos
    }


def criar_analise_por_categoria(dfs):
    """
    Cria análise agregada por categoria de veículo.
    
    Args:
        dfs (dict): Dicionário com DataFrames
    
    Returns:
        pd.DataFrame: Análise por categoria
    """
    
    df = dfs['impacto'].copy()
    
    analise = df.groupby('categoria').agg({
        'placa': 'count',
        'tempo_poupado': 'sum',
        'combustivel_poupado_ml': 'sum',
        'co2_evitar_g': 'sum'
    }).round(2)
    
    analise.columns = [
        'Total Passagens',
        'Tempo Economizado (min)',
        'Combustível Poupado (ml)',
        'CO₂ Evitado (g)'
    ]
    
    # Calcular equivalências
    analise['Equivalente Árvores'] = (
        analise['CO₂ Evitado (g)'] / 21000
    ).round(2)
    
    analise['Folhas de Papel'] = (
        analise['CO₂ Evitado (g)'] / 5
    ).astype(int)
    
    return analise


def criar_analise_temporal(dfs):
    """
    Cria análise temporal por mês.
    
    Args:
        dfs (dict): Dicionário com DataFrames
    
    Returns:
        pd.DataFrame: Análise mensal
    """
    
    df = dfs['impacto'].copy()
    
    analise = df.groupby('mes').agg({
        'placa': 'count',
        'tempo_poupado': 'sum',
        'combustivel_poupado_ml': 'sum',
        'co2_evitar_g': 'sum'
    }).round(2)
    
    analise.columns = [
        'Total Passagens',
        'Tempo Economizado (min)',
        'Combustível Poupado (ml)',
        'CO₂ Evitado (g)'
    ]
    
    return analise


def criar_ranking_veiculos(dfs):
    """
    Cria ranking de veículos por impacto ambiental.
    
    Args:
        dfs (dict): Dicionário com DataFrames
    
    Returns:
        pd.DataFrame: Top 20 veículos
    """
    
    df = dfs['impacto'].copy()
    
    ranking = df.groupby(['placa', 'modelo', 'marca', 'categoria']).agg({
        'tempo_poupado': 'sum',
        'combustivel_poupado_ml': 'sum',
        'co2_evitar_g': 'sum'
    }).round(2)
    
    ranking.columns = [
        'Tempo Poupado (min)',
        'Combustível (ml)',
        'CO₂ Evitado (g)'
    ]
    
    ranking['Árv Equiv'] = (
        ranking['CO₂ Evitado (g)'] / 21000
    ).round(2)
    
    ranking = ranking.sort_values('CO₂ Evitado (g)', ascending=False).head(20)
    
    return ranking


def gerar_relatorio_excel(dfs, output_path='relatorio_ecometric.xlsx'):
    """
    Gera relatório Excel completo com múltiplas abas.
    
    Args:
        dfs (dict): Dicionário com DataFrames
        output_path (str): Caminho do arquivo Excel
    """
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Aba 1: Resumo Executivo
        resumo = {
            'Métrica': [
                'Total de Passagens',
                'Total de Veículos',
                'CO₂ Total Evitado (g)',
                'Tempo Total Economizado (min)',
                'Combustível Total Poupado (ml)',
                'Árvores Preservadas (equiv)',
                'Folhas de Papel (equiv)'
            ],
            'Valor': [
                len(dfs['passagens']),
                dfs['saldos']['placa'].nunique(),
                dfs['impacto']['co2_evitar_g'].sum(),
                dfs['impacto']['tempo_poupado'].sum(),
                dfs['impacto']['combustivel_poupado_ml'].sum(),
                (dfs['impacto']['co2_evitar_g'].sum() / 21000),
                int(dfs['impacto']['co2_evitar_g'].sum() / 5)
            ]
        }
        
        df_resumo = pd.DataFrame(resumo)
        df_resumo.to_excel(writer, sheet_name='Resumo Executivo', index=False)
        
        # Aba 2: Análise por Categoria
        df_categoria = criar_analise_por_categoria(dfs)
        df_categoria.to_excel(writer, sheet_name='Por Categoria')
        
        # Aba 3: Análise Temporal
        df_temporal = criar_analise_temporal(dfs)
        df_temporal.to_excel(writer, sheet_name='Por Período')
        
        # Aba 4: Ranking de Veículos
        df_ranking = criar_ranking_veiculos(dfs)
        df_ranking.to_excel(writer, sheet_name='Ranking Veículos')
        
        # Aba 5: Saldos de Pontos
        df_saldos_ordenado = dfs['saldos'].sort_values('capcoins', ascending=False).head(50)
        df_saldos_ordenado.to_excel(writer, sheet_name='Top Saldos', index=False)
        
        # Aba 6: Dados Brutos (Impacto)
        df_impacto_export = dfs['impacto'].copy()
        df_impacto_export = df_impacto_export[[
            'placa', 'modelo', 'marca', 'categoria', 'tipo',
            'tempo_poupado', 'combustivel_poupado_ml', 'co2_evitar_g', 'data_hora'
        ]].head(500)  # Limitar a 500 registros
        df_impacto_export.to_excel(writer, sheet_name='Dados Impacto', index=False)
        
        # Aba 7: Dados Brutos (Passagens)
        df_passagens_export = dfs['passagens'].copy()
        df_passagens_export = df_passagens_export[[
            'placa', 'modelo', 'marca', 'categoria', 'tipo',
            'capcoins_ganhos', 'data_hora'
        ]].head(500)
        df_passagens_export.to_excel(writer, sheet_name='Dados Passagens', index=False)
    
    print(f"✅ Relatório gerado: {output_path}")


def exibir_estatisticas(dfs):
    """
    Exibe estatísticas resumidas no console.
    
    Args:
        dfs (dict): Dicionário com DataFrames
    """
    
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS ECOMETRIC")
    print("="*60)
    
    print(f"\n🚘 Total de Passagens: {len(dfs['passagens'])}")
    print(f"🚗 Total de Veículos: {dfs['saldos']['placa'].nunique()}")
    print(f"🌍 Total de CO₂ Evitado: {dfs['impacto']['co2_evitar_g'].sum():.2f}g")
    print(f"⏱️ Tempo Total Economizado: {dfs['impacto']['tempo_poupado'].sum():.2f}min")
    print(f"⛽ Combustível Poupado: {dfs['impacto']['combustivel_poupado_ml'].sum():.2f}ml")
    print(f"🌳 Árvores Preservadas (equiv): {dfs['impacto']['co2_evitar_g'].sum() / 21000:.2f}")
    
    print("\n" + "-"*60)
    print("📈 ANÁLISE POR CATEGORIA")
    print("-"*60)
    print(criar_analise_por_categoria(dfs))
    
    print("\n" + "-"*60)
    print("🏆 TOP 10 VEÍCULOS")
    print("-"*60)
    print(criar_ranking_veiculos(dfs).head(10))
    
    print("\n" + "="*60)


if __name__ == "__main__":
    
    print("🔄 Extraindo dados...")
    dfs = extrair_dados_completos()
    
    print("📊 Criando análises...")
    exibir_estatisticas(dfs)
    
    print("\n💾 Gerando relatório Excel...")
    output_file = f"/mnt/user-data/outputs/relatorio_ecometric_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    gerar_relatorio_excel(dfs, output_file)