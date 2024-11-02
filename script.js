// script.js
document.addEventListener("DOMContentLoaded", function() {
    // Carregar a página inicial por padrão
    loadPage('home.html');

    // Adicionar eventos de clique aos links
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const page = this.getAttribute('data-page') || 'home.html';
            loadPage(page);
        });
    });
});

function loadPage(page) {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = '<p>Carregando...</p>'; // Mensagem de carregamento
    fetch(page)
        .then(response => {
            if (!response.ok) throw new Error('Erro ao carregar a página.');
            return response.text();
        })
        .then(html => {
            conteudo.innerHTML = html;
            window.history.pushState({ page }, '', page); // Atualiza o histórico
        })
        .catch(error => {
            conteudo.innerHTML = `<p>${error.message}</p>`;
        });
}

// Manipulação do histórico
window.addEventListener('popstate', function(event) {
    if (event.state) {
        loadPage(event.state.page);
    } else {
        loadPage('home.html'); // Carrega a página inicial se não houver estado
    }
});
