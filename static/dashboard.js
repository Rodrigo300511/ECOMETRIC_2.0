/* ====================================================
   ECOMETRIC DASHBOARD - SCRIPTS PRINCIPAIS PROTEGIDOS
   ==================================================== */

let charts = {};

// Função global de proteção para ofuscar os caracteres centrais da placa
function mascararPlaca(placa) {
    if (!placa || placa.length < 4) return placa;
    return placa.substring(0, 2) + '***' + placa.substring(placa.length - 2);
}

// ====================================================
// INICIALIZAÇÃO
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌱 Inicializando Dashboard Ecometric Protegido...');
    
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
        await criarGraficoTimeline();
        await criarGraficoCategoria();
        await criarGraficoRanking(); // Este agora irá ocultar as placas das barras
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
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: { font: { size: 12, weight: 600 }, padding: 20, usePointStyle: true }
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
                        title: { display: true, text: 'CO₂ (gramas)' },
                        grid: { color: 'rgba(16, 185, 129, 0.05)' }
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        title: { display: true, text: 'Combustível (ml)' },
                        grid: { drawOnChartArea: false }
                    },
                    x: { grid: { color: 'rgba(16, 185, 129, 0.05)' } }
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
        const cores = ['#10b981', '#047857', '#6d28d9', '#f97316', '#0ea5e9', '#ec4899'];

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
                        labels: { font: { size: 12, weight: 600 }, padding: 20, usePointStyle: true }
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
// GRÁFICO: RANKING GLOBAL (Barra horizontal protegida)
// ====================================================
async function criarGraficoRanking() {
    try {
        const response = await axios.get('/api/ranking');
        const dados = response.data.slice(0, 10);

        // PROTEÇÃO: Mascarar rótulos das placas no gráfico geral
        const labels = dados.map(d => mascararPlaca(d.placa));
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
                    legend: { display: false },
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
                        grid: { color: 'rgba(16, 185, 129, 0.05)' },
                        title: { display: true, text: 'Gramas de CO₂' }
                    },
                    y: { grid: { display: false } }
                }
            }
        });
    } catch (error) {
        console.error('❌ Erro ao criar gráfico de ranking:', error);
    }
}

// ====================================================
// UTILIDADES / NAVEGAÇÃO
// ====================================================
function mostrarErro(mensagem) { console.error(mensagem); }

function atualizarNavegacao() {
    const path = window.location.pathname;
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        if (link.getAttribute('href') === path) { link.classList.add('active'); } 
        else { link.classList.remove('active'); }
    });
}
atualizarNavegacao();
window.addEventListener('popstate', atualizarNavegacao);

// =========================================================
// AREA DO CLIENTE
// =========================================================
let chartClienteInstance = null;

function alternarAba(abaNome) {
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.style.backgroundColor = 'transparent';
        btn.style.color = '#333';
    });

    if (abaNome === 'visao-geral') {
        document.getElementById('tab-visao-geral').style.display = 'block';
        event.target.style.backgroundColor = '#2ecc71';
        event.target.style.color = 'white';
    } else if (abaNome === 'area-cliente') {
        document.getElementById('tab-area-cliente').style.display = 'block';
        event.target.style.backgroundColor = '#2ecc71';
        event.target.style.color = 'white';
        carregarModelosDropdown(); 
    }
}

function carregarModelosDropdown() {
    axios.get('/api/modelos').then(response => {
        const select = document.getElementById('cad-modelo');
        select.innerHTML = '<option value="">Selecione o Modelo</option>';
        response.data.forEach(m => {
            select.innerHTML += `<option value="${m.id}">${m.marca} ${m.nome} (${m.ano})</option>`;
        });
    }).catch(err => console.error('Erro ao carregar modelos:', err));
}

function ejecutarCadastroVeiculo() {
    const placa = document.getElementById('cad-placa').value;
    const modeloId = document.getElementById('cad-modelo').value;
    const msg = document.getElementById('msg-cadastro');

    axios.post('/api/cliente/cadastro', { placa, modelo_id: modeloId })
        .then(res => {
            msg.innerHTML = `<span style="color: green;">${res.data.mensagem}</span>`;
            document.getElementById('cad-placa').value = '';
        })
        .catch(err => msg.innerHTML = `<span style="color: red;">${err.response.data.erro}</span>`);
}

// Buscar e exibir os dados de impacto do cliente (Com Proteção Visual)
function carregarDadosCliente() {
    const placaInput = document.getElementById('input-placa-login').value;
    if (!placaInput) return alert('Por favor, informe uma placa!');

    axios.get(`/api/cliente/${placaInput}`).then(response => {
        const data = response.data;
        const placaOriginal = data.perfil.placa || placaInput;
        
        document.getElementById('dashboard-individual-cliente').style.display = 'block';
        
        // PROTEÇÃO VISUAL AQUI:
        const txtPerfil = document.getElementById('txt-placa-perfil');
        txtPerfil.innerText = mascararPlaca(placaOriginal).toUpperCase(); // Exibe mascarado na tela
        txtPerfil.setAttribute('data-placa-real', placaOriginal);          // Guarda a real nos bastidores
        
        document.getElementById('cli-co2').innerText = `${data.perfil.co2_total_g ? data.perfil.co2_total_g.toFixed(1) : 0}g`;
        document.getElementById('cli-arvores').innerText = data.perfil.equivalente_arvores ? data.perfil.equivalente_arvores.toFixed(2) : 0;
        document.getElementById('cli-capcoins').innerText = data.perfil.saldo_capcoins || 0;

        const tbody = document.getElementById('tbody-historico-cliente');
        tbody.innerHTML = '';
        if (data.historico.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:15px;">Ainda não existem registos para este veículo.</td></tr>';
        } else {
            data.historico.forEach(p => {
                const dataFormatada = new Date(p.data_hora).toLocaleString('pt-PT');
                tbody.innerHTML += `<tr>
                    <td style="padding:12px 10px;">${dataFormatada}</td>
                    <td style="padding:12px 10px;">${p.local}</td>
                    <td style="padding:12px 10px;">${p.tempo_poupado}m</td>
                    <td style="padding:12px 10px; color:#2ecc71; font-weight:bold;">+${p.capcoins}</td>
                </tr>`;
            });
        }

        const ctx = document.getElementById('chartEvolucaoCliente').getContext('2d');
        if (chartClienteInstance) chartClienteInstance.destroy();
        chartClienteInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.evolucao.meses,
                datasets: [{ 
                    label: 'CO₂ Evitado (g)', 
                    data: data.evolucao.co2, 
                    borderColor: '#2ecc71', 
                    backgroundColor: 'rgba(46, 204, 113, 0.2)', 
                    fill: true,
                    tension: 0.3 
                }]
            }
        });
    }).catch((err) => {
        console.error(err);
        alert('Erro ao procurar dados. Tem a certeza que a placa está correta?');
    });
}

// ==========================================
// SIMULAR USO DA TAGGY EM TEMPO REAL CORRIGIDO
// ==========================================
function simularUsoTaggy(botao) {
    // CORREÇÃO: Lê o atributo invisível de dados que criamos acima para não ler os asteriscos '***'
    const placaReal = document.getElementById('txt-placa-perfil').getAttribute('data-placa-real');
    if (!placaReal || placaReal === '-') return alert('Aceda ao seu painel primeiro.');

    const textoOriginal = botao.innerHTML;
    botao.innerHTML = 'A abrir catraca... ⏳';
    botao.disabled = true;
    botao.style.backgroundColor = '#e67e22';

    // Faz a requisição usando a placa limpa e verdadeira obtida dos bastidores
    axios.post('/api/cliente/usar_taggy', { placa: placaReal, local: 'Shopping Tacaruna (Demonstração)' })
        .then(response => {
            // Atualiza o input de login com a placa real antes de recarregar a tela
            document.getElementById('input-placa-login').value = placaReal;
            
            carregarDadosCliente();
            alert('✅ Catraca aberta sem filas!\n\nVocê poupou combustível, ajudou o ambiente e ganhou +3 CapCoins!');
        })
        .catch(error => {
            alert('Erro ao registar a passagem: ' + (error.response?.data?.erro || 'Erro desconhecido.'));
        })
        .finally(() => {
            botao.innerHTML = textoOriginal;
            botao.disabled = false;
            botao.style.backgroundColor = '#f39c12';
        });
}