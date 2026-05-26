/* ====================================================
   ECOMETRIC DASHBOARD - SCRIPTS PRINCIPAIS
   ==================================================== */

let charts = {};

// ====================================================
// INICIALIZAÇÃO
// ====================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌱 Inicializando Dashboard Ecometric...');
    
    await carregarMetricas();
    await carregarGraficos();
    
    console.log('✅ Dashboard carregado com sucesso!');
});

// ====================================================
// CARREGAR MÉTRICAS PRINCIPAIS
// ====================================================

async function carregarMetricas() {
    try {
        const response = await axios.get('/api/metricas');
        const dados = response.data;

        // Formatador de números
        const formatter = new Intl.NumberFormat('pt-BR', {
            maximumFractionDigits: 2
        });

        // Atualizar valores
        document.getElementById('co2-value').textContent = 
            formatter.format(dados.co2_total_g);
        document.getElementById('time-value').textContent = 
            formatter.format(dados.tempo_total_min);
        document.getElementById('fuel-value').textContent = 
            formatter.format(dados.combustivel_total_ml);
        document.getElementById('tree-value').textContent = 
            dados.equivalente_arvores.toFixed(2);

        // Atualizar barras de progresso (animadas)
        animarBarra('co2-bar', 60);
        animarBarra('time-bar', 70);
        animarBarra('fuel-bar', 50);
        animarBarra('tree-bar', 80);

        // Atualizar total de passagens e veículos
        document.getElementById('total-passages').textContent = 
            formatter.format(dados.total_passagens);

        // Contar número de veículos (da API de ranking)
        const ranking = await axios.get('/api/ranking');
        const uniqueVehicles = new Set(ranking.data.map(r => r.placa));
        document.getElementById('total-vehicles').textContent = 
            uniqueVehicles.size;

    } catch (error) {
        console.error('❌ Erro ao carregar métricas:', error);
        mostrarErro('Erro ao carregar métricas');
    }
}

// ====================================================
// ANIMAR BARRAS DE PROGRESSO
// ====================================================

function animarBarra(elementId, maxWidth) {
    const element = document.getElementById(elementId);
    let currentWidth = 0;
    const targetWidth = Math.random() * maxWidth + 20;
    
    const interval = setInterval(() => {
        if (currentWidth >= targetWidth) {
            clearInterval(interval);
        } else {
            currentWidth += 1;
            element.style.width = currentWidth + '%';
        }
    }, 20);
}

// ====================================================
// CARREGAR GRÁFICOS
// ====================================================

async function carregarGraficos() {
    try {
        // Gráfico de timeline
        await criarGraficoTimeline();
        
        // Gráfico de categorias
        await criarGraficoCategoria();
        
        // Gráfico de ranking
        await criarGraficoRanking();
        
    } catch (error) {
        console.error('❌ Erro ao carregar gráficos:', error);
        mostrarErro('Erro ao criar gráficos');
    }
}

// ====================================================
// GRÁFICO: TIMELINE (CO₂ ao longo do tempo)
// ====================================================

async function criarGraficoTimeline() {
    try {
        const response = await axios.get('/api/periodos');
        const dados = response.data;

        // Preparar dados para o gráfico
        const labels = dados.map(d => d.mes);
        const co2Data = dados.map(d => d.co2_g);
        const combustivelData = dados.map(d => d.combustivel_ml);

        const ctx = document.getElementById('timelineChart').getContext('2d');
        
        charts.timeline = new Chart(ctx, {
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
                        pointBackgroundColor: '#047857',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 7
                    },
                    {
                        label: 'Combustível (ml)',
                        data: combustivelData,
                        borderColor: '#f97316',
                        backgroundColor: 'rgba(249, 115, 22, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#ea580c',
                        yAxisID: 'y1',
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 12, weight: 600 },
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: { size: 14, weight: 700 },
                        bodyFont: { size: 12 },
                        padding: 15,
                        borderRadius: 8,
                        displayColors: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'CO₂ (gramas)'
                        },
                        grid: {
                            color: 'rgba(16, 185, 129, 0.05)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Combustível (ml)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(16, 185, 129, 0.05)'
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('❌ Erro ao criar gráfico de timeline:', error);
    }
}

// ====================================================
// GRÁFICO: CATEGORIAS (Pizza/Doughnut)
// ====================================================

async function criarGraficoCategoria() {
    try {
        const response = await axios.get('/api/categorias');
        const dados = response.data;

        const labels = dados.map(d => d.categoria);
        const co2Data = dados.map(d => d.co2_g);

        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        const cores = [
            '#10b981',  // Verde
            '#047857',  // Verde escuro
            '#6d28d9',  // Roxo
            '#f97316',  // Laranja
            '#0ea5e9',  // Azul
            '#ec4899'   // Rosa
        ];

        charts.category = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: co2Data,
                    backgroundColor: cores.slice(0, labels.length),
                    borderColor: '#fff',
                    borderWidth: 2,
                    hoverBorderColor: '#10b981',
                    hoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { size: 12, weight: 600 },
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: { size: 14, weight: 700 },
                        bodyFont: { size: 12 },
                        padding: 12,
                        borderRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed.toFixed(0)}g (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('❌ Erro ao criar gráfico de categorias:', error);
    }
}

// ====================================================
// GRÁFICO: RANKING (Barra horizontal)
// ====================================================

async function criarGraficoRanking() {
    try {
        const response = await axios.get('/api/ranking');
        const dados = response.data.slice(0, 10); // Top 10

        const labels = dados.map(d => d.placa);
        const co2Data = dados.map(d => d.co2_g);

        const ctx = document.getElementById('rankingChart').getContext('2d');
        
        charts.ranking = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'CO₂ Evitado (g)',
                    data: co2Data,
                    backgroundColor: [
                        '#10b981', '#059669', '#047857', '#065f46', '#064e3b',
                        '#6d28d9', '#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd'
                    ],
                    borderColor: '#047857',
                    borderWidth: 1,
                    borderRadius: 8,
                    hoverBackgroundColor: '#047857'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: { size: 13, weight: 700 },
                        bodyFont: { size: 12 },
                        padding: 12,
                        borderRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `CO₂ Evitado: ${context.parsed.x.toFixed(0)}g`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(16, 185, 129, 0.05)'
                        },
                        title: {
                            display: true,
                            text: 'Gramas de CO₂'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('❌ Erro ao criar gráfico de ranking:', error);
    }
}

// ====================================================
// UTILIDADES
// ====================================================

function mostrarErro(mensagem) {
    console.error(mensagem);
    // Aqui você pode adicionar um toast notification
}

// ====================================================
// NAVEGAÇÃO ATIVA
// ====================================================

function atualizarNavegacao() {
    const path = window.location.pathname;
    const links = document.querySelectorAll('.nav-link');
    
    links.forEach(link => {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Chamar ao carregar
atualizarNavegacao();

// Atualizar ao mudar de página
window.addEventListener('popstate', atualizarNavegacao);