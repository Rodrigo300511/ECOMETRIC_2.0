"""
app.py - Dashboard Flask Ecometric

Aplicação web responsável por:
- Exibir métricas de impacto ambiental
- Mostrar dashboards por categoria
- Gerar gráficos interativos
- Apresentar rankings de veículos
- Gerenciar sessões e fluxos de Visão Geral vs Área do Cliente
- [NOVO] Disponibilizar catálogo de recompensas e resgate exclusivo para clientes
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime, timedelta
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.database import conectar, fechar_conexao
from src.impact_service import metricas_globais, ranking_usuarios_verdes
from src.services import cadastrar_veiculo_por_modelo, listar_modelos
from src.impact_service import obter_painel_impacto


app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurações do servidor e segurança de Sessão
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Chave secreta obrigatória para assinar os cookies de sessão de forma segura
app.secret_key = os.environ.get('SECRET_KEY', 'ecometric_secret_token_key_9876')


# =========================================================
# FLUXO DE COMPORTAMENTO E CONTROLE DE SESSÃO (AUTENTICAÇÃO)
# =========================================================

@app.route('/login')
def login_page():
    """Renderiza a página de autenticação (Portal de Login)."""
    # Se já estiver autenticado, redireciona para o fluxo da home
    if 'perfil' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Limpa a sessão atual do usuário e redireciona para o login."""
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/api/login', methods=['POST'])
def api_login():
    """API: Processa as credenciais de entrada e define o escopo do usuário."""
    try:
        dados = request.get_json() or {}
        usuario = dados.get('usuario', '').strip()
        senha = dados.get('senha', '')

        if not usuario or not senha:
            return jsonify({'erro': 'Usuário/Placa e senha são obrigatórios.'}), 400

        # 1. Validação do Perfil Administrativo (Visão Geral)
        if usuario.lower() == 'admin' and senha == 'admin123':
            session['usuario_logado'] = 'admin'
            session['perfil'] = 'admin'
            return jsonify({'perfil': 'admin'})

        # 2. Validação de Cliente (Usa a Placa do Carro como identificador de Usuário)
        # Verifica se o formato bate minimamente com um padrão de identificação veicular
        elif len(usuario) >= 7 and senha == '123456':
            placa_formatada = usuario.upper()
            
            # Validação no banco de dados para garantir integridade (evitar login de placa fantasma)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT placa FROM veiculos WHERE placa = ?", (placa_formatada,))
            veiculo_existe = cursor.fetchone()
            fechar_conexao(conn)

            if not veiculo_existe:
                return jsonify({'erro': 'Esta placa não consta como cadastrada no sistema.'}), 404

            session['usuario_logado'] = placa_formatada
            session['perfil'] = 'cliente'
            session['placa_cliente'] = placa_formatada
            
            return jsonify({
                'perfil': 'cliente',
                'placa': placa_formatada
            })

        return jsonify({'erro': 'Credenciais de acesso incorretas.'}), 401

    except Exception as e:
        return jsonify({'erro': f'Erro interno no servidor: {str(e)}'}), 500


# =========================================================
# ROTAS DO DASHBOARD (VISÕES CONDICIONAIS)
# =========================================================

@app.route('/')
def index():
    """Página de entrada com bifurcação condicional baseada na Sessão."""
    # Se não houver uma sessão activa, força o login
    if 'perfil' not in session:
        return redirect(url_for('login_page'))
    
    # Bifurcação 1: Administrador vê a Visão Geral Completa (Métricas Globais)
    if session['perfil'] == 'admin':
        try:
            metricas = metricas_globais()
            return render_template('index.html', metricas=metricas, perfil='admin')
        except Exception as e:
            return f"Erro ao processar visão geral: {str(e)}", 500
            
    # Bifurcação 2: Cliente vê estritamente o seu Painel Individualizado (Área do Cliente)
    elif session['perfil'] == 'cliente':
        placa = session.get('placa_cliente')
        return render_template('cliente.html', placa=placa, perfil='cliente')


@app.route('/api/metricas')
def api_metricas():
    """API: Retorna métricas globais em JSON (Restrito para Admin)."""
    if 'perfil' not in session or session['perfil'] != 'admin':
        return jsonify({'erro': 'Acesso negado. Requer perfil administrativo.'}), 403
        
    try:
        metricas = metricas_globais()
        return jsonify(metricas)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/categorias')
def api_categorias():
    """API: Análise por categoria de veículo."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.nome as categoria,
                COUNT(p.id) as total_passagens,
                SUM(i.tempo_poupado) as tempo_total,
                SUM(i.combustivel_poupado_ml) as combustivel_total,
                SUM(i.co2_evitar_g) as co2_total

            FROM categorias c
            LEFT JOIN modelos m ON c.id = m.categoria_id
            LEFT JOIN veiculos v ON m.id = v.modelo_id
            LEFT JOIN impacto_ambiental i ON v.placa = i.placa
            LEFT JOIN passagens p ON v.placa = p.placa

            GROUP BY c.id, c.nome
            ORDER BY co2_total DESC NULLS LAST
        """)

        categorias = cursor.fetchall()
        fechar_conexao(conn)

        resultado = []
        for cat in categorias:
            if cat[0]:  # Se tem categoria
                resultado.append({
                    'categoria': cat[0],
                    'passagens': cat[1] or 0,
                    'tempo_min': round(cat[2] or 0, 2),
                    'combustivel_ml': round(cat[3] or 0, 2),
                    'co2_g': round(cat[4] or 0, 2),
                    'arvores_equiv': round((cat[4] or 0) / 21000, 2)
                })

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/periodos')
def api_periodos():
    """API: Análise por período (mês)."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CAST(substr(data_hora, 1, 7) as TEXT) as mes,
                COUNT(*) as total_passagens,
                SUM(tempo_poupado) as tempo_total,
                SUM(combustivel_poupado_ml) as combustivel_total,
                SUM(co2_evitar_g) as co2_total

            FROM impacto_ambiental
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 12
        """)

        periodos = cursor.fetchall()
        fechar_conexao(conn)

        resultado = []
        for periodo in periodos:
            resultado.append({
                'mes': periodo[0],
                'passagens': periodo[1],
                'tempo_min': round(periodo[2] or 0, 2),
                'combustivel_ml': round(periodo[3] or 0, 2),
                'co2_g': round(periodo[4] or 0, 2)
            })

        resultado.reverse()
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/ranking')
def api_ranking():
    """API: Ranking de veículos por impacto."""
    try:
        ranking = ranking_usuarios_verdes()
        
        resultado = []
        posicao = 1
        
        for item in ranking[:20]:  # Top 20
            resultado.append({
                'posicao': posicao,
                'placa': item[0],
                'co2_g': round(item[1], 2)
            })
            posicao += 1

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/veiculos')
def api_veiculos():
    """API: Dados detalhados de veículos."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                v.placa,
                m.nome as modelo,
                m.marca,
                c.nome as categoria,
                COUNT(p.id) as total_passagens,
                SUM(i.co2_evitar_g) as co2_total,
                s.saldo as capcoins

            FROM veiculos v
            JOIN modelos m ON v.modelo_id = m.id
            JOIN categorias c ON m.categoria_id = c.id
            LEFT JOIN passagens p ON v.placa = p.placa
            LEFT JOIN impacto_ambiental i ON v.placa = i.placa
            LEFT JOIN saldo_capcoins s ON v.placa = s.placa

            GROUP BY v.placa
            ORDER BY co2_total DESC NULLS LAST
            LIMIT 50
        """)

        veiculos = cursor.fetchall()
        fechar_conexao(conn)

        resultado = []
        for veh in veiculos:
            resultado.append({
                'placa': veh[0],
                'modelo': veh[1],
                'marca': veh[2],
                'categoria': veh[3],
                'passagens': veh[4] or 0,
                'co2_g': round(veh[5] or 0, 2),
                'capcoins': veh[6] or 0
            })

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# =========================================================
# ROTAS DE RENDERIZAÇÃO DE PÁGINAS (ADMINISTRATIVAS / GERAIS)
# =========================================================

@app.route('/categorias')
def categorias_page():
    if 'perfil' not in session or session['perfil'] != 'admin':
        return redirect(url_for('login_page'))
    return render_template('categorias.html')


@app.route('/periodos')
def periodos_page():
    if 'perfil' not in session or session['perfil'] != 'admin':
        return redirect(url_for('login_page'))
    return render_template('periodos.html')


@app.route('/ranking')
def ranking_page():
    if 'perfil' not in session:
        return redirect(url_for('login_page'))
    return render_template('ranking.html')


@app.route('/veiculos')
def veiculos_page():
    if 'perfil' not in session or session['perfil'] != 'admin':
        return redirect(url_for('login_page'))
    return render_template('veiculos.html')


# =========================================================
# FEATURE: LOJA DE RECOMPENSAS (RESTRITO AO PERFIL CLIENTE)
# =========================================================

@app.route('/loja')
def loja_page():
    """Renderiza a página da Loja Sustentável de Recompensas.
    BARREIRA: Apenas o cliente logado pode acessar. Admin é redirecionado para home.
    """
    if 'perfil' not in session:
        return redirect(url_for('login_page'))
        
    if session['perfil'] == 'admin':
        return redirect(url_for('index'))
        
    placa = session.get('placa_cliente')
    return render_template('loja.html', placa=placa, perfil='cliente')


@app.route('/api/recompensas', methods=['GET'])
def api_listar_recompensas():
    """API: Retorna o catálogo de prêmios cadastrados para montagem da loja."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, custo, descricao, categoria FROM recompensas ORDER BY custo ASC")
        linhas = cursor.fetchall()
        fechar_conexao(conn)
        
        recompensas = [{
            'id': r[0], 'nome': r[1], 'custo': r[2], 'descricao': r[3], 'categoria': r[4]
        } for r in linhas]
        
        return jsonify(recompensas)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/loja/resgatar', methods=['POST'])
def api_resgatar_recompensa():
    """API: Processa a dedução dos CapCoins ao trocar por uma recompensa.
    BARREIRA RIGIDA: Apenas para clientes reais. Bloqueia manipulações ou acessos de Admin.
    """
    if 'perfil' not in session or session['perfil'] != 'cliente':
        return jsonify({'erro': 'Acesso negado. Apenas clientes podem efetuar resgates.'}), 403
        
    try:
        dados = request.get_json() or {}
        placa = dados.get('placa', '').strip().upper()
        recompensa_id = dados.get('recompensa_id')
        
        # Garante integridade: placa enviada no corpo deve bater com a placa logada
        if placa != session.get('placa_cliente'):
            return jsonify({'erro': 'Ação inválida. Identificação do veículo inconsistente.'}), 403
            
        if not recompensa_id:
            return jsonify({'erro': 'ID da recompensa é obrigatório.'}), 400

        from src.services import resgatar_recompensa
        # Aciona o seu serviço central do backend (services.py) que fará a validação de saldo
        resgatar_recompensa(placa, int(recompensa_id))
        
        return jsonify({'status': 'sucesso', 'mensagem': 'Resgate processado com sucesso!'})
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro no processamento do resgate: {str(e)}'}), 500


# =========================================================
# ROTAS DA FEATURE CLIENTE (DADOS ESPECÍFICOS)
# =========================================================

@app.route('/api/modelos', methods=['GET'])
def api_listar_modelos():
    try:
        modelos = listar_modelos()
        lista_modelos = [{'id': m[0], 'nome': m[1], 'marca': m[2], 'ano': m[3], 'categoria': m[4]} for m in modelos]
        return jsonify(lista_modelos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/cliente/cadastro', methods=['POST'])
def api_cadastrar_veiculo():
    try:
        dados = request.get_json()
        placa = dados.get('placa', '').strip().upper()
        modelo_id = dados.get('modelo_id')

        if not placa or not modelo_id:
            return jsonify({'erro': 'Placa e Modelo são obrigatórios.'}), 400

        cadastrar_veiculo_por_modelo(placa, int(modelo_id))
        return jsonify({'status': 'sucesso', 'mensagem': f'Veículo {placa} registado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/cliente/<placa>', methods=['GET'])
def api_dados_cliente(placa):
    # Proteção de barreira: Clientes só podem consultar os dados da própria placa logada
    if 'perfil' in session and session['perfil'] == 'cliente' and session['placa_cliente'] != placa.upper():
        return jsonify({'erro': 'Acesso não autorizado aos dados de outra placa.'}), 403

    try:
        placa = placa.strip().upper()
        painel = obter_painel_impacto(placa)
        
        if not painel or painel.get('total_passagens', 0) == 0:
            return jsonify({'perfil': painel, 'historico': [], 'evolucao': {'meses': [], 'co2': []}})

        conn = conectar()
        cursor = conn.cursor()
        
        # Histórico de passagens
        cursor.execute("""
            SELECT i.data_hora, i.tipo, i.co2_evitar_g, i.tempo_poupado, p.capcoins_ganhos
            FROM impacto_ambiental i
            JOIN passagens p ON i.placa = p.placa AND i.data_hora = p.data_hora
            WHERE i.placa = ? ORDER BY i.data_hora DESC
        """, (placa,))
        historico = [{'data_hora': p[0], 'local': p[1], 'co2_evitado': p[2], 'tempo_poupado': p[3], 'capcoins': p[4]} for p in cursor.fetchall()]

        # Evolução Mensal
        cursor.execute("""
            SELECT CAST(substr(data_hora, 1, 7) as TEXT) as mes, SUM(co2_evitar_g)
            FROM impacto_ambiental WHERE placa = ? GROUP BY mes ORDER BY mes ASC
        """, (placa,))
        dados_evolucao = cursor.fetchall()
        evolucao = {'meses': [row[0] for row in dados_evolucao], 'co2': [row[1] for row in dados_evolucao]}

        fechar_conexao(conn)
        return jsonify({'perfil': painel, 'historico': historico, 'evolucao': evolucao})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/cliente/usar_taggy', methods=['POST'])
def api_usar_taggy():
    """Simula o uso da Taggy em tempo real, gerando impacto e pontos."""
    try:
        dados = request.get_json()
        placa = dados.get('placa', '').strip().upper()
        local = dados.get('local', 'Shopping Tacaruna')

        if not placa:
            return jsonify({'erro': 'Placa é obrigatória.'}), 400

        conn = conectar()
        cursor = conn.cursor()

        # 1. Buscar os dados técnicos do veículo para calcular o impacto corretamente
        cursor.execute("""
            SELECT c.consumo_litro_hora, c.fator_co2
            FROM veiculos v
            JOIN modelos m ON v.modelo_id = m.id
            JOIN categorias c ON m.categoria_id = c.id
            WHERE v.placa = ?
        """, (placa,))
        veiculo = cursor.fetchone()

        if not veiculo:
            fechar_conexao(conn)
            return jsonify({'erro': 'Veículo não cadastrado no sistema.'}), 404

        consumo_litro_hora, fator_co2 = veiculo

        # 2. Regras de Negócio (8 min poupados, 3 CapCoins ganhos)
        tempo_poupado = 8.0
        litros_poupados = consumo_litro_hora * (tempo_poupado / 60.0)
        combustivel_poupado_ml = litros_poupados * 1000.0
        co2_evitar_g = litros_poupados * fator_co2
        capcoins = 3
        data_hora = datetime.now().isoformat()

        # 3. Inserir a nova Passagem
        cursor.execute("""
            INSERT INTO passagens (placa, tipo, capcoins_ganhos, data_hora)
            VALUES (?, ?, ?, ?)
        """, (placa, local, capcoins, data_hora))

        # 4. Inserir o Impacto Ambiental
        cursor.execute("""
            INSERT INTO impacto_ambiental (placa, tipo, tempo_poupado, combustivel_poupado_ml, co2_evitar_g, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (placa, local, tempo_poupado, combustivel_poupado_ml, co2_evitar_g, data_hora))

        # 5. Atualizar a Carteira de CapCoins do Cliente
        cursor.execute("""
            INSERT INTO saldo_capcoins (placa, saldo)
            VALUES (?, ?)
            ON CONFLICT(placa) DO UPDATE SET saldo = saldo + ?
        """, (placa, capcoins, capcoins))

        conn.commit()
        fechar_conexao(conn)

        return jsonify({'status': 'sucesso', 'mensagem': 'Passagem registada com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# =========================================================
# CONTROLADORES DE ERRO ESTILIZADOS
# =========================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌱 ECOMETRIC - DASHBOARD PROFISSIONAL")
    print("="*60)
    print("\n🚀 Iniciando aplicação...")
    print("📡 Acesse em: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')