# 📚 Documentação Completa - Ecometric (Parte 2)

## 🌐 API REST

### Endpoints Disponíveis

#### `GET /`
Página principal do dashboard
- **Descrição:** Exibe métricas globais e gráficos de impacto ambiental
- **Resposta:** HTML (template index.html)
- **Status:** 200

#### `GET /api/metricas`
Retorna métricas globais do sistema
- **Descrição:** Dados agregados de impacto ambiental
- **Resposta:** JSON
```json
{
    "co2_total_g": 45000.0,
    "tempo_total_min": 2500.0,
    "combustivel_total_ml": 25000.0,
    "equivalente_arvores": 2.14,
    "total_passagens": 300
}
```
- **Status:** 200 | 500

#### `GET /api/categorias`
Análise agregada por categoria de veículo
- **Descrição:** Impacto ambiental separado por tipo de carro
- **Resposta:** JSON Array
```json
[
    {
        "categoria": "Hatch",
        "passagens": 150,
        "tempo_min": 1200.0,
        "combustivel_ml": 12000.0,
        "co2_g": 27720.0,
        "arvores_equiv": 1.32
    },
    {
        "categoria": "Sedan",
        "passagens": 100,
        "tempo_min": 800.0,
        "combustivel_ml": 6400.0,
        "co2_g": 13440.0,
        "arvores_equiv": 0.64
    }
]
```
- **Status:** 200 | 500

#### `GET /api/periodos`
Análise temporal (por mês) dos últimos 12 meses
- **Descrição:** Evolução do impacto ambiental ao longo do tempo
- **Resposta:** JSON Array
```json
[
    {
        "mes": "2024-01",
        "passagens": 25,
        "tempo_min": 200.0,
        "combustivel_ml": 2000.0,
        "co2_g": 4620.0
    },
    {
        "mes": "2024-02",
        "passagens": 28,
        "tempo_min": 224.0,
        "combustivel_ml": 2240.0,
        "co2_g": 5171.2
    }
]
```
- **Status:** 200 | 500

#### `GET /api/ranking`
Top 20 veículos por CO₂ evitado
- **Descrição:** Ranking ESG dos melhores contribuintes
- **Resposta:** JSON Array
```json
[
    {
        "posicao": 1,
        "placa": "ABC1234",
        "co2_g": 2500.0
    },
    {
        "posicao": 2,
        "placa": "XYZ9876",
        "co2_g": 2300.0
    }
]
```
- **Status:** 200 | 500

#### `GET /api/veiculos`
Lista detalhada dos veículos participantes (top 50)
- **Descrição:** Dados completos de cada veículo
- **Resposta:** JSON Array
```json
[
    {
        "placa": "ABC1234",
        "modelo": "Corolla",
        "marca": "Toyota",
        "categoria": "Sedan",
        "passagens": 15,
        "co2_g": 2500.0,
        "capcoins": 45
    }
]
```
- **Status:** 200 | 500

#### `GET /health`
Health check da aplicação
- **Descrição:** Verifica se a aplicação está rodando
- **Resposta:** JSON
```json
{"status": "ok"}
```
- **Status:** 200

---

## 📊 Dashboard e Visualizações

### Design System

O dashboard utiliza um **Design System moderno e sustentável** baseado em:

#### Paleta de Cores
```css
/* Verde Sustentável */
--primary-green: #10b981        /* Verde principal */
--dark-green: #047857            /* Verde escuro */
--light-green: #d1fae5           /* Verde claro */
--very-light-green: #f0fdf4      /* Verde muito claro */

/* Complementares */
--earth-brown: #92400e           /* Marrom terra */
--sky-blue: #0ea5e9              /* Azul céu */
--warning-orange: #f97316        /* Laranja alerta */
--success-green: #16a34a          /* Verde sucesso */
```

#### Tipografia
- **Display:** Segoe UI, system-ui
- **Body:** Segoe UI, system-ui
- **Pesos:** 600 (semi-bold), 700 (bold), 900 (black)

#### Componentes Principais

##### 1. Navbar (Navegação)
- Logo animado com emoji 🌱
- Menu responsivo com hover effects
- Indicador de página ativa
- Sticky no topo da página

##### 2. Hero Section
- Título grande e impactante
- Subtítulo explicativo
- Background com padrão sutil
- Animação ao carregar

##### 3. Metric Cards
Cards com quatro métricas principais:
- **CO₂ Evitado** (em vermelho)
- **Tempo Economizado** (em laranja)
- **Combustível Poupado** (em roxo)
- **Árvores Preservadas** (em verde)

Cada card inclui:
- Ícone emoji
- Valor numérico grande
- Unidade de medida
- Barra de progresso animada

##### 4. Gráficos Interativos
Usando **Chart.js** para visualizações:
- **Linha:** Evolução temporal
- **Barra:** Comparações por categoria
- **Doughnut:** Distribuição de impacto
- **Radar:** Comparação multidimensional

##### 5. Tabelas de Dados
- Headers com fundo verde claro
- Bordas sutis entre linhas
- Hover effect nas linhas
- Responsivo com scroll horizontal

### Páginas do Dashboard

#### 1. Dashboard Principal (/)
**Visão:** Resumo executivo do sistema
**Componentes:**
- 4 metric cards principais
- 1 gráfico de timeline (evolução)
- 2 gráficos comparativos (categoria + ranking)
- Estatísticas totais (passagens, veículos)

**Gráficos:**
```javascript
// Timeline: CO₂ e Combustível ao longo do tempo
Chart.js - Line Chart (duplo eixo Y)

// Categorias: Distribuição de impacto por tipo
Chart.js - Doughnut Chart

// Ranking: Top 10 veículos
Chart.js - Horizontal Bar Chart
```

#### 2. Análise por Categorias (/categorias)
**Visão:** Comparação entre tipos de veículos
**Componentes:**
- Tabela de resumo por categoria
- 4 gráficos de comparação
- Análise de equivalências

**Gráficos:**
```javascript
// CO₂ por categoria
Chart.js - Bar Chart

// Combustível por categoria
Chart.js - Bar Chart

// Tempo economizado por categoria
Chart.js - Bar Chart

// Equivalência em árvores
Chart.js - Radar Chart
```

#### 3. Análise Temporal (/periodos)
**Visão:** Evolução mensal do impacto
**Componentes:**
- 3 gráficos de linha/barra
- Análise de tendências

**Gráficos:**
```javascript
// Evolução mensal (CO₂ + Tempo)
Chart.js - Line Chart (duplo eixo)

// CO₂ por mês
Chart.js - Bar Chart

// Passagens por mês
Chart.js - Bar Chart
```

#### 4. Ranking ESG (/ranking)
**Visão:** Veículos mais sustentáveis
**Componentes:**
- Gráfico de ranking (top 20)
- Tabela com posições
- Medalhas (🥇 🥈 🥉)

#### 5. Lista de Veículos (/veiculos)
**Visão:** Dados detalhados de cada carro
**Componentes:**
- Tabela interativa com sorting
- 7 colunas de dados
- Badges de categoria

---

## 💾 Análise de Dados e Excel

### Script: `generate_mock_data.py`

Gera 1000 registros realistas com:
- **Datas:** Últimos 6 meses (aleatórias)
- **Horas:** Entre 6h-22h (horário de funcionamento de shoppings)
- **Veículos:** Selecionados aleatoriamente do banco
- **Tipos:** Apenas 'shopping' para MVP
- **Tempos:** 8-12 minutos poupados por passagem

**Execução:**
```bash
python generate_mock_data.py 1000
```

**Campos Gerados:**
```sql
INSERT INTO passagens VALUES (
    id, placa, tipo='shopping', capcoins_ganhos, data_hora
)

INSERT INTO impacto_ambiental VALUES (
    id, placa, tipo='shopping', tempo_poupado, 
    combustivel_poupado_ml, co2_evitar_g, data_hora
)
```

**Distribuição de Dados:**
- 50 veículos únicos
- 1000 passagens totais (20 por veículo em média)
- CO₂ variável conforme consumo da categoria

### Script: `analytics_export.py`

Exporta dados para **Excel com múltiplas abas**

**Execução:**
```bash
python analytics_export.py
```

**Saída:**
`relatorio_ecometric_YYYYMMDD_HHMMSS.xlsx`

**Abas do Relatório:**

#### 1. "Resumo Executivo"
Métricas principais do sistema:
| Métrica | Valor |
|---------|-------|
| Total de Passagens | 1000 |
| Total de Veículos | 50 |
| CO₂ Total Evitado (g) | 45000 |
| Tempo Total Economizado (min) | 2500 |
| Combustível Total Poupado (ml) | 25000 |
| Árvores Preservadas | 2.14 |
| Folhas de Papel | 9000 |

#### 2. "Por Categoria"
Análise agregada por tipo de veículo:
| Categoria | Passagens | Tempo (min) | Combustível (ml) | CO₂ (g) | Árvores | Folhas |
|-----------|-----------|-------------|------------------|---------|---------|--------|
| Hatch | 150 | 1200 | 12000 | 27720 | 1.32 | 5544 |
| Sedan | 100 | 800 | 6400 | 13440 | 0.64 | 2688 |

#### 3. "Por Período"
Evolução mensal dos últimos 12 meses:
| Período | Passagens | Tempo | Combustível | CO₂ |
|---------|-----------|-------|-------------|-----|
| 2024-01 | 25 | 200 | 2000 | 4620 |
| 2024-02 | 28 | 224 | 2240 | 5171 |

#### 4. "Ranking Veículos"
Top 20 veículos por impacto:
| Placa | Tempo | Combustível | CO₂ | Árvores |
|-------|-------|-------------|-----|---------|
| ABC1234 | 120 | 1200 | 2772 | 0.132 |
| XYZ9876 | 110 | 1100 | 2539 | 0.121 |

#### 5. "Top Saldos"
Veículos com mais CapCoins:
| Placa | Modelo | Marca | Categoria | CapCoins |
|-------|--------|-------|-----------|----------|
| ABC1234 | Corolla | Toyota | Sedan | 60 |

#### 6. "Dados Impacto"
Amostra de 500 registros de impacto ambiental com todos os detalhes

#### 7. "Dados Passagens"
Amostra de 500 registros de passagens com capcoins ganhos

### Uso em Python

```python
import pandas as pd
from analytics_export import extrair_dados_completos, gerar_relatorio_excel

# Extrair dados
dfs = extrair_dados_completos()

# Acessar DataFrames
print(dfs['impacto'].head())    # Primeiras linhas
print(dfs['passagens'].describe())  # Estatísticas
print(dfs['saldos'].sort_values('capcoins', ascending=False))

# Gerar relatório
gerar_relatorio_excel(dfs, 'meu_relatorio.xlsx')
```

---

## 🚀 Como Usar

### Cenário 1: Desenvolver Localmente

```bash
# 1. Setup
cd ecometric
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# 2. Inicializar banco
python -c "from src.seed import popular_banco; popular_banco()"

# 3. Gerar dados de teste
python generate_mock_data.py 1000

# 4. Rodar aplicação
python app.py

# 5. Acessar
# Abra http://localhost:5000 no navegador
```

### Cenário 2: Testar a API

```bash
# Com curl
curl http://localhost:5000/api/metricas
curl http://localhost:5000/api/categorias
curl http://localhost:5000/api/ranking

# Com Python
import requests

response = requests.get('http://localhost:5000/api/metricas')
print(response.json())
```

### Cenário 3: Exportar Relatório

```bash
# Gerar Excel
python analytics_export.py

# Arquivo gerado em: /mnt/user-data/outputs/relatorio_ecometric_*.xlsx
```

### Cenário 4: Adicionar Novo Veículo

```python
from src.services import cadastrar_veiculo_por_modelo

# Cadastrar Corolla (modelo_id=1)
cadastrar_veiculo_por_modelo('ABC1234', 1)

# Agora o veículo aparecerá no dashboard
```

### Cenário 5: Registrar Passagem

```python
from src.services import registrar_uso_taggy
from src.impact_service import comparar_co2

# Registrar passagem
resultado = registrar_uso_taggy('ABC1234', 'shopping')
print(f"Ganhou {resultado['total_ganho']} CapCoins")

# Calcular impacto
impacto = comparar_co2('ABC1234', 'shopping')
print(f"CO₂ evitado: {impacto['co2_evitar_g']}g")
```

---

## 🔍 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:**
```bash
pip install flask
# ou reinstalar todas as dependências
pip install -r requirements.txt
```

### Erro: "sqlite3.OperationalError: no such table"
**Solução:**
```bash
# Recriar banco de dados
python -c "from src.seed import popular_banco; popular_banco()"
```

### Erro: "Address already in use :5000"
**Solução:**
```bash
# Porta 5000 já está em uso
# Opção 1: Matar processo na porta 5000
# Opção 2: Usar porta diferente em app.py
app.run(debug=True, port=5001)
```

### Dashboard carrega mas não mostra dados
**Verificar:**
1. Dados foram gerados? `python generate_mock_data.py 1000`
2. Banco tem tabelas? `SELECT name FROM sqlite_master WHERE type='table';`
3. Console do navegador tem erros? Abrir DevTools (F12)
4. API responde? `curl http://localhost:5000/api/metricas`

### Gráficos não aparecem
**Verificar:**
1. JavaScript ativado no navegador
2. Chart.js carregou? (DevTools → Network)
3. Axios carregou? (DevTools → Network)
4. Dados chegaram da API? (DevTools → Network → /api/*)

### Excel não gera ou fica corrompido
**Solução:**
```bash
# Reinstalar openpyxl
pip install --upgrade openpyxl

# Verificar permissões de escrita em /mnt/user-data/outputs/
```

---

## 📝 Notas Importantes

### Sobre os Dados Mockados
- Todos os 1000 registros são **fictícios para demonstração**
- Distribuição realista simulando uso real de shoppings
- Datas aleatórias nos últimos 6 meses
- Tipos de veículos baseados em frota real de Recife/PE

### Sobre o MVP
- Foco em **shopping centers** (não inclui pedágios/condomínios por enquanto)
- Apenas registros de **2024**
- 50 veículos-teste gerados automaticamente
- Design responsivo mas otimizado para **desktop**

### Próximos Passos Sugeridos
1. **Autenticação:** Adicionar login de usuários
2. **Histórico de Passagens:** Detalhar cada transação
3. **Mapa Interativo:** Mostrar localização de shoppings
4. **Notificações:** Alertas quando atinge 100 CapCoins
5. **Mobile App:** Versão nativa para iOS/Android
6. **Gamificação Avançada:** Badges, achievements, leaderboards
7. **Integração Real:** Conectar com API do Taggy
8. **Previsões:** ML para estimar economia futura

---

**Última atualização:** Mai/2024
**Versão:** 1.0.0 (MVP)
**Status:** Pronto para demonstração