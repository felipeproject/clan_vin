// navigation.js
// Funções de navegação entre páginas

document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".nav-link");

    const disableLinks = () => {
        links.forEach(link => link.classList.add("disabled"));
    };

    const enableLinks = () => {
        links.forEach(link => link.classList.remove("disabled"));
    };

    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const page = link.getAttribute("data-page");

            if (page) {
                disableLinks(); // Desabilita links
                fetch(page)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Erro ao carregar a página: " + response.statusText);
                        }
                        return response.text();
                    })
                    .then(html => {
                        document.getElementById("conteudo").innerHTML = html;
                        enableLinks(); // Habilita links após o carregamento
                        window.history.pushState({ html }, '', page); // Atualiza o histórico
                    })
                    .catch(error => {
                        console.error("Erro ao carregar a página:", error);
                        enableLinks(); // Habilita links mesmo em erro
                    });
            }
        });
    });

    // Manipulação do evento popstate
    window.addEventListener('popstate', function(event) {
        if (event.state) {
            document.getElementById("conteudo").innerHTML = event.state.html; // Atualiza o conteúdo
        } else {
            // Carregar conteúdo padrão ou inicial se necessário
            document.getElementById("conteudo").innerHTML = '<p>Conteúdo inicial aqui.</p>';
        }
    });
});
