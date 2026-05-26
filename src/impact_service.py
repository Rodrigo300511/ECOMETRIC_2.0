"""
impact_service.py - Cálculos de Impacto Ambiental

Módulo responsável por:
- Calcular impacto ambiental das passagens
- Gerar equivalências (árvores, folhas de papel)
- Criar painéis de impacto por veículo
- Gerar rankings e métricas globais
"""

from .database import conectar, fechar_conexao


# =========================================================
# CONSTANTES E FATORES DE CÁLCULO
# =========================================================

# Folhas de papel economizadas por grama de CO2 evitado
# 1 árvore = 21kg de CO2 absorvida em 1 ano
# 1 resma (500 folhas) = ~2,3kg de CO2 para produzir
CO2_POR_FOLHA = 5  # gramas

# CO2 absorvido por árvore em sua vida útil
CO2_POR_ARVORE = 21000  # gramas

# Tempo padrão em fila (sem Taggy)
TEMPO_FILA_SHOPPING = 10  # minutos


def comparar_co2(placa, tipo="shopping"):
    """
    Calcula o impacto ambiental de uma passagem com Taggy.
    
    Args:
        placa (str): Placa do veículo
        tipo (str): Tipo de evento (padrão: "shopping")
    
    Returns:
        dict: Dicionário com:
            - tipo: tipo do evento
            - combustivel: tipo de combustível
            - hibrido: se é veículo híbrido
            - tempo_poupado_min: minutos economizados
            - combustivel_poupado_ml: ml economizado
            - co2_evitar_g: gramas de CO2 evitadas
    
    Raises:
        ValueError: Se veículo não for encontrado
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # BUSCAR DADOS DO VEÍCULO
    # =====================================================

    cursor.execute("""
        SELECT
            c.consumo_litro_hora,
            c.combustivel,
            c.fator_co2,
            c.hibrido

        FROM veiculos v
        JOIN modelos m ON v.modelo_id = m.id
        JOIN categorias c ON m.categoria_id = c.id
        WHERE v.placa = ?
    """, (placa,))

    res = cursor.fetchone()

    if not res:
        fechar_conexao(conn)
        raise ValueError("❌ Veículo não encontrado")

    consumo_litro_hora, combustivel, fator_co2, hibrido = res

    # =====================================================
    # CALCULAR TEMPO POUPADO
    # =====================================================
    # Para shopping: média de 10 minutos em fila
    # Com Taggy: reduz para ~2 minutos (estacionamento direto)
    
    tempo_sem_tag = TEMPO_FILA_SHOPPING
    tempo_com_tag = 2
    tempo_poupado = tempo_sem_tag - tempo_com_tag

    # =====================================================
    # CALCULAR COMBUSTÍVEL POUPADO
    # =====================================================
    # Apenas em marcha lenta (fila)
    
    litros_poupados = consumo_litro_hora * (tempo_poupado / 60)
    combustivel_poupado_ml = litros_poupados * 1000

    # =====================================================
    # CALCULAR CO2 EVITADO
    # =====================================================
    
    co2_evitar_g = litros_poupados * fator_co2

    # =====================================================
    # REGISTRAR IMPACTO
    # =====================================================

    cursor.execute("""
        INSERT INTO impacto_ambiental (
            placa,
            tipo,
            tempo_poupado,
            combustivel_poupado_ml,
            co2_evitar_g
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        placa,
        tipo,
        round(tempo_poupado, 2),
        round(combustivel_poupado_ml, 2),
        round(co2_evitar_g, 2)
    ))

    conn.commit()
    fechar_conexao(conn)

    return {
        "tipo": tipo,
        "combustivel": combustivel,
        "hibrido": bool(hibrido),
        "tempo_poupado_min": round(tempo_poupado, 2),
        "combustivel_poupado_ml": round(combustivel_poupado_ml, 2),
        "co2_evitar_g": round(co2_evitar_g, 2)
    }


def calcular_equivalencia_folhas(co2_total):
    """
    Converte CO2 evitado em folhas de papel economizadas.
    
    Args:
        co2_total (float): Total de CO2 em gramas
    
    Returns:
        int: Número de folhas equivalentes
    """
    return int(co2_total / CO2_POR_FOLHA)


def calcular_equivalencia_arvores(co2_total):
    """
    Converte CO2 evitado em árvores preservadas.
    
    Args:
        co2_total (float): Total de CO2 em gramas
    
    Returns:
        float: Número de árvores equivalentes
    """
    return round(co2_total / CO2_POR_ARVORE, 2)


def obter_painel_impacto(placa):
    """
    Gera painel completo de impacto ambiental por veículo.
    
    Args:
        placa (str): Placa do veículo
    
    Returns:
        dict: Dashboard com métricas de impacto e gamificação
    
    Raises:
        ValueError: Se veículo não for encontrado
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # Validar veículo
    cursor.execute("""
        SELECT id FROM veiculos WHERE placa = ?
    """, (placa,))
    
    if not cursor.fetchone():
        fechar_conexao(conn)
        raise ValueError("❌ Veículo não encontrado")

    # =====================================================
    # SALDO DE CAPCOINS
    # =====================================================

    cursor.execute("""
        SELECT saldo
        FROM saldo_capcoins
        WHERE placa = ?
    """, (placa,))

    saldo_res = cursor.fetchone()
    saldo = saldo_res[0] if saldo_res else 0

    # =====================================================
    # IMPACTO TOTAL
    # =====================================================

    cursor.execute("""
        SELECT
            SUM(tempo_poupado),
            SUM(combustivel_poupado_ml),
            SUM(co2_evitar_g)
        FROM impacto_ambiental
        WHERE placa = ?
    """, (placa,))

    impacto = cursor.fetchone()

    tempo_total = impacto[0] or 0
    combustivel_total = impacto[1] or 0
    co2_total = impacto[2] or 0

    # =====================================================
    # TOTAL DE PASSAGENS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM passagens
        WHERE placa = ?
    """, (placa,))

    total_passagens = cursor.fetchone()[0]

    fechar_conexao(conn)

    # =====================================================
    # EQUIVALÊNCIAS
    # =====================================================

    folhas = calcular_equivalencia_folhas(co2_total)
    arvores = calcular_equivalencia_arvores(co2_total)

    return {
        "saldo_capcoins": saldo,
        "total_passagens": total_passagens,
        "tempo_total_min": round(tempo_total, 2),
        "combustivel_poupado_ml": round(combustivel_total, 2),
        "co2_total_g": round(co2_total, 2),
        "folhas_poupadas": folhas,
        "equivalente_arvores": arvores
    }


def ranking_usuarios_verdes():
    """
    Gera ranking dos veículos por CO2 evitado.
    
    Returns:
        list: Lista de tuplas (placa, co2_total) ordenada
    """
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            placa,
            SUM(co2_evitar_g) as total_co2
        FROM impacto_ambiental
        GROUP BY placa
        ORDER BY total_co2 DESC
    """)

    ranking = cursor.fetchall()
    fechar_conexao(conn)

    return ranking


def metricas_globais():
    """
    Gera métricas globais de impacto ambiental.
    
    Returns:
        dict: Dicionário com:
            - co2_total_g: Total de CO2 evitado
            - tempo_total_min: Total de tempo economizado
            - combustivel_total_ml: Total de combustível poupado
            - equivalente_arvores: Árvores preservadas
            - total_passagens: Número total de passagens registradas
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # CO2 TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(co2_evitar_g)
        FROM impacto_ambiental
    """)

    co2_total = cursor.fetchone()[0] or 0

    # =====================================================
    # TEMPO TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(tempo_poupado)
        FROM impacto_ambiental
    """)

    tempo_total = cursor.fetchone()[0] or 0

    # =====================================================
    # COMBUSTÍVEL TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(combustivel_poupado_ml)
        FROM impacto_ambiental
    """)

    combustivel_total = cursor.fetchone()[0] or 0

    # =====================================================
    # TOTAL DE PASSAGENS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM passagens
    """)

    total_passagens = cursor.fetchone()[0]

    fechar_conexao(conn)

    return {
        "co2_total_g": round(co2_total, 2),
        "tempo_total_min": round(tempo_total, 2),
        "combustivel_total_ml": round(combustivel_total, 2),
        "equivalente_arvores": calcular_equivalencia_arvores(co2_total),
        "total_passagens": total_passagens
    }