// Função para mostrar o modal com os detalhes do evento
function showEventDetails(eventDescription) {
    document.getElementById('event-description').innerText = eventDescription;
    document.getElementById('event-modal').style.display = 'block';
}

// Função para fechar o modal
function closeModal() {
    document.getElementById('event-modal').style.display = 'none';
}

// Fecha o modal ao clicar fora da área do conteúdo do modal
window.onclick = function(event) {
    const modal = document.getElementById('event-modal');
    if (event.target === modal) {
        closeModal();
    }
}
