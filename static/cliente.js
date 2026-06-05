/* ====================================================
   ECOMETRIC DASHBOARD - PORTAL E REGRAS DO CLIENTE
   ==================================================== */

if (typeof window.charts === 'undefined') {
    window.charts = {};
}

document.addEventListener('DOMContentLoaded', () => {
    const placa = window.CLIENTE_PLACA;
    if (!placa) {
        console.error('❌ Erro: Identificação do cliente ausente.');
        return;
    }

    // Inicializa a carga dos dados
    carregarDadosCliente(placa);

    // Configura o evento do Simulador Taggy
    const btnSimular = document.getElementById('btn-simular-taggy');
    if (btnSimular) {
        btnSimular.addEventListener('click', () => simularPassagemTaggy(placa));
    }
});

/**
 * Consulta e popula todas as métricas, gráficos e tabelas do cliente logado
 */
async function carregarDadosCliente(placa) {
    try {
        const response = await axios.get(`/api/cliente/${placa}`);
        const data = response.data;

        // 1. Popular os Cards Superiores
        const perfil = data.perfil || {};
        document.getElementById('res-passagens').textContent = perfil.total_passagens || 0;
        document.getElementById('res-co2').textContent = (perfil.co2_total_g || 0).toFixed(2) + ' g';
        document.getElementById('res-capcoins').textContent = '🪙 ' + (perfil.saldo_capcoins || 0);
        
        // Cálculo de árvores equivalente aproximado
        const arvores = (perfil.co2_total_g || 0) / 21000;
        document.getElementById('res-arvores').textContent = '🌳 ' + arvores.toFixed(3);

        // 2. Popular Tabela de Histórico
        const tbody = document.getElementById('tbody-historico');
        if (data.historico && data.historico.length > 0) {
            tbody.innerHTML = data.historico.map(h => {
                // Formatação simples da data ISO string
                const dataFormatada = h.data_hora ? h.data_hora.replace('T', ' ').substring(0,19) : '---';
                return `
                    <tr>
                        <td style="padding:12px;">${dataFormatada}</td>
                        <td style="padding:12px;">${h.local || 'Ponto de Acesso'}</td>
                        <td style="padding:12px;">⏱️ ${h.tempo_poupado || 0} min</td>
                        <td style="padding:12px; color:#10b981; font-weight:bold;">${(h.co2_evitado || 0).toFixed(2)} g</td>
                        <td style="padding:12px; font-weight:600;">🪙 +${h.capcoins || 0}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:20px;">😢 Nenhuma passagem registrada até o momento.</td></tr>`;
        }

        // 3. Renderizar o Gráfico de Barras/Linha Mensal do Cliente
        renderizarGraficoCliente(data.evolucao || { meses: [], co2: [] });

    } catch (error) {
        console.error('❌ Erro ao obter dados do cliente:', error);
    }
}

/**
 * Monta o gráfico Chart.js dinamicamente baseado no histórico do cliente
 */
function renderizarGraficoCliente(evolucao) {
    const canvas = document.getElementById('chart-cliente-co2');
    if (!canvas) return;

    if (window.charts.clienteChart) {
        window.charts.clienteChart.destroy();
    }

    const ctx = canvas.getContext('2d');
    window.charts.clienteChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: evolucao.meses || [],
            datasets: [{
                label: 'CO₂ Evitado por Mês (g)',
                data: evolucao.co2 || [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: '#e2e8f0' } },
                x: { grid: { display: false } }
            }
        }
    });
}

/**
 * Faz a chamada à API do simulador e atualiza a tela instantaneamente
 */
async function simularPassagemTaggy(placa) {
    const btnSimular = document.getElementById('btn-simular-taggy');
    const msg = document.getElementById('msg-simulador');
    
    btnSimular.disabled = true;
    msg.style.color = '#475569';
    msg.textContent = 'Processando passagem... ⏳';

    try {
        const locaisValidos = ['Shopping Tacaruna', 'Shopping Riomar', 'Pedágio Via Costeira', 'Estacionamento Aeroporto'];
        const localAleatorio = locaisValidos[Math.floor(Math.random() * locaisValidos.length)];

        const response = await axios.post('/api/cliente/usar_taggy', {
            placa: placa,
            local: localAleatorio
        });

        if (response.data && response.data.status === 'sucesso') {
            msg.style.color = '#166534';
            msg.textContent = `✅ Sucesso! Registrado em: ${localAleatorio}`;
            
            // Recarrega os dados na tela em tempo real sem dar refresh na página!
            await carregarDadosCliente(placa);
        }
    } catch (error) {
        console.error(error);
        msg.style.color = '#b91c1c';
        msg.textContent = '⚠️ Falha ao registrar simulação de passagem.';
    } finally {
        btnSimular.disabled = false;
    }
}