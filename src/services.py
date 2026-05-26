"""
services.py - Serviços Principais do Sistema

Módulo responsável por:
- Listar modelos disponíveis
- Cadastrar veículos
- Registrar uso do Taggy
- Gerir recompensas
"""

from datetime import datetime
from .database import conectar, fechar_conexao


# =========================================================
# LISTAGEM
# =========================================================

def listar_modelos():
    """
    Lista todos os modelos de veículos disponíveis.
    
    Returns:
        list: Lista de tuplas (id, nome, marca, ano, categoria)
    """
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.id,
            m.nome,
            m.marca,
            m.ano,
            c.nome

        FROM modelos m
        JOIN categorias c ON m.categoria_id = c.id
        ORDER BY m.nome
    """)

    modelos = cursor.fetchall()
    fechar_conexao(conn)

    return modelos


def listar_veiculos():
    """
    Lista todos os veículos cadastrados.
    
    Returns:
        list: Lista de tuplas (placa, modelo, marca, ano)
    """
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            v.placa,
            m.nome,
            m.marca,
            m.ano

        FROM veiculos v
        JOIN modelos m ON v.modelo_id = m.id
        ORDER BY v.placa
    """)

    veiculos = cursor.fetchall()
    fechar_conexao(conn)

    return veiculos


# =========================================================
# CADASTRO DE VEÍCULOS
# =========================================================

def cadastrar_veiculo_por_modelo(placa, modelo_id):
    """
    Cadastra novo veículo selecionando um modelo existente.
    
    Args:
        placa (str): Placa do veículo (formato: ABC1234)
        modelo_id (int): ID do modelo cadastrado
    
    Raises:
        ValueError: Se placa já existe ou modelo não existe
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # VALIDAR DUPLICIDADE
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM veiculos
        WHERE placa = ?
    """, (placa,))

    if cursor.fetchone():
        fechar_conexao(conn)
        raise ValueError("❌ Veículo já cadastrado")

    # =====================================================
    # VALIDAR MODELO
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM modelos
        WHERE id = ?
    """, (modelo_id,))

    if not cursor.fetchone():
        fechar_conexao(conn)
        raise ValueError("❌ Modelo não encontrado")

    # =====================================================
    # INSERIR VEÍCULO
    # =====================================================

    cursor.execute("""
        INSERT INTO veiculos (placa, modelo_id)
        VALUES (?, ?)
    """, (placa, modelo_id))

    # =====================================================
    # CRIAR SALDO INICIAL
    # =====================================================

    cursor.execute("""
        INSERT INTO saldo_capcoins (placa, saldo)
        VALUES (?, ?)
    """, (placa, 0))

    conn.commit()
    fechar_conexao(conn)


# =========================================================
# PONTUAÇÃO
# =========================================================

def registrar_uso_taggy(placa, tipo="shopping"):
    """
    Registra uso do Taggy e calcula pontos ganhos.
    
    Args:
        placa (str): Placa do veículo
        tipo (str): Tipo de evento (padrão: "shopping")
    
    Returns:
        dict: Dicionário com:
            - pontos_base: pontos da passagem
            - bonus: bônus de frequência
            - total_ganho: total de pontos ganhos
            - total_passagens_mes: passagens no mês
    
    Raises:
        ValueError: Se veículo não for encontrado
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # VALIDAR VEÍCULO
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM veiculos
        WHERE placa = ?
    """, (placa,))

    if not cursor.fetchone():
        fechar_conexao(conn)
        raise ValueError("❌ Veículo não encontrado")

    # =====================================================
    # TABELA DE PONTOS
    # =====================================================
    
    pontos_base = {
        "pedagio": 5,
        "shopping": 3,
        "condominio": 2,
        "drive_thru": 2
    }

    pontos = pontos_base.get(tipo, 1)

    # =====================================================
    # REGISTRAR PASSAGEM
    # =====================================================

    cursor.execute("""
        INSERT INTO passagens (placa, tipo, capcoins_ganhos)
        VALUES (?, ?, ?)
    """, (placa, tipo, pontos))

    # =====================================================
    # CONTAR PASSAGENS DO MÊS
    # =====================================================

    mes_atual = datetime.now().strftime("%Y-%m")

    cursor.execute("""
        SELECT COUNT(*)
        FROM passagens
        WHERE placa = ?
        AND strftime('%Y-%m', data_hora) = ?
    """, (placa, mes_atual))

    total_mes = cursor.fetchone()[0]

    # =====================================================
    # CALCULAR BÔNUS DE FREQUÊNCIA
    # =====================================================
    
    bonus = 0

    if total_mes == 10:
        bonus = 20
    elif total_mes == 20:
        bonus = 50
    elif total_mes == 40:
        bonus = 100

    total_ganho = pontos + bonus

    # =====================================================
    # ATUALIZAR SALDO
    # =====================================================

    cursor.execute("""
        SELECT saldo
        FROM saldo_capcoins
        WHERE placa = ?
    """, (placa,))

    existe = cursor.fetchone()

    if existe:
        cursor.execute("""
            UPDATE saldo_capcoins
            SET saldo = saldo + ?
            WHERE placa = ?
        """, (total_ganho, placa))
    else:
        cursor.execute("""
            INSERT INTO saldo_capcoins (placa, saldo)
            VALUES (?, ?)
        """, (placa, total_ganho))

    conn.commit()
    fechar_conexao(conn)

    return {
        "pontos_base": pontos,
        "bonus": bonus,
        "total_ganho": total_ganho,
        "total_passagens_mes": total_mes
    }


# =========================================================
# RECOMPENSAS
# =========================================================

def listar_recompensas_catalogo():
    """
    Lista catálogo completo de recompensas.
    
    Returns:
        list: Lista de tuplas (id, nome, custo, descricao, categoria)
    """
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            custo,
            descricao,
            categoria

        FROM recompensas
        ORDER BY custo ASC
    """)

    recompensas = cursor.fetchall()
    fechar_conexao(conn)

    return recompensas


def resgatar_recompensa(placa, recompensa_id):
    """
    Resgata uma recompensa usando CapCoins.
    
    Args:
        placa (str): Placa do veículo
        recompensa_id (int): ID da recompensa
    
    Returns:
        dict: Dicionário com:
            - recompensa: nome da recompensa
            - saldo_restante: saldo após resgate
    
    Raises:
        ValueError: Se saldo insuficiente ou recompensa não existe
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # BUSCAR RECOMPENSA
    # =====================================================

    cursor.execute("""
        SELECT nome, custo
        FROM recompensas
        WHERE id = ?
    """, (recompensa_id,))

    recompensa = cursor.fetchone()

    if not recompensa:
        fechar_conexao(conn)
        raise ValueError("❌ Recompensa não encontrada")

    nome_recompensa, custo = recompensa

    # =====================================================
    # BUSCAR SALDO
    # =====================================================

    cursor.execute("""
        SELECT saldo
        FROM saldo_capcoins
        WHERE placa = ?
    """, (placa,))

    saldo_res = cursor.fetchone()
    saldo = saldo_res[0] if saldo_res else 0

    # =====================================================
    # VALIDAR SALDO
    # =====================================================

    if saldo < custo:
        fechar_conexao(conn)
        raise ValueError("❌ Saldo insuficiente")

    # =====================================================
    # DESCONTAR SALDO
    # =====================================================

    novo_saldo = saldo - custo

    cursor.execute("""
        UPDATE saldo_capcoins
        SET saldo = ?
        WHERE placa = ?
    """, (novo_saldo, placa))

    conn.commit()
    fechar_conexao(conn)

    return {
        "recompensa": nome_recompensa,
        "saldo_restante": novo_saldo
    }