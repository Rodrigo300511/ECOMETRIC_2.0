/* Carregar dados e criar gráficos do Ranking */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🏆 Carregando ranking de veículos...');

    await carregarRanking();

    console.log('✅ Ranking carregado!');
});

async function carregarRanking() {
    try {
        const response = await axios.get('/api/ranking');
        const dados = response.data;

        if (!dados || dados.length === 0) {
            document.getElementById('tbody').innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;padding:2rem;">
                        😢 Nenhum dado disponível
                    </td>
                </tr>
            `;
            return;
        }

        // Preencher tabela
        const tbody = document.getElementById('tbody');

        tbody.innerHTML = dados.map(item => `
            <tr>
                <td><strong>#${item.posicao}</strong></td>
                <td>${item.placa}</td>
                <td style="font-weight:600;color:var(--primary-green);">
                    ${item.co2_g.toFixed(2)}
                </td>
            </tr>
        `).join('');

        criarGraficoRanking(dados);

    } catch (error) {
        console.error('❌ Erro ao carregar ranking:', error);

        document.getElementById('tbody').innerHTML = `
            <tr>
                <td colspan="3" style="text-align:center;padding:2rem;color:red;">
                    ⚠️ Erro ao carregar dados
                </td>
            </tr>
        `;
    }
}

function criarGraficoRanking(dados) {

    // Top 10
    const top10 = dados.slice(0, 10);

    const labels = top10.map(v => v.placa);
    const co2 = top10.map(v => v.co2_g);

    new Chart(document.getElementById('rankingChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Evitado (g)',
                data: co2,
                backgroundColor: [
                    '#10b981',
                    '#059669',
                    '#047857',
                    '#34d399',
                    '#6ee7b7',
                    '#a7f3d0',
                    '#d1fae5',
                    '#10b981',
                    '#059669',
                    '#047857'
                ],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    padding: 12,
                    borderRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}