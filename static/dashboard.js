/* ====================================================
   ECOMETRIC DASHBOARD - SCRIPTS PRINCIPAIS UNIFICADOS E PROTEGIDOS
   ==================================================== */

let charts = {};
let chartClienteInstance = null; // Instância isolada do gráfico do cliente

// Função global de proteção para ofuscar os caracteres centrais da placa
function mascararPlaca(placa) {
    if (!placa || placa.length < 4) return placa;
    return placa.substring(0, 2) + '***' + placa.substring(placa.length - 2);
}

// ====================================================
// INICIALIZAÇÃO BASEADA EM PERFIL DE SESSÃO
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌱 Inicializando Dashboard Ecometric Protegido...');
    console.log('👤 Perfil Detetado:', window.USER_PERFIL);

    // Fluxo Condicional de Inicialização de Abas e Requisições
    if (window.USER_PERFIL === 'admin') {
        // Fluxo Administrativo Geral
        alternarAba('visao-geral');
        await carregarMetricas();
        await carregarGraficos();
    } 
    else if (window.USER_PERFIL === 'cliente') {
        // Fluxo de Cliente Individualizado
        alternarAba('area-cliente');
        
        // Se a sessão do Flask já proveu a placa do cliente, busca os dados automaticamente
        if (window.USER_PLACA) {
            document.getElementById('input-placa-login').value = window.USER_PLACA;
            carregarDadosCliente(window.USER_PLACA);
        }
    } else {
        // Fallback de segurança (caso não haja sessão ativa na rota)
        alternarAba('visao-geral');
        await carregarMetricas();
        await carregarGraficos();
    }
    
    console.log('✅ Inicialização concluída com sucesso!');
});

// ====================================================
// CARREGAR MÉTRICAS PRINCIPAIS (ADMIN/GLOBAL)
// ====================================================
async function carregarMetricas() {
    try {
        const response = await axios.get('/api/metricas');
        const dados = response.data;

        // Formatador de números padrão pt-BR
        const formatter = new Intl.NumberFormat('pt-BR', {
            maximumFractionDigits: 2
        });

        // Atualizar valores na tela tratendo os nomes exatos retornados pela API
        if (document.getElementById('co2-value')) {
            document.getElementById('co2-value').textContent = formatter.format(dados.co2_total_g || dados.co2_evitado_g || 0);
        }
        if (document.getElementById('time-value')) {
            document.getElementById('time-value').textContent = formatter.format(dados.tempo_total_min || dados.tempo_poupado_min || 0);
        }
        if (document.getElementById('fuel-value')) {
            document.getElementById('fuel-value').textContent = formatter.format(dados.combustivel_total_ml || dados.combustivel_poupado_ml || 0);
        }
        if (document.getElementById('tree-value')) {
            const arvores = dados.equivalente_arvores || dados.arvores_equivalentes || 0;
            document.getElementById('tree-value').textContent = arvores.toFixed(2);
        }

        // Atualizar barras de progresso animadas originais
        animarBarra('co2-bar', 60);
        animarBarra('time-bar', 70);
        animarBarra('fuel-bar', 50);
        animarBarra('tree-bar', 80);

        // Atualizar totalizador inferior de passagens
        if (document.getElementById('total-passages')) {
            document.getElementById('total-passages').textContent = formatter.format(dados.total_passagens || 0);
        }

        // Contar número de veículos únicos a partir do endpoint de ranking
        if (document.getElementById('total-vehicles')) {
            const ranking = await axios.get('/api/ranking');
            const uniqueVehicles = new Set(ranking.data.map(r => r.placa));
            document.getElementById('total-vehicles').textContent = uniqueVehicles.size;
        }

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
    if (!element) return;
    
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
// CARREGAR GRÁFICOS GLOBAIS (ADMIN)
// ====================================================
async function carregarGraficos() {
    try {
        await criarGraficoTimeline();
        await criarGraficoCategoria();
        await criarGraficoRanking(); 
    } catch (error) {
        console.error('❌ Erro ao carregar gráficos globais:', error);
        mostrarErro('Erro ao criar gráficos');
    }
}

// ====================================================
// GRÁFICO: TIMELINE (CO₂ ao longo do tempo)
// ====================================================
async function criarGraficoTimeline() {
    const canvas = document.getElementById('timelineChart');
    if (!canvas) return;
    
    try {
        const response = await axios.get('/api/periodos');
        const dados = response.data;

        const labels = dados.map(d => d.mes);
        const co2Data = dados.map(d => d.co2_g);
        const combustivelData = dados.map(d => d.combustivel_ml);

        const ctx = canvas.getContext('2d');
        if (charts.timeline) charts.timeline.destroy();
        
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
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return;

    try {
        const response = await axios.get('/api/categorias');
        const dados = response.data;

        const labels = dados.map(d => d.categoria);
        const co2Data = dados.map(d => d.co2_g);

        const ctx = canvas.getContext('2d');
        const cores = ['#10b981', '#047857', '#6d28d9', '#f97316', '#0ea5e9', '#ec4899'];

        if (charts.category) charts.category.destroy();

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
    const canvas = document.getElementById('rankingChart');
    if (!canvas) return;

    try {
        const response = await axios.get('/api/ranking');
        const dados = response.data.slice(0, 10);

        // PROTEÇÃO: Mascarar rótulos das placas no gráfico geral
        const labels = dados.map(d => d.placa ? mascararPlaca(d.placa) : 'Veículo');
        const co2Data = dados.map(d => d.co2_g);

        const ctx = canvas.getContext('2d');
        if (charts.ranking) charts.ranking.destroy();
        
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
// MOTOR DE ALTERNÂNCIA DE ABAS (TABS LOGIC)
// ====================================================
function alternarAba(abaNome) {
    // Oculta todos os blocos de conteúdo das abas
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    
    // Reseta o estilo visual de todos os botões de controle de abas
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.style.backgroundColor = 'transparent';
        btn.style.color = '#333';
        btn.classList.remove('active');
    });

    // Ativa condicionalmente o bloco alvo
    if (abaNome === 'visao-geral') {
        const tabGeral = document.getElementById('tab-visao-geral');
        if (tabGeral) tabGeral.style.display = 'block';
    } 
    else if (abaNome === 'area-cliente') {
        const tabCliente = document.getElementById('tab-area-cliente');
        if (tabCliente) tabCliente.style.display = 'block';
        carregarModelosDropdown(); 
    }

    // Alinha o estilo do botão que disparou o evento (caso exista o clique físico)
    if (event && event.target && event.target.classList.contains('tab-btn')) {
        event.target.style.backgroundColor = '#2ecc71';
        event.target.style.color = 'white';
        event.target.classList.add('active');
    }
}

// =========================================================
// ÁREA DO CLIENTE: BUSCA INDIVIDUAL E HISTÓRICO PROTEGIDO
// =========================================================
function carregarDadosCliente(placaForcada = null) {
    const placaInput = document.getElementById('input-placa-login') ? document.getElementById('input-placa-login').value.trim() : '';
    const placaAlvo = placaForcada || placaInput;

    if (!placaAlvo) return alert('Por favor, informe uma placa válida!');

    axios.get(`/api/cliente/${placaAlvo}`).then(response => {
        const data = response.data;
        
        // Trata os fallbacks caso o objeto interno mude levemente de nome entre estruturas
        const perfilVeiculo = data.perfil || {};
        const placaOriginal = perfilVeiculo.placa || placaAlvo;
        
        document.getElementById('dashboard-individual-cliente').style.display = 'block';
        
        // PROTEÇÃO VISUAL MANTIDA:
        const txtPerfil = document.getElementById('txt-placa-perfil');
        if (txtPerfil) {
            txtPerfil.innerText = mascararPlaca(placaOriginal).toUpperCase(); // Exibe mascarado
            txtPerfil.setAttribute('data-placa-real', placaOriginal);          // Salva original em background
        }
        
        // Atualiza os contadores individuais com fallbacks seguros de chaves da API
        const co2Cli = perfilVeiculo.co2_total_g || perfilVeiculo.co2_evitado_g || 0;
        const arvCli = perfilVeiculo.equivalente_arvores || perfilVeiculo.arvores_equivalentes || 0;
        
        document.getElementById('cli-co2').innerText = `${co2Cli.toFixed(1)}g`;
        document.getElementById('cli-arvores').innerText = arvCli.toFixed(2);
        document.getElementById('cli-capcoins').innerText = perfilVeiculo.saldo_capcoins || 0;

        // Renderização da tabela de histórico
        const tbody = document.getElementById('tbody-historico-cliente');
        if (tbody) {
            tbody.innerHTML = '';
            if (!data.historico || data.historico.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:15px; color:#666;">Ainda não existem registos para este veículo.</td></tr>';
            } else {
                data.historico.forEach(p => {
                    // Adaptável para formatações locais pt-BR / pt-PT de forma elegante
                    const dataFormatada = new Date(p.data_hora).toLocaleString('pt-BR');
                    tbody.innerHTML += `
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding:12px 10px; color:#555;">${dataFormatada}</td>
                            <td style="padding:12px 10px; font-weight:600;">${p.local}</td>
                            <td style="padding:12px 10px; color:#e67e22; font-weight:bold;">⏱️ ${p.tempo_poupado}m</td>
                            <td style="padding:12px 10px; color:#2ecc71; font-weight:bold;">🪙 +${p.capcoins}</td>
                        </tr>`;
                });
            }
        }

        // Gráfico de evolução em tempo real individual do cliente
        const canvasCli = document.getElementById('chartEvolucaoCliente');
        if (canvasCli) {
            const ctx = canvasCli.getContext('2d');
            if (chartClienteInstance) chartClienteInstance.destroy();
            
            // Fallbacks de arrays para evitar falhas caso a listagem de meses esteja vazia
            const mesesEvolucao = (data.evolucao && data.evolucao.meses) ? data.evolucao.meses : [];
            const co2Evolucao = (data.evolucao && data.evolucao.co2) ? data.evolucao.co2 : [];

            chartClienteInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: mesesEvolucao,
                    datasets: [{ 
                        label: 'Meu CO₂ Evitado (g)', 
                        data: co2Evolucao, 
                        borderColor: '#2ecc71', 
                        backgroundColor: 'rgba(46, 204, 113, 0.1)', 
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3 
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true
                }
            });
        }
    }).catch((err) => {
        console.error(err);
        alert('Erro ao procurar dados. Certifique-se de que o veículo possui passagens registadas.');
    });
}

// =========================================================
// SIMULAR USO DA TAGGY EM TEMPO REAL COM ATUALIZAÇÃO SÍNCRONA
// =========================================================
function simularUsoTaggy(botao) {
    // Lê o atributo original nos bastidores livre de asteriscos '***'
    const placaReal = document.getElementById('txt-placa-perfil') ? document.getElementById('txt-placa-perfil').getAttribute('data-placa-real') : null;
    if (!placaReal || placaReal === '-') return alert('Aceda ao seu painel primeiro.');

    const textoOriginal = botao.innerHTML;
    botao.innerHTML = 'A abrir catraca... ⏳';
    botao.disabled = true;
    botao.style.backgroundColor = '#e67e22';

    axios.post('/api/cliente/usar_taggy', { placa: placaReal, local: 'Shopping Tacaruna (Demonstração)' })
        .then(response => {
            // Re-alimenta o input oculto de login caso o motor precise ler
            if (document.getElementById('input-placa-login')) {
                document.getElementById('input-placa-login').value = placaReal;
            }
            
            // Recarrega painel individual imediatamente na tela
            carregarDadosCliente(placaReal);
            
            // Se o perfil logado for admin, atualiza também a visão global de fundo
            if (window.USER_PERFIL === 'admin') {
                carregarMetricas();
                carregarGraficos();
            }

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

// =========================================================
// CADASTRO DE NOVOS VEÍCULOS
// =========================================================
function carregarModelosDropdown() {
    const select = document.getElementById('cad-modelo');
    if (!select) return;

    axios.get('/api/modelos').then(response => {
        select.innerHTML = '<option value="">Selecione o Modelo</option>';
        response.data.forEach(m => {
            select.innerHTML += `<option value="${m.id}">${m.marca} ${m.nome} (${m.ano})</option>`;
        });
    }).catch(err => console.error('Erro ao carregar modelos do catálogo:', err));
}

function ejecutarCadastroVeiculo() {
    const placa = document.getElementById('cad-placa') ? document.getElementById('cad-placa').value.trim() : '';
    const modeloId = document.getElementById('cad-modelo') ? document.getElementById('cad-modelo').value : '';
    const msg = document.getElementById('msg-cadastro');

    if (!placa || !modeloId) {
        if (msg) msg.innerHTML = `<span style="color: red;">⚠️ Preencha todos os campos.</span>`;
        return;
    }

    axios.post('/api/cliente/cadastro', { placa: placa.toUpperCase(), modelo_id: modeloId })
        .then(res => {
            if (msg) msg.innerHTML = `<span style="color: green;">${res.data.mensagem}</span>`;
            if (document.getElementById('cad-placa')) document.getElementById('cad-placa').value = '';
            if (document.getElementById('cad-modelo')) document.getElementById('cad-modelo').value = '';
        })
        .catch(err => {
            if (msg) msg.innerHTML = `<span style="color: red;">${err.response?.data?.erro || 'Erro no registo.'}</span>`;
        });
}

// ====================================================
// UTILIDADES / CONTROLE DE LINKS NAV
// ====================================================
function mostrarErro(mensagem) { console.error(mensagem); }

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

// Escutas de roteamento nativo de interface
atualizarNavegacao();
window.addEventListener('popstate', atualizarNavegacao);
// ====================================================
// COMPLEMENTOS DE NAVEGAÇÃO INTELLIGENT SPA (FIX)
// ====================================================

/**
 * Permite que o Administrador role a tela de forma suave até o gráfico 
 * ou métrica selecionada no menu superior sem recarregar a página.
 */
function focarElementoAdmin(idElemento) {
    // Garante primeiro que a aba de Visão Geral (Admin) está visível
    alternarAba('visao-geral');
    
    // Procura o elemento correspondente (ex: categoryChart, rankingChart...)
    const el = document.getElementById(idElemento);
    if (el) {
        // Rola a tela de forma suave até centralizar o componente solicitado
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Destaca brevemente a borda do gráfico para o Admin saber onde a tela parou
        const container = el.closest('.chart-container') || el.closest('.metric-card');
        if (container) {
            container.style.transition = '0.5s';
            container.style.boxShadow = '0 0 15px rgba(46, 204, 113, 0.6)';
            setTimeout(() => {
                container.style.boxShadow = '';
            }, 1500);
        }
    }
}

/**
 * Controla o clique no botão "Ranking" do Cliente.
 * Mantém o cliente na aba dele e foca no painel individual dele para ver o progresso.
 */
function mostrarRankingNoCliente() {
    // 1. Garante que ele continua na Área do Cliente protegida
    alternarAba('area-cliente');
    
    // 2. Se ele já consultou a placa dele, move suavemente até o gráfico de evolução individual
    const graficoCliente = document.getElementById('chartEvolucaoCliente');
    const painelIndividual = document.getElementById('dashboard-individual-cliente');
    
    if (painelIndividual && painelIndividual.style.display !== 'none' && graficoCliente) {
        graficoCliente.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
        // Se ele ainda não digitou a placa, rola suavemente até o input de consulta
        const inputPlaca = document.getElementById('input-placa-login');
        if (inputPlaca) {
            inputPlaca.scrollIntoView({ behavior: 'smooth', block: 'center' });
            inputPlaca.focus();
        }
    }
}

/**
 * Controla o clique na "Loja Sustentável" do Cliente.
 * Exibe um alerta amigável de que os CapCoins coletados estão salvos!
 */
function mostrarLojaNoCliente() {
    alternarAba('area-cliente');
    
    // Obtém o saldo atual de CapCoins que está na tela
    const saldoElement = document.getElementById('cli-capcoins');
    const saldo = saldoElement ? saldoElement.innerText : '0';
    
    alert(`🪙 Bem-vindo à Loja Sustentável Ecometric!\n\nSeu saldo atual é de: ${saldo} CapCoins.\n\nO catálogo de recompensas (descontos em pedágios, estacionamentos e recargas elétricas) estará disponível em breve na próxima atualização do sistema!`);
}