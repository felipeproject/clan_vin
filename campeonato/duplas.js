// Função principal para carregar equipes
async function carregarEquipes() {
    try {
        const url = `equipes.json?t=${new Date().getTime()}`; // Adiciona um timestamp para evitar cache
        const response = await fetch(url);

        // Verifica se a resposta foi bem-sucedida
        if (!response.ok) {
            throw new Error(`Erro ao carregar o arquivo JSON: ${response.statusText}`);
        }

        // Analisa o JSON
        const data = await response.json();
        exibirEquipes(data.equipes); // Exibe as equipes
        mostrarMensagemSucesso("Equipes carregadas com sucesso!"); // Mensagem de sucesso
    } catch (error) {
        console.error('Erro ao carregar equipes:', error);
        mostrarMensagemErro('Ocorreu um erro ao carregar as equipes. Tente novamente mais tarde.');
    }
}

// Função para exibir as equipes
function exibirEquipes(equipes) {
    const container = document.getElementById('equipesContainer');
    container.innerHTML = ''; // Limpa o conteúdo anterior

    equipes.forEach(equipe => {
        const { dupla, imagens } = equipe;
        const [nick1, nick2] = dupla;
        const link1 = `https://pubg.op.gg/user/${nick1}`;
        const link2 = nick2 === 'Sem Jogador' ? '#' : `https://pubg.op.gg/user/${nick2}`;

        container.innerHTML += `
            <div class="dupla">
                <div class="card">
                    <img src="imagens/${imagens[0]}" alt="${nick1}">
                    <a href="${link1}" target="_blank" class="link-nome">${nick1}</a>
                </div>
                <div class="icon">
                    <img src="imagens/icone_partido.png" alt="Ícone de Partido" class="partido-icon">
                </div>
                <div class="card">
                    <img src="imagens/${imagens[1]}" alt="${nick2}" class="${nick2 === 'Sem Jogador' ? 'pulse' : ''}">
                    <a href="${link2}" target="_blank" class="link-nome">${nick2}</a>
                </div>
            </div>`;
    });
}


// Chama a função para carregar as equipes ao carregar a página
document.addEventListener('DOMContentLoaded', carregarEquipes);
