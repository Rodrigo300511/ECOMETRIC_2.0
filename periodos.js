document.addEventListener('DOMContentLoaded', async () => {
    console.log('📅 Carregando análise temporal...');
    await carregarDados();
});

async function carregarDados() {
    try {
        const response = await axios.get('/api/periodos');
        const dados = response.data;

        if (!dados || dados.length === 0) {
            console.warn('⚠️ Sem dados de período');
            return;
        }

        criarGraficos(dados);
    } catch (error) {
        console.error('❌ Erro:', error);
    }
}

function criarGraficos(dados) {
    const labels = dados.map(d => d.mes);
    const co2Data = dados.map(d => d.co2_g);
    const passagesData = dados.map(d => d.passagens);
    const combustivelData = dados.map(d => d.combustivel_ml);
    const tempoData = dados.map(d => d.tempo_min);

    // Gráfico de Evolução (Linha com múltiplas métricas)
    new Chart(document.getElementById('evolutionChart'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'CO₂ Evitado (g)',
                    data: co2Data,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: '#047857'
                },
                {
                    label: 'Tempo Economizado (min)',
                    data: tempoData,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    borderDash: [5, 5],
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { position: 'top', labels: { font: { size: 12, weight: 600 } } }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'CO₂ (g)' }
                },
                y1: {
                    position: 'right',
                    title: { display: true, text: 'Tempo (min)' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });

    // Gráfico CO₂ por Mês
    new Chart(document.getElementById('co2TimeChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Evitado (g)',
                data: co2Data,
                backgroundColor: '#10b981',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });

    // Gráfico Passagens por Mês
    new Chart(document.getElementById('passagesChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total de Passagens',
                data: passagesData,
                backgroundColor: '#0ea5e9',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}