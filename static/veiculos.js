/* ====================================================
   ECOMETRIC DASHBOARD - GESTÃO DE VEÍCULOS PROTEGIDOS
   ==================================================== */

// Garante uma inicialização segura e isolada para o objeto de gráficos se necessário
if (typeof window.charts === 'undefined') {
    window.charts = {};
}

/**
 * Aplica uma máscara de anonimização na placa do veículo para privacidade/LGPD (ex: ABC1234 -> AB***34)
 */
function mascararPlaca(placa) {
    if (!placa) return '---';
    const str = String(placa).trim();
    if (str.length < 4) return str;
    return str.substring(0, 2) + '***' + str.substring(str.length - 2);
}

// ====================================================
// INICIALIZAÇÃO CONTROLADA
// ====================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚗 [Ecometric] Inicializando listagem de veículos...');
    await carregarVeiculos();
    console.log('✅ Veículos carregados com sucesso!');
});

// ====================================================
// CARREGAR E EXIBIR LISTA DE VEÍCULOS
// ====================================================
async function carregarVeiculos() {
    const tbody = document.getElementById('tbody');
    if (!tbody) {
        console.error('❌ Erro crítico: Elemento <tbody id="tbody"> não foi encontrado no HTML.');
        return;
    }

    try {
        const response = await axios.get('/api/veiculos');
        const dados = response.data;

        if (!dados || dados.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="padding:20px;text-align:center;">
                        😢 Nenhum veículo encontrado no sistema.
                    </td>
                </tr>
            `;
            return;
        }

        // Preenchimento dinâmico e seguro aplicando o mascararPlaca
        tbody.innerHTML = dados.map(v => {
            const placaMascarada = mascararPlaca(v.placa).toUpperCase();
            const co2Formatado = typeof v.co2_g === 'number' ? v.co2_g.toFixed(2) : '0.00';
            
            return `
                <tr>
                    <td style="padding:12px;"><strong>${placaMascarada}</strong></td>
                    <td style="padding:12px;">${v.marca || '---'}</td>
                    <td style="padding:12px;">${v.modelo || '---'}</td>
                    <td style="padding:12px;"><span class="badge-categoria">${v.categoria || 'Outros'}</span></td>
                    <td style="padding:12px;">${v.passagens || 0}</td>
                    <td style="padding:12px; color:var(--primary-green, #10b981); font-weight:bold;">
                        ${co2Formatado} g
                    </td>
                    <td style="padding:12px; font-weight:600;">
                        🪙 ${v.capcoins || 0}
                    </td>
                </tr>
            `;
        }).join('');

    } catch (error) {
        console.error('❌ Erro ao processar requisição dos veículos:', error);
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="color:#dc2626; padding:20px; text-align:center; font-weight:bold;">
                    ⚠️ Erro ao carregar dados dos veículos. Verifique a consola do navegador.
                </td>
            </tr>
        `;
    }
}