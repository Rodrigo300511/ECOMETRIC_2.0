# 🌱 Ecometric — Dashboard de Impacto Ambiental

> **Inteligência Ambiental para Mobilidade Urbana**
> Transformando cada passagem Taggy em dados concretos de sustentabilidade.

---

# 📌 Visão Geral

O **Ecometric** é uma aplicação web desenvolvida com **Flask + SQLite** que monitora e quantifica o impacto ambiental gerado pelo uso do sistema Taggy em shoppings e estacionamentos.

A cada passagem registrada, o sistema calcula automaticamente:

* 🌿 CO₂ evitado
* ⛽ Combustível poupado
* ⏱️ Tempo economizado

Esses dados são convertidos em:

* dashboards analíticos;
* rankings sustentáveis;
* gráficos temporais;
* sistema de gamificação com **CapCoins**.

Os usuários podem acumular moedas sustentáveis e trocá-las por recompensas reais na loja integrada do sistema.

---

# 🚀 Funcionalidades Principais

| Módulo                   | Descrição                                                           |
| ------------------------ | ------------------------------------------------------------------- |
| 📊 Dashboard Global      | Métricas agregadas de CO₂, combustível, tempo e árvores preservadas |
| 👤 Área do Cliente       | Histórico individual por placa e evolução mensal                    |
| 🪙 Loja Sustentável      | Resgate de recompensas utilizando CapCoins                          |
| 🚗 Análise por Categoria | Comparativo entre Hatch, Sedan, SUV, Pickup, Híbrido e Elétrico     |
| 📈 Análise Temporal      | Evolução mensal com gráficos dinâmicos                              |
| 🏆 Ranking Verde         | Top 20 veículos com maior CO₂ evitado                               |
| 🔧 Gestão de Veículos    | Cadastro de placas e controle de saldo                              |
| ⚡ Simulador Taggy        | Simulação em tempo real de passagens                                |

---

# 🗂️ Estrutura do Projeto

```text
ECOMETRIC/
│
├── app.py
├── analytics_export.py
├── generate_mock_data.py
├── requirements.txt
├── ecometric.db
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── impact_service.py
│   ├── models.py
│   ├── seed.py
│   └── services.py
│
├── static/
│   ├── style.css
│   ├── dashboard.js
│   ├── cliente.js
│   ├── loja.js
│   ├── categorias.js
│   ├── periodos.js
│   ├── ranking.js
│   ├── veiculos.js
│   └── login.js
│
└── templates/
    ├── 404.html
    ├── 500.html
    ├── index.html
    ├── login.html
    ├── cliente.html
    ├── loja.html
    ├── categorias.html
    ├── periodos.html
    ├── ranking.html
    └── veiculos.html
```

---

# 🔐 Credenciais de Acesso

## 👨‍💼 Administrador

| Campo   | Valor      |
| ------- | ---------- |
| Usuário | `admin`    |
| Senha   | `admin123` |

---

## 👤 Cliente

| Campo         | Valor                         |
| ------------- | ----------------------------- |
| Usuário/Placa | Qualquer placa gerada no mock |
| Senha         | `123456`                      |

### Exemplo de placas:

```text
SOA5G69
ABC1234
XYZ8A91
```

> As placas disponíveis podem ser visualizadas na aba **Veículos** do painel administrativo.

---

# 📦 Instalação e Execução

## Pré-requisitos

* Python 3.9+
* pip

---

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/ecometric.git
cd ecometric
```

---

## 2️⃣ Criar ambiente virtual

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Instalar dependências

```bash
pip install flask pandas openpyxl
```

---

## 4️⃣ Inicializar banco de dados

```bash
python -c "from src.seed import popular_banco; popular_banco()"
```

---

## 5️⃣ Gerar dados fictícios (Opcional)

```bash
python generate_mock_data.py
```

---

## 6️⃣ Executar aplicação

```bash
python app.py
```

Acesse em:

```text
http://localhost:5000
```

---

# 📊 Scripts Analíticos

O projeto inclui scripts auxiliares para exportação de dados:

| Script                  | Função                   |
| ----------------------- | ------------------------ |
| `analytics_export.py`   | Exporta dados para Excel |
| `generate_mock_data.py` | Gera dados simulados     |

Ideal para integração com:

* Power BI
* Excel
* Ferramentas de BI

---

# 🌐 Arquitetura da API

Todos os endpoints retornam dados no formato **JSON** seguindo o padrão REST.

---

# 🖥️ Endpoints de Telas

| Método | Endpoint      | Restrição   | Descrição             |
| ------ | ------------- | ----------- | --------------------- |
| GET    | `/`           | Livre/Admin | Dashboard principal   |
| GET    | `/categorias` | Livre/Admin | Análise por categoria |
| GET    | `/periodos`   | Livre/Admin | Evolução temporal     |
| GET    | `/ranking`    | Livre/Admin | Ranking sustentável   |
| GET    | `/veiculos`   | Livre/Admin | Gestão de veículos    |
| GET    | `/loja`       | Cliente     | Loja de recompensas   |
| GET    | `/health`     | Livre       | Health check          |

---

# 🔌 Endpoints da API

| Método | Endpoint                  | Descrição              |
| ------ | ------------------------- | ---------------------- |
| GET    | `/api/metricas`           | Métricas globais       |
| GET    | `/api/categorias`         | Impacto por categoria  |
| GET    | `/api/periodos`           | Evolução mensal        |
| GET    | `/api/ranking`            | Ranking verde          |
| GET    | `/api/veiculos`           | Lista de veículos      |
| GET    | `/api/recompensas`        | Catálogo da loja       |
| POST   | `/api/loja/resgatar`      | Resgate de recompensas |
| POST   | `/api/cliente/cadastro`   | Cadastro de veículo    |
| GET    | `/api/cliente/<placa>`    | Painel do cliente      |
| POST   | `/api/cliente/usar_taggy` | Simulação de uso       |

---

# 🗄️ Banco de Dados

O sistema utiliza **SQLite**, com geração automática do arquivo:

```text
ecometric.db
```

---

## 📐 Relacionamento das Tabelas

```text
categorias ──< modelos ──< veiculos ──< passagens
                                 ├──< impacto_ambiental
                                 └── saldo_capcoins

recompensas
```

---

## 📋 Tabelas

| Tabela            | Descrição                     |
| ----------------- | ----------------------------- |
| categorias        | Perfil ambiental dos veículos |
| modelos           | Modelos cadastrados           |
| veiculos          | Veículos registrados          |
| passagens         | Histórico de uso              |
| impacto_ambiental | Métricas ambientais           |
| saldo_capcoins    | Saldo de moedas               |
| recompensas       | Catálogo da loja              |

---

# 🌿 Metodologia de Cálculo

## CO₂ Evitado

O cálculo baseia-se no tempo economizado em filas:

```text
tempo_poupado   = 10 min - 2 min
litros_poupados = consumo_L/h × (tempo_poupado / 60)
CO₂_evitado_g   = litros_poupados × fator_CO₂
```

---

# 🌳 Equivalências Ambientais

| Equivalência           | Fator                      |
| ---------------------- | -------------------------- |
| 📄 Folhas de papel     | 1 folha = 5g CO₂           |
| 🌳 Árvores preservadas | 1 árvore = 21.000g CO₂/ano |

---

# 🪙 Sistema de Gamificação — CapCoins

## Pontuação por Passagem

| Tipo       | Pontos     |
| ---------- | ---------- |
| Pedágio    | 5 CapCoins |
| Shopping   | 3 CapCoins |
| Condomínio | 2 CapCoins |
| Drive-thru | 2 CapCoins |

---

# 🛍️ Catálogo da Loja

| Recompensa                        | Categoria   | Custo |
| --------------------------------- | ----------- | ----- |
| Doação para Reflorestamento       | Sustentável | 100   |
| Lavagem Ecológica                 | Serviço     | 150   |
| Crédito Bike Itaú                 | Serviço     | 200   |
| Plantio de Árvore com Certificado | Sustentável | 300   |
| Desconto Plano Taggy (30%)        | Serviço     | 350   |

---

# ⚙️ Stack Tecnológica

## Backend

* Python 3.9+
* Flask
* SQLite 3

---

## Frontend

* HTML5
* CSS3
* JavaScript (ES2020+)
* Chart.js 3.9
* Axios 1.4

---

# 📄 Licença

```text
🌱 Ecometric © 2026
Inteligência Ambiental para Mobilidade Urbana
Reduzindo emissões, um trajeto por vez.
```
