/* ====================================================
   ECOMETRIC DASHBOARD - FLUXO DE AUTENTICAÇÃO E SESSÃO
   ==================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const formLogin = document.getElementById('form-login');
    if (!formLogin) return;

    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault(); // Impede o recarregamento padrão da página

        const usuarioInput = document.getElementById('usuario').value.trim();
        const senhaInput = document.getElementById('senha').value;
        const btnEntrar = document.getElementById('btn-entrar');
        const containerErro = document.getElementById('mensagem-erro');

        // Reset visual de erros
        containerErro.style.display = 'none';
        containerErro.textContent = '';
        btnEntrar.disabled = true;
        btnEntrar.textContent = 'Autenticando... ⏳';

        try {
            // Faz o pedido de autenticação à API do Flask
            const response = await axios.post('/api/login', {
                usuario: usuarioInput,
                senha: senhaInput
            });

            const data = response.data;

            console.log('🔐 Resposta de autenticação:', data);

            // Redirecionamento baseado no tipo de perfil retornado pelo Servidor
            if (data.perfil === 'admin') {
                console.log('💼 Acesso Administrativo concedido. Redirecionando...');
                window.location.href = '/'; // Redireciona para o Dashboard Geral
            } else if (data.perfil === 'cliente') {
                console.log('🚗 Acesso Cliente concedido. Redirecionando...');
                // Salva a sessão local da placa se o seu dashboard.js precisar ler
                localStorage.setItem('cliente_placa', data.placa);
                window.location.href = '/'; // Redireciona para o Dashboard que vai focar no cliente
            }

        } catch (error) {
            console.error('❌ Erro na autenticação:', error);
            
            containerErro.style.display = 'block';
            if (error.response && error.response.data && error.response.data.erro) {
                containerErro.textContent = `⚠️ ${error.response.data.erro}`;
            } else {
                containerErro.textContent = '⚠️ Erro ao conectar ao servidor. Tente novamente.';
            }
        } finally {
            // Restaura o botão de login
            btnEntrar.disabled = false;
            btnEntrar.textContent = 'Entrar no Painel';
        }
    });
});