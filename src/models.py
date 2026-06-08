"""
models.py - Definição de Esquema do Banco de Dados

Módulo responsável pela criação de todas as tabelas
do banco de dados Ecometric com suas relações e constraints.
"""

from .database import conectar, fechar_conexao


def criar_tabelas():
    """
<<<<<<< HEAD
    Cria todas as tabelas do banco de dados Ecometric e aplica migrações.
=======
    Cria todas as tabelas do banco de dados Ecometric.
    
    Tabelas criadas:
    - categorias: Perfil ambiental dos veículos
    - modelos: Modelos de carros cadastrados
    - veiculos: Veículos cadastrados por usuários
    - passagens: Registros de uso do Taggy
    - impacto_ambiental: Histórico de impacto ambiental
    - saldo_capcoins: Saldo de pontos dos usuários
    - recompensas: Catálogo de recompensas sustentáveis
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    """
    
    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # TABELA: CATEGORIAS
    # =========================================================
<<<<<<< HEAD
=======
    # Representa o PERFIL AMBIENTAL do veículo
    # 
    # Campos:
    # - consumo_litro_hora: consumo em marcha lenta (L/h)
    # - fator_co2: emissão de CO2 por litro (g/L)
    # - hibrido: 0=não, 1=sim
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
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
<<<<<<< HEAD
=======
    # Armazena modelos de veículos disponíveis
    # Exemplos: Gol, Onix, Corolla, Compass
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT NOT NULL,
        ano INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
<<<<<<< HEAD
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
=======
        FOREIGN KEY (categoria_id)
            REFERENCES categorias(id),
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
        UNIQUE(nome, marca, ano)
    )
    """)

    # =========================================================
    # TABELA: VEÍCULOS
    # =========================================================
<<<<<<< HEAD
=======
    # Veículos cadastrados pelos usuários
    # Cada veículo aponta para um modelo específico
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL UNIQUE,
        modelo_id INTEGER NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
<<<<<<< HEAD
        FOREIGN KEY (modelo_id) REFERENCES modelos(id)
=======
        FOREIGN KEY (modelo_id)
            REFERENCES modelos(id)
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    )
    """)

    # =========================================================
    # TABELA: PASSAGENS
    # =========================================================
<<<<<<< HEAD
=======
    # Registra cada uso do Taggy nos shoppings
    # Inclui tipo de evento e pontos ganhos
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'shopping',
        capcoins_ganhos INTEGER DEFAULT 0,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
<<<<<<< HEAD
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
=======
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    )
    """)

    # =========================================================
    # TABELA: IMPACTO AMBIENTAL
    # =========================================================
<<<<<<< HEAD
=======
    # Histórico detalhado do impacto ambiental
    # 
    # Unidades:
    # - tempo_poupado: minutos
    # - combustivel_poupado_ml: mililitros
    # - co2_evitar_g: gramas
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS impacto_ambiental (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'shopping',
        tempo_poupado REAL NOT NULL,
        combustivel_poupado_ml REAL NOT NULL,
        co2_evitar_g REAL NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
<<<<<<< HEAD
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
=======
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    )
    """)

    # =========================================================
    # TABELA: SALDO CAPCOINS
    # =========================================================
<<<<<<< HEAD
=======
    # Saldo atual de pontos por veículo/usuário
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saldo_capcoins (
        placa TEXT PRIMARY KEY,
        saldo INTEGER DEFAULT 0,
        atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
<<<<<<< HEAD
        FOREIGN KEY (placa) REFERENCES veiculos(placa)
=======
        FOREIGN KEY (placa)
            REFERENCES veiculos(placa)
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    )
    """)

    # =========================================================
<<<<<<< HEAD
    # TABELA: RECOMPENSAS (Atualizada com Estoque)
    # =========================================================
=======
    # TABELA: RECOMPENSAS
    # =========================================================
    # Catálogo de recompensas sustentáveis
    # =========================================================

>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recompensas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        custo INTEGER NOT NULL,
        descricao TEXT,
<<<<<<< HEAD
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
=======
        categoria TEXT
    )
    """)

    conn.commit()
    fechar_conexao(conn)

    print("✅ Estrutura do banco criada com sucesso!")
>>>>>>> 0bfa46b114c01a7d648b116acf2a68eaefa9c498
