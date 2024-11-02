const jsonUrl = 'dados/dados.json'; // URL do arquivo JSON
let rodadas = [];
let indiceRodadaAtual = 0;

// Função para carregar dados do JSON
async function carregarDados() {
    try {
        const resposta = await fetch(jsonUrl);
        if (!resposta.ok) throw new Error('Erro ao carregar os dados.');

        const dados = await resposta.json();

        // Verifica se a estrutura do JSON é válida
        if (!dados.rodadas || !Array.isArray(dados.rodadas)) {
            throw new Error('Estrutura de dados inválida.');
        }

        rodadas = dados.rodadas;
        console.log('Rodadas carregadas:', rodadas); // Log das rodadas carregadas
        atualizarTabelaGeral();
        atualizarTabelaRodadas();
    } catch (error) {
        document.getElementById('mensagemErro').innerText = error.message;
    }
}

// Função para calcular pontos por posição
function calcularPontosPorPosicao(posicao) {
    switch (posicao) {
        case 1: return 10;
        case 2: return 8;
        case 3: return 6;
        case 4: return 4;
        case 5: return 2;
        default: return 0;
    }
}

// Função para atualizar a tabela geral
function atualizarTabelaGeral() {
    const tabelaGeral = document.getElementById('tabelaGeral').getElementsByTagName('tbody')[0];
    tabelaGeral.innerHTML = ''; // Limpa a tabela

    const pontuacoes = {};

    // Calcula pontuações
    rodadas.forEach(rodada => {
        if (!rodada.ranking) return; // Ignora se não houver ranking

        rodada.ranking.forEach(item => {
            if (!pontuacoes[item.dupla]) {
                pontuacoes[item.dupla] = { kills: 0, posicoes: [], jogos: 0 };
            }
            pontuacoes[item.dupla].kills += item.kills;
            pontuacoes[item.dupla].posicoes.push(item.posicao); // Armazena a posição da rodada
            pontuacoes[item.dupla].jogos++;
        });
    });

    console.log('Pontuações calculadas:', pontuacoes); // Log das pontuações

    // Adiciona dados na tabela
    Object.keys(pontuacoes).forEach((dupla, index) => {
        const { kills, posicoes, jogos } = pontuacoes[dupla];
        
        // Calcula os pontos totais
        const pontosTotais = kills + posicoes.reduce((total, pos) => total + calcularPontosPorPosicao(pos), 0);

        const novaLinha = tabelaGeral.insertRow();
        novaLinha.insertCell(0).innerText = index + 1;
        novaLinha.insertCell(1).innerText = dupla;
        novaLinha.insertCell(2).innerText = jogos;
        novaLinha.insertCell(3).innerText = kills;
        novaLinha.insertCell(4).innerText = pontosTotais;

        // Destaca se estiver entre os 3 primeiros
        if (index < 3) {
            novaLinha.classList.add('highlight');
        }
    });
}

// Função para atualizar a tabela de rodadas
function atualizarTabelaRodadas() {
    const tabelaRodadas = document.getElementById('tabelaRodadas').getElementsByTagName('tbody')[0];
    tabelaRodadas.innerHTML = ''; // Limpa a tabela
    const rodadaAtual = rodadas[indiceRodadaAtual];

    // Atualiza título da rodada
    if (rodadaAtual) {
        document.getElementById('tituloRodada').innerText = `${rodadaAtual.nome} - ${rodadaAtual.mapa}`;

        rodadaAtual.ranking.forEach(item => {
            const novaLinha = tabelaRodadas.insertRow();
            novaLinha.insertCell(0).innerText = item.posicao;
            novaLinha.insertCell(1).innerText = item.dupla;
            novaLinha.insertCell(2).innerText = item.kills;

            // Cálculo de pontos
            const pontos = item.kills + calcularPontosPorPosicao(item.posicao);
            novaLinha.insertCell(3).innerText = pontos;
        });
    } else {
        document.getElementById('tituloRodada').innerText = "Rodada não encontrada";
    }
}

// Função para navegar entre as rodadas
function navegarRodadas(direcao) {
    indiceRodadaAtual += direcao;
    indiceRodadaAtual = Math.max(0, Math.min(indiceRodadaAtual, rodadas.length - 1)); // Limita o índice
    atualizarTabelaRodadas();
}

// Carrega dados na inicialização
carregarDados();
