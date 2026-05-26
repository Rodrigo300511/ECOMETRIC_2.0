"""
app.py - Dashboard Flask Ecometric

Aplicação web responsável por:
- Exibir métricas de impacto ambiental
- Mostrar dashboards por categoria
- Gerar gráficos interativos
- Apresentar rankings de veículos
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.database import conectar, fechar_conexao
from src.impact_service import metricas_globais, ranking_usuarios_verdes


app = Flask(__name__, template_folder='templates', static_folder='static')

# Desabilitar cache para desenvolvimento
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# =========================================================
# ROTAS DO DASHBOARD
# =========================================================

@app.route('/')
def index():
    """Página inicial com métricas globais."""
    
    try:
        metricas = metricas_globais()
        
        return render_template('index.html', metricas=metricas)
    
    except Exception as e:
        return f"Erro: {str(e)}", 500


@app.route('/api/metricas')
def api_metricas():
    """API: Retorna métricas globais em JSON."""
    
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

        # Inverter para mostrar do mais antigo para o mais recente
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
# ROTAS DE PÁGINAS
# =========================================================

@app.route('/categorias')
def categorias_page():
    """Página de análise por categoria."""
    return render_template('categorias.html')


@app.route('/periodos')
def periodos_page():
    """Página de análise temporal."""
    return render_template('periodos.html')


@app.route('/ranking')
def ranking_page():
    """Página de ranking de veículos."""
    return render_template('ranking.html')


@app.route('/veiculos')
def veiculos_page():
    """Página de lista detalhada de veículos."""
    return render_template('veiculos.html')


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):
    """Página de erro 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Página de erro 500."""
    return render_template('500.html'), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route('/health')
def health():
    """Verificar saúde da aplicação."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌱 ECOMETRIC - DASHBOARD")
    print("="*60)
    print("\n🚀 Iniciando aplicação...")
    print("📡 Acesse em: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')