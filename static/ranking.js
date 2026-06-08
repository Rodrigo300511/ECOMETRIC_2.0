/* ====================================================
   ECOMETRIC DASHBOARD - RANKING COM PROTEÇÃO DE DADOS
   ==================================================== */

// Garante uma inicialização segura e isolada para o objeto de gráficos
if (typeof window.charts === 'undefined') {
    window.charts = {};
}

/**
 * Aplica uma máscara de anonimização na placa do veículo para LGPD/Privacidade (ex: ABC1234 -> AB***34)
 */
function mascararPlaca(placa) {
    if (!placa) return '---';
    const str = String(placa).trim();
    if (str.length < 4) return str;
    return str.substring(0, 2) + '***' + str.substring(str.length - 2);
}

// ====================================================
// INICIALIZAÇÃO
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🏆 Carregando ranking de veículos protegidos...');
    await carregarRanking();
    console.log('✅ Ranking carregado com sucesso!');
});

// ====================================================
// CARREGAR E PREENCHER DADOS DO RANKING
// ====================================================
async function carregarRanking() {
    try {
        const response = await axios.get('/api/ranking');
        const dados = response.data;

        const tbody = document.getElementById('tbody');
        if (!tbody) return;

        if (!dados || dados.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;padding:2rem;">
                        😢 Nenhum dado disponível
                    </td>
                </tr>
            `;
            return;
        }

        // Mapeamento e preenchimento dinâmico aplicando as medalhas originais e a máscara de placa
        tbody.innerHTML = dados.map(item => {
            let medalha = '';
            let classe = '';

            if (item.posicao === 1) {
                medalha = '🥇';
                classe = 'gold';
            } else if (item.posicao === 2) {
                medalha = '🥈';
                classe = 'silver';
            } else if (item.posicao === 3) {
                medalha = '🥉';
                classe = 'bronze';
            }

            return `
                <tr class="${classe}">
                    <td class="position">
                        ${medalha} ${item.posicao}
                    </td>
                    <td>
                        <strong>${mascararPlaca(item.placa).toUpperCase()}</strong>
                    </td>
                    <td class="co2-value" style="font-weight:600; color:var(--primary-green, #059669);">
                        ${Number(item.co2_g).toFixed(2)} g
                    </td>
                </tr>
            `;
        }).join('');

        // Tenta renderizar o gráfico com os dados se o elemento existir
        criarGraficoRanking(dados);

    } catch (error) {
        console.error('❌ Erro ao carregar ranking:', error);
        
        const tbody = document.getElementById('tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;padding:2rem;color:#dc2626;font-weight:bold;">
                        ⚠️ Erro ao carregar dados do ranking
                    </td>
                </tr>
            `;
        }
    }
}

// ====================================================
// RENDERIZAR GRÁFICO DO RANKING (TOP 10)
// ====================================================
function criarGraficoRanking(dados) {
    const canvasId = 'rankingChart';
    if (!document.getElementById(canvasId)) return;

    // Isola os 10 melhores posicionados
    const top10 = dados.slice(0, 10);

    // Mapeamento de dados aplicando a máscara também nos rótulos do gráfico
    const labels = top10.map(v => mascararPlaca(v.placa).toUpperCase());
    const co2Data = top10.map(v => v.co2_g);

    // Controle e destruição segura da instância anterior para evitar sobreposição visual
    if (window.charts && window.charts.rankingChart) {
        window.charts.rankingChart.destroy();
    }

    // Configuração visual alinhada ao Design System Corporativo Ecometric
    const COR_TEXTO_SOBRIO = '#475569';
    const COR_LINHA_GRADE  = '#e2e8f0';

    Chart.defaults.font.family = "'Inter', 'Segoe UI', sans-serif";
    Chart.defaults.font.color = COR_TEXTO_SOBRIO;

    const ctx = document.getElementById(canvasId).getContext('2d');
    window.charts.rankingChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Evitado (g)',
                data: co2Data,
                backgroundColor: [
                    '#10b981', '#059669', '#047857', '#34d399', '#6ee7b7',
                    '#a7f3d0', '#d1fae5', '#10b981', '#059669', '#047857'
                ],
                borderRadius: 6,
                barPercentage: 0.6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { 
                    grid: { color: COR_LINHA_GRADE }, 
                    ticks: { color: COR_TEXTO_SOBRIO } 
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: COR_TEXTO_SOBRIO } 
                }
            }
        }
    });
}