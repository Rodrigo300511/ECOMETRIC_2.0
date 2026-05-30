document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚗 Carregando veículos...');

    await carregarVeiculos();

    console.log('✅ Veículos carregados!');
});

async function carregarVeiculos() {

    try {

        const response = await axios.get('/api/veiculos');
        const dados = response.data;

        const tbody = document.getElementById('tbody');

        if (!dados || dados.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align:center;padding:2rem;">
                        Nenhum veículo encontrado
                    </td>
                </tr>
            `;

            return;
        }

        tbody.innerHTML = dados.map(v => `
            <tr>
                <td><strong>${v.placa}</strong></td>
                <td>${v.modelo}</td>
                <td>${v.marca}</td>
                <td>${v.categoria}</td>
                <td>${v.passagens}</td>
                <td>${v.co2_g.toFixed(2)}</td>
                <td>${v.capcoins}</td>
            </tr>
        `).join('');

    }
    catch(error) {

        console.error(error);

        document.getElementById('tbody').innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center;padding:2rem;">
                    Erro ao carregar veículos
                </td>
            </tr>
        `;
    }
}