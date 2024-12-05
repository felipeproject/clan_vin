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

// Função para abrir o pop-up e carregar conteúdo dinâmico
document.getElementById('times-btn').addEventListener('click', function () {
    // Exibir o pop-up
    document.getElementById('times-popup').style.display = 'flex';

    // Carregar o conteúdo dinâmico do arquivo "times.html"
    fetch('times.html')
        .then(response => response.text())
        .then(data => {
            // Inserir o conteúdo carregado no pop-up
            document.getElementById('popup-content').innerHTML = data;
        })
        .catch(error => {
            // Caso ocorra erro no carregamento do conteúdo
            document.getElementById('popup-content').innerHTML = 'Erro ao carregar o conteúdo.';
            console.error('Erro ao carregar conteúdo:', error);
        });
});

// Função para fechar o pop-up
function closePopup() {
    document.getElementById('times-popup').style.display = 'none';
}