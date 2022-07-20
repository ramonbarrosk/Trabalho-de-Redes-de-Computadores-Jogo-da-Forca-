
# Projeto de Redes de Computadores utilizando socket

## Dupla do projeto:

- **Ramon Barros de Lima**
- **Saulo Roberto dos Santos**
----
## Jogo da Forca

O projeto consiste em um jogo da forca que pode ser jogado por um ou dois jogadores conectados no mesmo servidor.

Como é do conhecimento de todos, vai ser escolhida aleatoriamente uma palavra de uma lista que definimos como tema sobre ANIMAIS. Após se conectar com o servidor o cliente vai escolher a opção se vai jogar de um ou dois jogadores.

Caso seja escolhido a opção de dois jogadores, o servidor vai aguardar outro cliente se conectar através de um novo terminal, assim após se conectar, é possível prosseguir com o jogo.

Durante o jogo um jogador ou os dois juntos vão ter um total de 6 tentativas.


---

## Requisitos

Para ser possível jogar, o usuário vai ter que ter instalado em sua máquina o python na sua versão 3.6 ou superior.

---
## Como jogar

Primeiramente vamos ter que rodar o servidor, executando o seguinte comando dentro da raiz do projeto.

```bash
$ python src/Server/server.py
```

Após rodar o servidor, vamos abrir um novo terminal para rodar o cliente para ser possível se conectar com o servidor e começar o jogo.

Execute o seguinte comando na raiz do projeto:

```bash
$ python src/Client/client.py
```

Inicialmente vai aparecer uma pergunta se vai querer jogar com um ou dois jogadores. Caso escolha a opção de dois jogadores, é necessário abrir um novo terminal e rodar o comando acima novamente,  e responder a pergunta com SIM mais uma vez.

---

## Sobre o desenvolvimento

- Projeto desenvolvido utilizando a linguagem Python
- Foi utilizada as bibliotecas  <code>__thread_</code> e <code>socket</code>

---

Obrigado pela atenção e bom jogo.