// Definindo o valor da premiação
const valorP = 270.00; // Valor total da premiação

// Formata o valor como moeda brasileira
function formatarMoeda(valor) {
    return `R$ ${valor.toFixed(2).replace('.', ',')}`;
}

// Atualiza o valor total da premiação e o valor por pessoa
function atualizarValor(valorTotal, numeroDePessoas) {
    // Atualiza o valor total da premiação
    document.getElementById('valorArrecadadoWidget').innerText = formatarMoeda(valorTotal);
    
    // Calcula o valor dividido baseado no número de pessoas
    const valorDividido = valorTotal / numeroDePessoas;
    
    // Atualiza o valor por pessoa com formatação
    document.getElementById('valorPorPessoa').innerText = formatarMoeda(valorDividido) + ' para cada um';
}

// Função que anima o valor arrecadado de 0 até o valor desejado
function animarValorArrecadado(valorFinal) {
    const valorElements = document.querySelectorAll('#valorArrecadadoWidget'); // Seleciona o elemento do valor arrecadado
    let valorAtual = 0;
    const incremento = valorFinal / 100; // Define o incremento baseado no valor final para suavizar a animação

    const intervalo = setInterval(() => {
        valorAtual += incremento;
        if (valorAtual >= valorFinal) {
            valorAtual = valorFinal;
            clearInterval(intervalo); // Para a animação quando atingir o valor final
        }

        // Atualiza todos os elementos com o valor formatado
        valorElements.forEach(element => {
            element.innerText = formatarMoeda(valorAtual);
        });
    }, 20); // Velocidade da animação
}

// Inicia a animação ao carregar a página
window.onload = function() {
    const numeroDePessoas = 2; // Ajustado para 2 pessoas
    atualizarValor(valorP, numeroDePessoas); // Atualiza com 2 pessoas
    animarValorArrecadado(valorP);
};

// Função para copiar a chave PIX
function copiarChavePix() {
    const chavePix = document.getElementById('pix-key').innerText; // Obtém a chave PIX
    navigator.clipboard.writeText(chavePix).then(() => {
        // Exibe a mensagem de confirmação
        const copyMessage = document.getElementById('copyMessage');
        copyMessage.style.display = 'block';
        setTimeout(() => {
            copyMessage.style.display = 'none'; // Oculta a mensagem após 2 segundos
        }, 2000);
    }).catch(err => {
        console.error('Erro ao copiar a chave PIX: ', err);
    });
}

// Função para fechar o widget
function fecharWidget() {
    const widget = document.getElementById('widget');
    widget.style.display = 'none'; // Oculta o widget
}
