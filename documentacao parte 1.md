# 📚 Documentação Completa - Ecometric

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Projeto](#arquitetura-do-projeto)
3. [Instalação e Setup](#instalação-e-setup)
4. [Estrutura de Pastas](#estrutura-de-pastas)
5. [Módulos e Funcionalidades](#módulos-e-funcionalidades)
6. [API REST](#api-rest)
7. [Dashboard e Visualizações](#dashboard-e-visualizações)
8. [Análise de Dados e Excel](#análise-de-dados-e-excel)
9. [Como Usar](#como-usar)
10. [Troubleshooting](#troubleshooting)

---

## 🌱 Visão Geral

**Ecometric** é uma plataforma inteligente de monitoramento de impacto ambiental para mobilidade urbana em Recife, Pernambuco. O sistema transforma o uso de tags RFID (Taggy) em estacionamentos e shoppings em dados mensuráveis de sustentabilidade.

### Objetivos Principais
- 📊 **Medir** o impacto ambiental do uso de Taggy
- 🎮 **Gamificar** a experiência através de pontos (CapCoins)
- 🌍 **Visualizar** equivalências ambientais (árvores preservadas, folhas de papel economizadas)
- 📈 **Analisar** dados por categoria de veículo, período e rankings
- 💾 **Exportar** relatórios em Excel para análise detalhada

### Escopo do MVP
- Foco em **shopping centers** da Região Metropolitana de Pernambuco
- Banco de dados local com modelos **comuns em Recife/PE**
- 1000 registros mockados para demonstração
- Dashboard responsivo com gráficos interativos
- Relatórios exportáveis em Excel

---

## 🏗️ Arquitetura do Projeto

### Stack Tecnológico

```
Frontend:
├── HTML5 (Templates Jinja2)
├── CSS3 (Design System com CSS Variables)
└── JavaScript (Axios + Chart.js)

Backend:
├── Python 3.10+
├── Flask (Microframework web)
├── SQLite3 (Banco de dados local)
└── Pandas (Análise de dados)

Deployment:
└── Local (Flask development server ou production WSGI)
```

### Fluxo de Dados

```
┌─────────────────────────────────────┐
│   BASE DE DADOS SQLITE              │
│   ecometric.db                      │
│                                     │
│  • veiculos                         │
│  • modelos                          │
│  • categorias                       │
│  • passagens                        │
│  • impacto_ambiental                │
│  • saldo_capcoins                   │
│  • recompensas                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   FLASK APP (Backend)               │
│                                     │
│  app.py                             │
│  ├── /api/metricas                  │
│  ├── /api/categorias                │
│  ├── /api/periodos                  │
│  ├── /api/ranking                   │
│  └── /api/veiculos                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   DASHBOARD WEB (Frontend)          │
│                                     │
│  / (Dashboard Principal)            │
│  /categorias (Análise por tipo)     │
│  /periodos (Análise temporal)       │
│  /ranking (Ranking ESG)             │
│  /veiculos (Lista completa)         │
└─────────────────────────────────────┘

     JSON API    <──►    Browser
```

---

## ⚙️ Instalação e Setup

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Terminal/CMD
- Navegador moderno (Chrome, Firefox, Safari)

### Passo 1: Clonar/Preparar Projeto
```bash
# Navegue para o diretório do projeto
cd ecometric
```

### Passo 2: Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Inicializar Banco de Dados
```bash
# Cria as tabelas
python -c "from src.seed import popular_banco; popular_banco()"
```

### Passo 5: Gerar Dados de Demonstração
```bash
# Gera 1000 registros mockados
python generate_mock_data.py 1000
```

### Passo 6: Iniciar Dashboard
```bash
python app.py
```

Acesse: **http://localhost:5000**

### Passo 7: (Opcional) Gerar Relatório Excel
```bash
python analytics_export.py
```

Arquivo gerado: `relatorio_ecometric_YYYYMMDD_HHMMSS.xlsx`

---

## 📁 Estrutura de Pastas

```
ecometric/
│
├── src/                          # Código-fonte principal
│   ├── __init__.py
│   ├── database.py              # Conexão com SQLite
│   ├── models.py                # Definição de tabelas
│   ├── seed.py                  # Inicialização de dados
│   ├── services.py              # CRUD de veículos
│   └── impact_service.py        # Cálculos de impacto ambiental
│
├── templates/                    # Templates HTML (Jinja2)
│   ├── index.html               # Dashboard principal
│   ├── categorias.html          # Análise por categoria
│   ├── periodos.html            # Análise temporal
│   ├── ranking.html             # Ranking ESG
│   ├── veiculos.html            # Lista de veículos
│   ├── 404.html                 # Erro 404
│   └── 500.html                 # Erro 500
│
├── static/
│   ├── css/
│   │   └── style.css            # Estilos principais (Design System)
│   └── js/
│       ├── dashboard.js         # Script principal do dashboard
│       ├── categorias.js        # Script de análise por categoria
│       ├── periodos.js          # Script de análise temporal
│       ├── ranking.js           # Script de ranking
│       └── veiculos.js          # Script de lista de veículos
│
├── app.py                       # Aplicação Flask
├── generate_mock_data.py        # Gerador de dados mockados (1000 registros)
├── analytics_export.py          # Exportador para Excel
├── requirements.txt             # Dependências Python
├── ecometric.db                 # Banco de dados SQLite (gerado)
└── README.md                    # Este arquivo

```

---

## 🔧 Módulos e Funcionalidades

### 1. `database.py` - Gerenciamento de Banco de Dados

**Responsabilidades:**
- Estabelecer conexão com SQLite
- Gerenciar ciclo de vida das conexões

**Funções Principais:**
```python
def conectar() -> sqlite3.Connection
    """Retorna conexão ativa com banco de dados"""

def fechar_conexao(conn: sqlite3.Connection)
    """Fecha conexão de forma segura"""
```

**Exemplo de Uso:**
```python
from src.database import conectar, fechar_conexao

conn = conectar()
cursor = conn.cursor()
cursor.execute("SELECT * FROM veiculos")
veiculos = cursor.fetchall()
fechar_conexao(conn)
```

---

### 2. `models.py` - Definição de Esquema

**Responsabilidades:**
- Criar tabelas do banco de dados
- Definir relacionamentos entre tabelas

**Tabelas Criadas:**

#### `categorias`
Perfil ambiental dos veículos
```
id (PK)
nome (UNIQUE)
consumo_litro_hora (REAL) - consumo em marcha lenta
combustivel (TEXT) - gasolina, flex, diesel, híbrido, elétrico
fator_co2 (REAL) - gramas de CO2 por litro
hibrido (INTEGER) - 0 ou 1
```

#### `modelos`
Modelos de carros cadastrados
```
id (PK)
nome (TEXT)
marca (TEXT)
ano (INTEGER)
categoria_id (FK) → categorias.id
```

#### `veiculos`
Veículos cadastrados pelos usuários
```
id (PK)
placa (UNIQUE) - ABC1234
modelo_id (FK) → modelos.id
data_cadastro (DATETIME)
```

#### `passagens`
Registros de uso do Taggy
```
id (PK)
placa (FK) → veiculos.placa
tipo (TEXT) - 'shopping'
capcoins_ganhos (INTEGER) - pontos ganhados
data_hora (DATETIME)
```

#### `impacto_ambiental`
Histórico detalhado de impacto
```
id (PK)
placa (FK) → veiculos.placa
tipo (TEXT) - tipo de evento
tempo_poupado (REAL) - minutos
combustivel_poupado_ml (REAL) - mililitros
co2_evitar_g (REAL) - gramas de CO2
data_hora (DATETIME)
```

#### `saldo_capcoins`
Saldo de pontos por veículo
```
placa (PK) → veiculos.placa
saldo (INTEGER) - pontos acumulados
atualizado_em (DATETIME)
```

#### `recompensas`
Catálogo de recompensas sustentáveis
```
id (PK)
nome (TEXT)
custo (INTEGER) - CapCoins necessários
descricao (TEXT)
categoria (TEXT) - tipo de recompensa
```

---

### 3. `seed.py` - População Inicial de Dados

**Responsabilidades:**
- Popular banco com categorias, modelos e recompensas iniciais
- Preparar dados de exemplo para Recife/PE

**Categorias Criadas:**
1. **Hatch** (0.6 L/h) - Gol, Onix, Palio
2. **Sedan** (0.8 L/h) - Corolla, Civic
3. **SUV** (1.2 L/h) - Compass, HR-V
4. **Pickup** (1.5 L/h) - Hilux, S10
5. **Híbrido** (0.3 L/h) - Corolla Hybrid
6. **Elétrico** (0 L/h) - BYD Yuan, Nissan Leaf

**Modelos Populares (Recife/PE):**
- 18 modelos de carros comuns na região

**Tempos em Fila (Shoppings):**
- Sem Taggy: ~10 minutos
- Com Taggy: ~2 minutos
- **Tempo poupado: 8 minutos por passagem**

**Recompensas Sustentáveis:**
- 100 CapCoins: Doação para reflorestamento
- 150 CapCoins: Ecobag ou lavagem ecológica
- 300 CapCoins: Plantio de árvore
- 400 CapCoins: Cesta orgânica

---

### 4. `services.py` - Operações CRUD

**Funções Principais:**

#### `listar_modelos()` → List[Tuple]
Retorna todos os modelos disponíveis
```python
resultado = [
    (1, 'Gol', 'Volkswagen', 2023, 'Hatch'),
    (2, 'Corolla', 'Toyota', 2023, 'Sedan'),
    ...
]
```

#### `cadastrar_veiculo_por_modelo(placa: str, modelo_id: int)` → None
Cadastra novo veículo usando modelo existente
```python
cadastrar_veiculo_por_modelo('ABC1234', 1)
# Cria veículo com placa ABC1234 do modelo ID 1
```

#### `registrar_uso_taggy(placa: str, tipo: str) → Dict`
Registra passagem e calcula pontos
```python
resultado = registrar_uso_taggy('ABC1234', 'shopping')
# {
#     'pontos_base': 3,
#     'bonus': 0,
#     'total_ganho': 3,
#     'total_passagens_mes': 1
# }
```

#### `listar_recompensas_catalogo()` → List[Tuple]
Retorna catálogo de recompensas
```python
recompensas = [
    (1, 'Doação para Reflorestamento', 100, '...', 'sustentavel'),
    ...
]
```

---

### 5. `impact_service.py` - Cálculos de Impacto

**Constantes de Cálculo:**
```python
CO2_POR_FOLHA = 5              # gramas
CO2_POR_ARVORE = 21000         # gramas (vida útil)
TEMPO_FILA_SHOPPING = 10       # minutos (sem Taggy)
```

**Funções Principais:**

#### `comparar_co2(placa: str, tipo: str) → Dict`
Calcula impacto ambiental de uma passagem
```python
resultado = comparar_co2('ABC1234', 'shopping')
# {
#     'tipo': 'shopping',
#     'combustivel': 'gasolina',
#     'hibrido': False,
#     'tempo_poupado_min': 8.0,
#     'combustivel_poupado_ml': 80.0,
#     'co2_evitar_g': 184.8
# }
```

**Fórmulas Utilizadas:**
```
tempo_poupado = tempo_sem_tag - tempo_com_tag
litros_poupados = consumo_litro_hora × (tempo_poupado / 60)
combustivel_poupado_ml = litros_poupados × 1000
co2_evitar_g = litros_poupados × fator_co2
```

#### `calcular_equivalencia_arvores(co2_total: float) → float`
Converte CO2 em árvores preservadas
```python
arvores = calcular_equivalencia_arvores(21000)  # 1 árvore
```

#### `obter_painel_impacto(placa: str) → Dict`
Dashboard completo de impacto por veículo
```python
painel = obter_painel_impacto('ABC1234')
# {
#     'saldo_capcoins': 15,
#     'total_passagens': 5,
#     'tempo_total_min': 40.0,
#     'combustivel_poupado_ml': 400.0,
#     'co2_total_g': 924.0,
#     'folhas_poupadas': 184,
#     'equivalente_arvores': 0.04
# }
```

#### `ranking_usuarios_verdes()` → List[Tuple]
Ranking de veículos por CO2 evitado
```python
ranking = [
    ('ABC1234', 924.0),
    ('XYZ9876', 800.5),
    ...
]
```

#### `metricas_globais()` → Dict
Métricas agregadas de todo o sistema
```python
metricas = {
    'co2_total_g': 45000.0,
    'tempo_total_min': 2500.0,
    'combustivel_total_ml': 25000.0,
    'equivalente_arvores': 2.14,
    'total_passagens': 300
}
```