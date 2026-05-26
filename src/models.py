"""
models.py - Definição de Esquema do Banco de Dados

Módulo responsável pela criação de todas as tabelas
do banco de dados Ecometric com suas relações e constraints.
"""

from .database import conectar, fechar_conexao


def criar_tabelas():
    """
    Cria todas as tabelas do banco de dados Ecometric.
    
    Tabelas criadas:
    - categorias: Perfil ambiental dos veículos
    - modelos: Modelos de carros cadastrados
    - veiculos: Veículos cadastrados por usuários
    - passagens: Registros de uso do Taggy
    - impacto_ambiental: Histórico de impacto ambiental
    - saldo_capcoins: Saldo de pontos dos usuários
    - recompensas: Catálogo de recompensas sustentáveis
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # TABELA: CATEGORIAS
    # =========================================================
    # Representa o PERFIL AMBIENTAL do veículo
    # 
    # Campos:
    # - consumo_litro_hora: consumo em marcha lenta (L/h)
    # - fator_co2: emissão de CO2 por litro (g/L)
    # - hibrido: 0=não, 1=sim
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
    # Armazena modelos de veículos disponíveis
    # Exemplos: Gol, Onix, Corolla, Compass
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT NOT NULL,
        ano INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id)
            REFERENCES categorias(id),
        UNIQUE(nome, marca, ano)
    )
    """)

    # =========================================================
    # TABELA: VEÍCULOS
    # =========================================================
    # Veículos cadastrados pelos usuários
    # Cada veículo aponta para um modelo específico
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL UNIQUE,
        modelo_id INTEGER NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (modelo_id)
            REFERENCES modelos(id)
    )
    """)

    # =========================================================
    # TABELA: PASSAGENS
    # =========================================================
    # Registra cada uso do Taggy nos shoppings
    # Inclui tipo de evento e pontos ganhos
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'shopping',
        capcoins_ganhos INTEGER DEFAULT 0,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: IMPACTO AMBIENTAL
    # =========================================================
    # Histórico detalhado do impacto ambiental
    # 
    # Unidades:
    # - tempo_poupado: minutos
    # - combustivel_poupado_ml: mililitros
    # - co2_evitar_g: gramas
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
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: SALDO CAPCOINS
    # =========================================================
    # Saldo atual de pontos por veículo/usuário
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saldo_capcoins (
        placa TEXT PRIMARY KEY,
        saldo INTEGER DEFAULT 0,
        atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
    )
    """)

    # =========================================================
    # TABELA: RECOMPENSAS
    # =========================================================
    # Catálogo de recompensas sustentáveis
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recompensas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        custo INTEGER NOT NULL,
        descricao TEXT,
        categoria TEXT
    )
    """)

    conn.commit()
    fechar_conexao(conn)

    print("✅ Estrutura do banco criada com sucesso!")