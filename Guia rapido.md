# 🚀 Ecometric MVP - Guia de Início Rápido

## 📦 O Que Você Recebeu

Você recebeu um **MVP completo e funcional** do Ecometric com:

✅ Backend Python (Flask + SQLite)  
✅ Frontend moderno (HTML5 + CSS3 + JavaScript)  
✅ Dashboard com 5 páginas  
✅ API REST (6 endpoints)  
✅ Gerador de dados mockados (1000 registros)  
✅ Exportador Excel com 7 abas  
✅ Documentação completa (50+ páginas)  

---

## ⚡ Setup em 5 Minutos

### Passo 1: Extrair Arquivo
```bash
tar -xzf ecometric-mvp.tar.gz
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
python -c "from src.seed import popular_banco; popular_banco()"
```

Output esperado:
```
✅ Categorias ambientais cadastradas!
✅ Modelos cadastrados!
✅ Catálogo de recompensas cadastrado!
✅ Banco populado com sucesso!
```

### Passo 5: Gerar Dados de Teste (1000 registros)
```bash
python generate_mock_data.py 1000
```

Output esperado:
```
🔄 Gerando 1000 registros mockados...
✅ 1000 registros gerados com sucesso!
📊 Veículos com dados: 50
```

### Passo 6: Iniciar Dashboard
```bash
python app.py
```

Output esperado:
```
============================================================
🌱 ECOMETRIC - DASHBOARD
============================================================

🚀 Iniciando aplicação...
📡 Acesse em: http://localhost:5000

============================================================
```

### Passo 7: Abrir no Navegador
Vá para: **http://localhost:5000**

---

## 📊 Explorando o Dashboard

### Página 1: Dashboard Principal (/)
- 4 cards com métricas principais
  - 💨 CO₂ Evitado
  - ⏱️ Tempo Economizado
  - ⛽ Combustível Poupado
  - 🌳 Árvores Preservadas
- 3 gráficos interativos
- Estatísticas totais

### Página 2: Análise por Categoria (/categorias)
- Tabela com resumo por tipo de veículo (Hatch, Sedan, SUV, etc)
- 4 gráficos comparativos
- Radar chart de equivalências

### Página 3: Evolução Temporal (/periodos)
- Timeline dos últimos 12 meses
- Gráficos de CO₂ e passagens por mês
- Análise de tendências

### Página 4: Ranking ESG (/ranking)
- Top 20 veículos mais sustentáveis
- Gráfico horizontal mostrando posições
- Tabela com medalhas (🥇 🥈 🥉)

### Página 5: Lista de Veículos (/veiculos)
- Tabela com 50 veículos cadastrados
- Dados: placa, modelo, marca, categoria, passagens, CO₂, CapCoins
- Pode ser scrollada horizontalmente

---

## 💾 Exportar Relatório Excel

```bash
python analytics_export.py
```

Um arquivo será gerado em: `/mnt/user-data/outputs/relatorio_ecometric_YYYYMMDD_HHMMSS.xlsx`

**7 Abas do Relatório:**
1. **Resumo Executivo** - Métricas principais do sistema
2. **Por Categoria** - Análise agregada por tipo de carro
3. **Por Período** - Evolução mensal (12 meses)
4. **Ranking Veículos** - Top 20 com todos os detalhes
5. **Top Saldos** - Veículos com mais CapCoins
6. **Dados Impacto** - Amostra de 500 registros brutos
7. **Dados Passagens** - Amostra de 500 registros brutos

---

## 🔧 Estrutura do Projeto

```
ecometric/
│
├── src/                          # 🧠 Lógica de Negócio
│   ├── database.py              # Conexão SQLite
│   ├── models.py                # Schemas de tabelas
│   ├── seed.py                  # Dados iniciais
│   ├── services.py              # CRUD de veículos
│   └── impact_service.py        # Cálculos ambientais
│
├── templates/                    # 🎨 Frontend HTML
│   ├── index.html               # Dashboard principal
│   ├── categorias.html          # Análise por tipo
│   ├── periodos.html            # Análise temporal
│   ├── ranking.html             # Ranking ESG
│   ├── veiculos.html            # Lista de carros
│   ├── 404.html                 # Erro não encontrado
│   └── 500.html                 # Erro servidor
│
├── static/                       # 📦 Recursos Estáticos
│   ├── css/
│   │   └── style.css            # Design System completo
│   └── js/
│       ├── dashboard.js         # Lógica do dashboard
│       ├── categorias.js        # Gráficos de categoria
│       ├── periodos.js          # Gráficos temporal
│       ├── ranking.js           # Gráficos ranking
│       └── veiculos.js          # Carregamento veículos
│
├── app.py                       # 🚀 Aplicação Flask
├── generate_mock_data.py        # 📊 Gerador de dados
├── analytics_export.py          # 💾 Exportador Excel
├── requirements.txt             # 📋 Dependências Python
└── README.md                    # 📖 Documentação
```

---

## 📚 Documentação

### Arquivos Incluídos:
- **README.md** - Visão geral e quick start
- **DOCUMENTACAO_PARTE1.md** - Arquitetura, módulos e API
- **DOCUMENTACAO_PARTE2.md** - Dashboard, dados e troubleshooting

### Tópicos Cobertos:
✅ Visão geral e objetivos  
✅ Arquitetura do projeto  
✅ Instalação e setup passo-a-passo  
✅ Estrutura de pastas  
✅ Documentação de cada módulo  
✅ Especificação da API REST  
✅ Design system e componentes  
✅ Como usar o dashboard  
✅ Exportação de relatórios  
✅ Troubleshooting e FAQ  
✅ Roadmap de funcionalidades futuras  

---

## 🔗 API REST Disponível

A aplicação expõe 6 endpoints JSON:

```bash
# Métricas globais
curl http://localhost:5000/api/metricas

# Análise por categoria
curl http://localhost:5000/api/categorias

# Análise temporal (últimos 12 meses)
curl http://localhost:5000/api/periodos

# Top 20 veículos por CO₂
curl http://localhost:5000/api/ranking

# Lista de veículos (top 50)
curl http://localhost:5000/api/veiculos

# Health check
curl http://localhost:5000/health
```

---

## 🎨 Paleta de Cores (Design System)

```
🟢 Verde Principal: #10b981
🟢 Verde Escuro: #047857
🟢 Verde Claro: #d1fae5
🟢 Verde Muito Claro: #f0fdf4

🟠 Laranja: #f97316
🔵 Azul: #0ea5e9
🟣 Roxo: #6d28d9
```

---

## 🧮 Fórmulas de Cálculo

### CO₂ Evitado (g)
```
litros_poupados = consumo_litro_hora × (tempo_poupado_min / 60)
co2_evitado = litros_poupados × fator_co2
```

### Árvores Preservadas
```
arvores = co2_total_g / 21000
```
(Uma árvore absorve ~21kg de CO2 em sua vida útil)

### Folhas Economizadas
```
folhas = co2_total_g / 5
```
(~5g de CO2 para produzir uma folha A4)

### CapCoins (Pontuação)
```
shopping: 3 pontos/passagem
bônus_10_passagens: +20 pontos
bônus_20_passagens: +50 pontos
bônus_40_passagens: +100 pontos
```

---

## ❓ FAQ Rápido

**P: Por que não conecta com a API real do Taggy?**  
R: Este é um MVP com dados mockados para demonstração. A integração com API real virá em versão futura.

**P: Posso adicionar meu próprio veículo?**  
R: Sim! Qualquer modelo em `modelos.py` pode ser cadastrado. Use a função `cadastrar_veiculo_por_modelo()`.

**P: Os dados são salvos?**  
R: Sim! Tudo é persistido em `ecometric.db` (SQLite). Os dados continuarão lá quando reiniciar.

**P: Como faço para resetar tudo?**  
R: Delete `ecometric.db` e execute `python -c "from src.seed import popular_banco; popular_banco()"`.

**P: Posso usar em produção?**  
R: Não, é um MVP. Para produção, use Flask + Gunicorn + Nginx + PostgreSQL.

---

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: flask` | `pip install -r requirements.txt` |
| `no such table: veiculos` | `python -c "from src.seed import popular_banco; popular_banco()"` |
| Porta 5000 em uso | `app.run(port=5001)` em app.py |
| Sem dados no dashboard | Execute `python generate_mock_data.py 1000` |
| Gráficos em branco | Limpe cache do navegador (Ctrl+Shift+Del) |

---

## 🎯 Próximos Passos Sugeridos

1. **Explorar o Dashboard** - Veja todos os 5 pages e gráficos
2. **Ler Documentação** - DOCUMENTACAO_PARTE1.md e PARTE2.md
3. **Testar a API** - Use curl/Postman nos endpoints
4. **Gerar Excel** - Execute analytics_export.py e veja o relatório
5. **Customizar** - Mude cores, adicione mais modelos, etc

---

## 📞 Contato e Suporte

Para dúvidas sobre o projeto, consulte:
- **README.md** - Visão geral rápida
- **DOCUMENTACAO_PARTE1.md** - Detalhes técnicos
- **DOCUMENTACAO_PARTE2.md** - Como usar e troubleshoot
- **Comentários no código** - Cada função tem docstring

---

## 🌱 Sobre o Ecometric

Ecometric transforma o uso de RFID Taggy em **dados mensuráveis de sustentabilidade**.

**Missão:** Reduzir emissões de CO₂ na mobilidade urbana de Recife, Pernambuco.

**Visão:** Um futuro onde a sustentabilidade é gamificada e recompensada.

---

**Status:** ✅ MVP Pronto para Demonstração  
**Versão:** 1.0.0  
**Última Atualização:** Maio/2024  

🌱 **Reduzindo emissões, um trajeto por vez.**