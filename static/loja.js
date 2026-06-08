/* ====================================================
   ECOMETRIC DASHBOARD - SISTEMA DE RECOMPENSAS (LOJA)
   ==================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const placa = window.CLIENTE_PLACA;
    
    if (!placa) {
        console.error('❌ Erro: Identificação da placa do cliente ausente na sessão.');
        exibirMensagem('❌ Você precisa estar logado com uma placa activa para acessar a loja.', '#dc2626', '#fef2f2');
        return;
    }

    // Atualiza a interface com a placa conectada
    document.getElementById('lbl-placa-usuario').textContent = placa.toUpperCase();

    // Inicializa a carga dos dados da loja
    carregarDadosLoja(placa);
});

/**
 * Busca simultaneamente o saldo do usuário e o catálogo de prêmios do Banco
 */
async function carregarDadosLoja(placa) {
    try {
        // 1. Busca os dados de perfil/saldo usando a rota que você já tem no app.py
        const responseCliente = await axios.get(`/api/cliente/${placa}`);
        const dadosCliente = responseCliente.data;
        
        let saldoAtual = 0;

        if (dadosCliente && dadosCliente.perfil && dadosCliente.perfil.saldo_capcoins !== undefined) {
            saldoAtual = dadosCliente.perfil.saldo_capcoins;
        }

        // Atualiza o elemento visual na tela da loja com o saldo real do carro
        document.getElementById('saldo-capcoins-loja').textContent = `🪙 ${saldoAtual}`;

        // 2. Busca a lista completa de recompensas cadastradas no sistema
        const responseLoja = await axios.get('/api/recompensas');
        const listaRecompensas = responseLoja.data;

        renderizarCatalogo(listaRecompensas, placa);

    } catch (error) {
        console.error('❌ Erro ao carregar dados da loja:', error);
        document.getElementById('grid-recompensas').innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; color: #dc2626; padding: 20px; font-weight: 500;">
                ⚠️ Erro ao carregar a loja ou o saldo. Verifique se o servidor está ativo.
            </div>
        `;
    }
}

/**
 * Renderiza dinamicamente os cards de produtos na tela
 */
function renderizarCatalogo(recompensas, placa) {
    const grid = document.getElementById('grid-recompensas');
    
    if (!recompensas || recompensas.length === 0) {
        grid.innerHTML = `<div style="grid-column:1/-1; text-align:center;">Nenhuma recompensa disponível no momento.</div>`;
        return;
    }

    // Mapeamento de emojis por categoria para deixar a interface intuitiva
    const emojisCategoria = {
        'sustentavel': '🌳',
        'servico': '🎫',
        'produto': '🎁',
        'educacao': '📚'
    };

    grid.innerHTML = recompensas.map(item => {
        // Tratamento para garantir o match do emoji mesmo se vier em maiúsculas do banco
        const categoriaLimpa = item.categoria ? item.categoria.toLowerCase().trim() : '';
        const emoji = emojisCategoria[categoriaLimpa] || '✨';
        
        return `
            <div class="card" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; transition: transform 0.2s; box-shadow: var(--shadow-sm);">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <span style="font-size: 2rem; margin-bottom: 10px;">${emoji}</span>
                        <span class="badge-categoria" style="text-transform: capitalize;">${item.categoria || 'Geral'}</span>
                    </div>
                    <h3 style="margin: 10px 0 5px 0; font-size: 1.15rem; color: var(--text-dark);">${item.nome}</h3>
                    <p style="margin: 0 0 15px 0; color: var(--text-light); font-size: 0.88rem; line-height: 1.4;">
                        ${item.descricao || 'Sem descrição disponível.'}
                    </p>
                </div>
                
                <div style="margin-top: 15px;">
                    <div style="font-weight: 700; color: var(--dark-green); font-size: 1.1rem; margin-bottom: 12px;">
                        🪙 ${item.custo} <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-light);">CapCoins</span>
                    </div>
                    <button 
                        onclick="resgatarPremio('${placa}', ${item.id}, '${item.nome}')" 
                        class="nav-link" 
                        style="width: 100%; display: block; text-align: center; background: var(--gradient-green); color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: opacity 0.2s;"
                        onmouseover="this.style.opacity=0.9"
                        onmouseout="this.style.opacity=1"
                    >
                        Resgatar Prêmio
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Dispara a ação de resgate para o backend
 */
async function resgatarPremio(placa, idRecompensa, nomeRecompensa) {
    if (!confirm(`Confirmar o resgate de: "${nomeRecompensa}"?`)) return;

    try {
        const response = await axios.post('/api/loja/resgatar', {
            placa: placa,
            recompensa_id: idRecompensa
        });

        if (response.data && response.data.status === 'sucesso') {
            exibirMensagem(`🎉 Sucesso! Você resgatou: ${nomeRecompensa}. Verifique seu e-mail cadastrado!`, '#166534', '#d1fae5');
            // Recarrega os saldos instantaneamente após a dedução
            carregarDadosLoja(placa);
        }
    } catch (error) {
        console.error('❌ Erro ao resgatar recompensa:', error);
        const msgErro = error.response?.data?.erro || 'Saldo insuficiente ou falha no processamento.';
        exibirMensagem(`⚠️ Falha no resgate: ${msgErro}`, '#dc2626', '#fef2f2');
    }
}

/**
 * Função utilitária para exibir alertas flutuantes no topo da loja
 */
function exibirMensagem(texto, corTexto, corFundo) {
    const box = document.getElementById('mensagem-loja');
    if (!box) return;
    
    box.style.display = 'block';
    box.style.color = corTexto;
    box.style.backgroundColor = corFundo;
    box.style.border = `1px solid ${corTexto}44`;
    box.textContent = texto;

    // Rola a página suavemente para cima para o usuário ler o alerta
    window.scrollTo({ top: 0, behavior: 'smooth' });
}