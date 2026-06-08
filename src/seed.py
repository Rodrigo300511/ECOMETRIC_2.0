"""
seed.py - Inicialização e População do Banco de Dados

Módulo responsável por popular o banco de dados com:
- Categorias ambientais de veículos
- Modelos mais comuns em Recife/PE
- Dados de tempos em fila para shoppings
- Catálogo de recompensas sustentáveis
"""

from .database import conectar, fechar_conexao
from .models import criar_tabelas


def popular_banco():
    """
    Popula o banco de dados com dados iniciais do sistema.
    
    Cria:
    1. Categorias ambientais (Hatch, Sedan, SUV, Pickup, Híbrido, Elétrico)
    2. Modelos populares em Recife/PE
    3. Tempos de fila para shoppings
    4. Catálogo de recompensas
    """

    # Garantir que as tabelas existem
    criar_tabelas()

    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # POPULAR CATEGORIAS AMBIENTAIS
    # =========================================================
    # Dados baseados em consumo real em marcha lenta
    # Fator CO2: gramas por litro (média de mercado)
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM categorias")

    if cursor.fetchone()[0] == 0:

        categorias = [
            # Hatch Gasolina (Gol, Onix, Palio)
            (
                "Hatch",
                0.6,          # consumo_litro_hora
                "gasolina",
                2310,         # fator_co2
                0             # hibrido
            ),

            # Sedan Flex (Corolla, Civic, Etios)
            (
                "Sedan",
                0.8,
                "flex",
                2100,
                0
            ),

            # SUV Gasolina (Compass, HR-V, Creta)
            (
                "SUV",
                1.2,
                "gasolina",
                2310,
                0
            ),

            # Pickup Diesel (Hilux, S10, Ranger)
            (
                "Pickup",
                1.5,
                "diesel",
                2680,
                0
            ),

            # Híbrido (Corolla Hybrid, Prius)
            (
                "Hibrido",
                0.3,
                "hibrido",
                900,
                1
            ),

            # Elétrico (BYD Yuan Plus, Tesla, Nissan Leaf)
            (
                "Eletrico",
                0.0,
                "eletrico",
                0,
                0
            )
        ]

        cursor.executemany("""
            INSERT INTO categorias (
                nome,
                consumo_litro_hora,
                combustivel,
                fator_co2,
                hibrido
            )
            VALUES (?, ?, ?, ?, ?)
        """, categorias)

        print("✅ Categorias ambientais cadastradas!")

    # =========================================================
    # POPULAR MODELOS - RECIFE/PE
    # =========================================================
    # Modelos mais populares na região metropolitana
    # de Pernambuco (Recife, Jaboatão, Olinda, Paulista)
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM modelos")

    if cursor.fetchone()[0] == 0:

        modelos = [
            # Hatch (categoria_id = 1)
            ("Gol", "Volkswagen", 2023, 1),
            ("Onix", "Chevrolet", 2023, 1),
            ("Palio", "Fiat", 2022, 1),
            ("Prisma", "Chevrolet", 2022, 1),

            # Sedan (categoria_id = 2)
            ("Corolla", "Toyota", 2023, 2),
            ("Civic", "Honda", 2023, 2),
            ("Etios", "Toyota", 2022, 2),
            ("Versa", "Nissan", 2022, 2),

            # SUV (categoria_id = 3)
            ("Compass", "Jeep", 2023, 3),
            ("HR-V", "Honda", 2023, 3),
            ("Creta", "Hyundai", 2023, 3),
            ("Tracker", "Chevrolet", 2022, 3),

            # Pickup (categoria_id = 4)
            ("Hilux", "Toyota", 2023, 4),
            ("S10", "Chevrolet", 2022, 4),
            ("Ranger", "Ford", 2022, 4),

            # Híbrido (categoria_id = 5)
            ("Corolla Hybrid", "Toyota", 2023, 5),
            ("Prius", "Toyota", 2022, 5),

            # Elétrico (categoria_id = 6)
            ("BYD Yuan Plus", "BYD", 2023, 6),
            ("Nissan Leaf", "Nissan", 2023, 6),
        ]

        cursor.executemany("""
            INSERT INTO modelos (
                nome,
                marca,
                ano,
                categoria_id
            )
            VALUES (?, ?, ?, ?)
        """, modelos)

        print("✅ Modelos cadastrados!")

    # =========================================================
    # POPULAR TEMPOS DE FILA - SHOPPINGS RECIFE/PE
    # =========================================================
    # Baseado em dados reais de shoppings populares:
    # - Shopping Recife
    # - Shopping Guararapes
    # - Shopping Tacaruna
    # - Aeroclube Pátio
    # 
    # Tempo em MINUTOS (marcha lenta em fila)
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM passagens")

    # Não vamos pré-popular passagens aqui
    # Elas serão geradas pelo script de mock data

    # =========================================================
    # POPULAR RECOMPENSAS SUSTENTÁVEIS
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM recompensas")

    if cursor.fetchone()[0] == 0:

        recompensas = [
            (
                "Doação para Reflorestamento",
                100,
                "Contribua para o plantio de árvores em Pernambuco",
                "sustentavel"
            ),

            (
                "Ecobag Sustentável",
                150,
                "Bolsa reutilizável de algodão orgânico 100%",
                "produto"
            ),

            (
                "Lavagem Ecológica",
                150,
                "Desconto em lavagem sem água de sua preferência",
                "servico"
            ),

            (
                "Crédito Bike Itaú",
                200,
                "Crédito para usar em compartilhamento de bicicletas",
                "mobilidade"
            ),

            (
                "Garrafa Reutilizável",
                250,
                "Garrafa inox de alta qualidade - 750ml",
                "produto"
            ),

            (
                "Plantio de Árvore com Certificado",
                300,
                "Plante uma árvore nativa e receba certificado",
                "sustentavel"
            ),

            (
                "Desconto Plano Taggy",
                350,
                "30% de desconto na mensalidade do próximo mês",
                "servico"
            ),

            (
                "Cesta de Produtos Orgânicos",
                400,
                "Cesta com produtos locais e orgânicos",
                "produto"
            ),

            (
                "Auditoria Carbono Gratuita",
                200,
                "Relatório detalhado do seu impacto ambiental",
                "servico"
            ),

            (
                "Oficina de Sustentabilidade",
                250,
                "Participação em workshop sobre mobilidade verde",
                "educacao"
            )
        ]

        cursor.executemany("""
            INSERT INTO recompensas (
                nome,
                custo,
                descricao,
                categoria
            )
            VALUES (?, ?, ?, ?)
        """, recompensas)

        print("✅ Catálogo de recompensas cadastrado!")

    # =========================================================
    # FINALIZAR
    # =========================================================

    conn.commit()
    fechar_conexao(conn)

    print("✅ Banco populado com sucesso!")


if __name__ == "__main__":
    popular_banco()