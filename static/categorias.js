/* Carregar dados e criar gráficos de categorias */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('📊 Carregando análise por categorias...');
    
    await carregarDados();
    
    console.log('✅ Análise carregada!');
});

async function carregarDados() {
    try {
        const response = await axios.get('/api/categorias');
        const dados = response.data;

        if (!dados || dados.length === 0) {
            document.getElementById('tbody').innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 2rem;">
                        😢 Nenhum dado disponível
                    </td>
                </tr>
            `;
            return;
        }

        // Preencher tabela
        const tbody = document.getElementById('tbody');
        tbody.innerHTML = dados.map(d => `
            <tr>
                <td><strong>${d.categoria}</strong></td>
                <td>${d.passagens}</td>
                <td>${d.tempo_min.toFixed(2)}</td>
                <td>${d.combustivel_ml.toFixed(2)}</td>
                <td style="font-weight: 600; color: var(--primary-green);">${d.co2_g.toFixed(2)}</td>
                <td>${d.arvores_equiv.toFixed(2)}</td>
            </tr>
        `).join('');

        // Criar gráficos
        criarGraficos(dados);

    } catch (error) {
        console.error('❌ Erro:', error);
        document.getElementById('tbody').innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 2rem; color: var(--warning-orange);">
                    ⚠️ Erro ao carregar dados
                </td>
            </tr>
        `;
    }
}

function criarGraficos(dados) {
    const labels = dados.map(d => d.categoria);
    const co2Data = dados.map(d => d.co2_g);
    const fuelData = dados.map(d => d.combustivel_ml);
    const timeData = dados.map(d => d.tempo_min);
    const treeData = dados.map(d => d.arvores_equiv);

    const cores = ['#10b981', '#059669', '#047857', '#065f46', '#064e3b', '#0d3b2d'];

    // Gráfico CO₂
    new Chart(document.getElementById('co2Chart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Evitado (g)',
                data: co2Data,
                backgroundColor: cores,
                borderRadius: 8,
                hoverBackgroundColor: '#047857'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8
                }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Gráfico Combustível
    new Chart(document.getElementById('fuelChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Combustível (ml)',
                data: fuelData,
                backgroundColor: '#f97316',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Gráfico Tempo
    new Chart(document.getElementById('timeChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tempo (min)',
                data: timeData,
                backgroundColor: '#f59e0b',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Gráfico Árvores
    new Chart(document.getElementById('treeChart'), {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Árvores Preservadas',
                data: treeData,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#047857',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                r: {
                    beginAtZero: true
                }
            }
        }
    });
}