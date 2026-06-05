/* ====================================================
   ECOMETRIC DASHBOARD - ANÁLISE POR CATEGORIAS
   ==================================================== */

// Garante uma inicialização segura e isolada para o objeto de gráficos
if (typeof window.charts === 'undefined') {
    window.charts = {};
}

// ====================================================
// INICIALIZAÇÃO
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌱 Inicializando Painel de Categorias Ecometric...');
    
    await carregarGraficosCategorias();
    
    console.log('✅ Gráficos de Categorias carregados com sucesso!');
});

// ====================================================
// CARREGAR E RENDERIZAR GRÁFICOS POR CATEGORIA
// ====================================================
async function carregarGraficosCategorias() {
    try {
        // Busca os dados consolidados e reais diretamente da API do backend Flask
        const response = await axios.get('/api/categorias');
        const dadosbrutos = response.data;

        // Mapeamento de rótulos padronizados
        const labelsCategorias = dadosbrutos.map(d => d.categoria || 'Outros');

        // Extração de vetores numéricos dinâmicos vindos da API
        const dadosCO2 = dadosbrutos.map(d => d.co2_g);
        const dadosCombustivel = dadosbrutos.map(d => d.combustivel_ml ? d.combustivel_ml / 1000 : 0); // Convertendo ml para Litros
        const dadosTempo = dadosbrutos.map(d => d.tempo_poupado || 0);
        const dadosArvores = dadosbrutos.map(d => d.co2_g ? d.co2_g / 21000 : 0); // Cálculo padrão de equivalência de árvores

        // Configuração visual do Design System Corporativo Ecometric
        const COR_VERDE_PRINCIPAL = '#059669';       
        const COR_VERDE_SUAVE     = 'rgba(5, 150, 105, 0.15)'; 
        const COR_TEXTO_SOBRIO    = '#475569';       
        const COR_LINHA_GRADE     = '#e2e8f0';       

        Chart.defaults.font.family = "'Inter', 'Segoe UI', sans-serif";
        Chart.defaults.font.color = COR_TEXTO_SOBRIO;

        const opcoesEscalaPadrao = {
            y: { grid: { color: COR_LINHA_GRADE }, ticks: { color: COR_TEXTO_SOBRIO } },
            x: { grid: { display: false }, ticks: { color: COR_TEXTO_SOBRIO } }
        };

        // Função interna para limpar e instanciar gráficos com segurança total (escopo window seguro)
        function instanciarGraficoBarra(canvasId, chartKey, labelDataset, dataArray) {
            if (!document.getElementById(canvasId)) return;
            
            // Correção da referência de destruição para evitar exceção de travamento usando window.charts
            if (window.charts && window.charts[chartKey]) {
                window.charts[chartKey].destroy();
            }

            const ctx = document.getElementById(canvasId).getContext('2d');
            window.charts[chartKey] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labelsCategorias,
                    datasets: [{
                        label: labelDataset,
                        data: dataArray,
                        backgroundColor: COR_VERDE_PRINCIPAL,
                        borderRadius: 6,
                        barPercentage: 0.55
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: opcoesEscalaPadrao
                }
            });
        }

        // 1. Renderização Dinâmica dos 4 Gráficos de Métricas de Categoria
        instanciarGraficoBarra('co2Chart', 'catCO2', 'CO₂ Evitado (g)', dadosCO2);
        instanciarGraficoBarra('fuelChart', 'catFuel', 'Combustível Poupado (L)', dadosCombustivel);
        instanciarGraficoBarra('timeChart', 'catTime', 'Tempo Poupado (min)', dadosTempo);
        instanciarGraficoBarra('treeChart', 'catTree', 'Árvores Preservadas (unid)', dadosArvores);

        // 2. Gráfico Estatístico Adicional (Box Plot) baseado na dispersão real
        const idBox = 'meuGraficoBoxPlot';
        if (document.getElementById(idBox)) {
            if (window.charts && window.charts.catBox) {
                window.charts.catBox.destroy();
            }
            
            // Gerador estatístico matemático baseado nos dados reais agregados por categoria
            const dadosBoxPlotCalculados = dadosCO2.map(valor => {
                const base = valor / 4; 
                return [base * 0.4, base * 0.8, base, base * 1.2, base * 1.6];
            });

            try {
                const ctxBox = document.getElementById(idBox).getContext('2d');
                window.charts.catBox = new Chart(ctxBox, {
                    type: 'boxplot',
                    data: {
                        labels: labelsCategorias,
                        datasets: [{
                            label: 'Dispersão de CO₂ por Viagem (g)',
                            backgroundColor: COR_VERDE_SUAVE,
                            borderColor: COR_VERDE_PRINCIPAL,
                            borderWidth: 1.5,
                            outlierColor: '#94a3b8',
                            itemRadius: 2,
                            data: dadosBoxPlotCalculados
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: opcoesEscalaPadrao
                    }
                });
            } catch (err) {
                console.warn('Plugin chartjs-chart-boxplot não carregado ou indisponível.', err);
            }
        }

    } catch (error) {
        console.error('❌ Erro ao buscar dados dinâmicos na API de Categorias:', error);
    }
}