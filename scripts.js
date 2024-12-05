// Função para incluir o conteúdo HTML dinamicamente
function loadHTML(id, file) {
    fetch(file)
        .then(response => response.text())
        .then(html => {
            document.getElementById(id).innerHTML = html;
        })
        .catch(err => console.log('Erro ao carregar o conteúdo: ', err));
}

// Carrega os arquivos HTML quando a página é carregada
window.onload = () => {
    loadHTML('campeonatos-container', 'campeonatos.html');
    loadHTML('navbar-container', 'navbar.html');
    loadHTML('comunicacao-container', 'comunicacao.html');
    loadHTML('eventos-container', 'eventos.html');
};
