"""
generate_mock_data.py - Gerador de Dados Mockados

Script responsável por gerar 1000 registros realistas de passagens
em shoppings da região metropolitana de Pernambuco (Recife, Jaboatão,
Olinda, Paulista) para demonstração e testes do sistema.
"""

import random
from datetime import datetime, timedelta
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.database import conectar, fechar_conexao


# =========================================================
# CONFIGURAÇÕES
# =========================================================

SHOPPINGS_RECIFE = [
    "Shopping Recife",
    "Shopping Guararapes",
    "Shopping Tacaruna",
    "Aeroclube Pátio",
    "Shopping Plaza"
]

TIPOS_VEICULOS = [
    (1, 0.6, 2310, "Hatch"),      # Hatch - Gol, Onix
    (2, 0.8, 2100, "Sedan"),      # Sedan - Corolla
    (3, 1.2, 2310, "SUV"),        # SUV - Compass
    (4, 1.5, 2680, "Pickup"),     # Pickup - Hilux
    (5, 0.3, 900, "Hibrido"),     # Híbrido
    (6, 0.0, 0, "Eletrico"),      # Elétrico
]

# Placas aleatórias estilo brasileiro
FABRICANTES = [
    "VW", "GM", "FD", "TY", "HND", "JP", "BYD"
]

# Shoppings de Recife e região metropolitana de Pernambuco
SHOPPINGS_COORDS = {
    "Shopping Recife": ("Recife", -8.0476, -34.8770),
    "Shopping Guararapes": ("Jaboatão", -8.1180, -35.0036),
    "Shopping Tacaruna": ("Recife", -8.0530, -34.8820),
    "Aeroclube Pátio": ("Paulista", -7.9340, -34.8620),
    "Shopping Plaza": ("Olinda", -8.0030, -34.8550)
}


def gerar_placa():
    """
    Gera placa de veículo aleatória no formato ABC1234.
    
    Returns:
        str: Placa simulada
    """
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numeros = ''.join(random.choices('0123456789', k=4))
    return f"{letras}{numeros}"


def gerar_dados_mockados(quantidade=1000):
    """
    Gera registros mockados de passagens em shoppings.
    
    Args:
        quantidade (int): Número de registros a gerar (padrão: 1000)
    
    Retorna:
        None - Registra dados no banco de dados
    """
    
    conn = conectar()
    cursor = conn.cursor()

    print(f"🔄 Gerando {quantidade} registros mockados...")

    # =========================================================
    # LISTAR VEÍCULOS EXISTENTES
    # =========================================================

    cursor.execute("""
        SELECT placa, modelo_id
        FROM veiculos
    """)

    veiculos_existentes = cursor.fetchall()

    if not veiculos_existentes:
        print("⚠️ Nenhum veículo cadastrado. Criando veículos de teste...")
        
        # Obter modelos por categoria
        cursor.execute("""
            SELECT id, categoria_id, nome
            FROM modelos
        """)
        modelos = cursor.fetchall()
        
        # Criar alguns veículos para teste
        for i in range(50):
            modelo_escolhido = random.choice(modelos)
            placa = gerar_placa()
            
            # Verificar se placa já existe
            cursor.execute("""
                SELECT id FROM veiculos WHERE placa = ?
            """, (placa,))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO veiculos (placa, modelo_id)
                    VALUES (?, ?)
                """, (placa, modelo_escolhido[0]))
                
                cursor.execute("""
                    INSERT INTO saldo_capcoins (placa, saldo)
                    VALUES (?, ?)
                """, (placa, 0))
        
        conn.commit()
        
        cursor.execute("""
            SELECT placa, modelo_id
            FROM veiculos
        """)
        veiculos_existentes = cursor.fetchall()

    # =========================================================
    # GERAR REGISTROS DE PASSAGENS
    # =========================================================

    registros_passagens = []
    registros_impacto = []
    
    data_inicio = datetime.now() - timedelta(days=180)  # Últimos 6 meses

    for _ in range(quantidade):
        
        # Selecionar veículo aleatório
        placa, modelo_id = random.choice(veiculos_existentes)

        # Obter dados do modelo
        cursor.execute("""
            SELECT c.consumo_litro_hora, c.fator_co2, c.hibrido, m.categoria_id
            FROM modelos m
            JOIN categorias c ON m.categoria_id = c.id
            WHERE m.id = ?
        """, (modelo_id,))
        
        dados_modelo = cursor.fetchone()
        if not dados_modelo:
            continue
            
        consumo_litro_hora, fator_co2, hibrido, categoria_id = dados_modelo

        # Data aleatória nos últimos 6 meses
        dias_atras = random.randint(0, 180)
        horas = random.randint(6, 22)  # Entre 6h e 22h
        minutos = random.randint(0, 59)
        
        data_passagem = data_inicio + timedelta(
            days=dias_atras,
            hours=horas,
            minutes=minutos
        )

        # Shopping aleatório
        shopping = random.choice(SHOPPINGS_RECIFE)

        # Tempo poupado (8 a 12 minutos)
        tempo_poupado = random.uniform(8, 12)

        # Combustível poupado
        litros_poupados = consumo_litro_hora * (tempo_poupado / 60)
        combustivel_poupado_ml = litros_poupados * 1000

        # CO2 evitado
        co2_evitar_g = litros_poupados * fator_co2

        # Pontos ganhos
        pontos_base = 3  # shopping é 3 pontos
        
        registros_passagens.append((
            placa,
            "shopping",
            pontos_base,
            data_passagem.isoformat()
        ))

        registros_impacto.append((
            placa,
            "shopping",
            round(tempo_poupado, 2),
            round(combustivel_poupado_ml, 2),
            round(co2_evitar_g, 2),
            data_passagem.isoformat()
        ))

    # =========================================================
    # INSERIR REGISTROS
    # =========================================================

    cursor.executemany("""
        INSERT INTO passagens (placa, tipo, capcoins_ganhos, data_hora)
        VALUES (?, ?, ?, ?)
    """, registros_passagens)

    cursor.executemany("""
        INSERT INTO impacto_ambiental (
            placa,
            tipo,
            tempo_poupado,
            combustivel_poupado_ml,
            co2_evitar_g,
            data_hora
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, registros_impacto)

    # =========================================================
    # ATUALIZAR SALDOS
    # =========================================================

    cursor.execute("""
        SELECT placa, SUM(capcoins_ganhos) as total
        FROM passagens
        GROUP BY placa
    """)

    saldos = cursor.fetchall()

    for placa, total in saldos:
        cursor.execute("""
            INSERT INTO saldo_capcoins (placa, saldo)
            VALUES (?, ?)
            ON CONFLICT(placa) DO UPDATE SET saldo = ?
        """, (placa, total, total))

    conn.commit()
    fechar_conexao(conn)

    print(f"✅ {quantidade} registros gerados com sucesso!")
    print(f"📊 Veículos com dados: {len(set(placa for placa, _ in veiculos_existentes))}")


if __name__ == "__main__":
    quantidade = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    gerar_dados_mockados(quantidade)