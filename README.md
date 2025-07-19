# Artificial Inteligence
Practical Work on Artificial Intelligence
## Descrição do Problema
<p> 
  Após matar o rei de Hyrule, o mago Agahnim está mantendo a princesa Zelda prisioneira e pretende romper o selo que mantem o malvado Ganon aprisionado no Dark World.
</p>
<p>
  Link é o único guerreiro capaz de vencer o mago Agahnim, salvar a princesa Zelda e trazer a paz para o reino de Hyrule. Porém, a única arma forte o suficiente para derrotar o mago Agahnim é a legendaria Master Sword, que encontra-se presa em um pedestal em Lost Woods. 
</p>
<p>
  Para provar que é digno de empunhar a Master Sword, Link deve encontrar e reunir os três Pingentes da Virtude: coragem, poder e sabedoria. 
Os três pingentes encontram-se espalhados pelo reino de Hyrule, dentro de perigosas Masmorras. 
</p>
<p>
  O nosso objetivo é encontrar os três pingentes da virtude e em seguida ir para Lost Woods procurar a legendaria Master Sword.
</p>

## Implementação
<p>
  O Trabalho consiste em implementar um agente capaz de locomover-se autonomamente pelo reino de Hyrule, explorar as perigosas masmorras e reunir os três Pingentes da Virtude. Para isso, você deve utilizar o algoritmo de busca heurística A*.
</p>
<p>
  O agente deve ser capaz de calcular automaticamente a melhor rota para reunir os três pingentes da virtude e ir para Lost Woods, onde está localizada a Master Sword.
</p>

<p>
  O reino de Hyrule é formado por 5 tipos de terrenos: grama, água, montanha, areia e floresta.
</p>

### Os custos para passar por cada tipo de terreno são os seguintes:
<p>
  <ul>
    <li>Grama – Custo: +10</li>
    <li>Areia – Custo: +20</li>
    <li>Floresta – Custo: +100</li>
    <li>Montanha – Custo: +150</li>
    <li>Água – Custo: +180</li>
  </ul>
</p>
<p>
  Os três pingentes da virtude estão localizados dentro de Masmorras, as quais estão identificadas no mapa pelos portões de entrada.
</p>
<p>
  Dentro das Masmorras, somente é possível caminhar pelas regiões mais claras identificadas no mapa. O custo para andar nesse tipo de terreno é de +10. Link inicia sua jornada na posição [25, 28] e termina após reunir os três pingentes da virtude e chegar até a entrada de Lost Woods (posição [7, 6]), onde ele poderá encontrar a Master Sword. A melhor rota para cumprir essa missão é a rota de menor custo levando em consideração o terreno.
</p>

## Informações Adicionais
<p>
  <ul>
    <li>O mapa principal deve ser representado por uma matriz 42 x 42. As Masmorras também devem ser representadas por matrizes de tamanho 28 x 28.</li>
    <li>O agente sempre inicia a jornada na casa do Link (ponto onde está o Link no mapa [25, 28]) e sempre termina a sua jornada ao chegar à entrada de Lost Woods (posição [7, 6]).</li>
    <li>Ao entrar em uma Masmorra, o agente deve encontrar o melhor caminho até o pingente e depois retornar a entrada para sair da Masmorra e retornar para o mapa principal.</li>
    <li>Os pingentes podem ser coletados em qualquer ordem. Porém, ordens diferentes vão resultaram em custos totais diferentes.</li>
    <li>O agente não pode andar na diagonal, somente na vertical e na horizontal.</li>
    <li>Deve existir uma maneira de visualizar os movimentos do agente, mesmo que a interface seja bem simples. Podendo até mesmo ser uma matriz desenhada e atualizada no console.</li>
    <li>Os mapas devem ser configuráveis, ou seja, deve ser possível modificar o tipo de terreno em cada local. O mapa pode ser lido de um arquivo de texto ou deve ser facilmente editável no código.</li>
    <li>O programa deve exibir o custo do caminho percorrido pelo agente enquanto ele se movimenta pelo mapa e também o custo final ao terminar a execução.</li>
    <li>O programa foi ser implementado em qualquer python</li>
  </ul>
</p>

## Como executar o programa
### Passo a passo
1. Clone o repositório em sua maquina
2. Execute o comando
```bash
  pip install matplotlib
```
3. Execute o arquivo `heuristicSearchComplete.py`
