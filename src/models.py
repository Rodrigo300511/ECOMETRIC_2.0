"""
models.py - Definição de Esquema do Banco de Dados

Módulo responsável pela criação de todas as tabelas
do banco de dados Ecometric com suas relações e constraints.
"""

from .database import conectar, fechar_conexao


def criar_tabelas():
    """
    Cria todas as tabelas do banco de dados Ecometric e aplica migrações.
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # TABELA: CATEGORIAS
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        consumo_litro_hora REAL NOT NULL,
        combustivel TEXT NOT NULL,
        fator_co2 REAL NOT NULL,
        hibrido INTEGER DEFAULT 0
    )
    """)

    # =========================================================
    # TABELA: MODELOS
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT NOT NULL,
        ano INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        UNIQUE(nome, marca, ano)
    )
    """)

    # =========================================================
    # TABELA: VEÍCULOS
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL UNIQUE,
        modelo_id INTEGER NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (modelo_id) REFERENCES modelos(id)
    )
    """)

    # =========================================================
    # TABELA: PASSAGENS
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'shopping',
        capcoins_ganhos INTEGER DEFAULT 0,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: IMPACTO AMBIENTAL
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS impacto_ambiental (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'shopping',
        tempo_poupado REAL NOT NULL,
        combustivel_poupado_ml REAL NOT NULL,
        co2_evitar_g REAL NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: SALDO CAPCOINS
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saldo_capcoins (
        placa TEXT PRIMARY KEY,
        saldo INTEGER DEFAULT 0,
        atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: RECOMPENSAS (Atualizada com Estoque)
    # =========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recompensas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        custo INTEGER NOT NULL,
        descricao TEXT,
        categoria TEXT,
        estoque INTEGER DEFAULT 0
    )
    """)

    # ---------------------------------------------------------
    # MIGRAÇÃO AUTOMÁTICA: Garante que a coluna estoque exista
    # ---------------------------------------------------------
    try:
        cursor.execute("SELECT estoque FROM recompensas LIMIT 1")
    except Exception:
        # Se falhar, significa que a coluna estoque não existe no banco atual
        try:
            cursor.execute("ALTER TABLE recompensas ADD COLUMN estoque INTEGER DEFAULT 0")
            conn.commit()
            print("🔄 Banco atualizado: Coluna 'estoque' adicionada com sucesso.")
        except Exception as e:
            print(f"⚠️ Erro ao aplicar migração de estoque: {e}")

    conn.commit()
    fechar_conexao(conn)

    print("✅ Estrutura do banco criada/verificada com sucesso!")