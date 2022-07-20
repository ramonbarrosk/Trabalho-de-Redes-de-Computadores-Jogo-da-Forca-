import socket
from _thread import *
import sys
import random

numeroCliente = 0  
palavras = ['macaco', 'gato', 'cachorro', 'girafa']
games = []

class Game:
    palavra = ""
    palavraString = ""
    digitadasIncorretas = 0
    letrasIncorretas = 0
    vez = 1
    lock = 0
    completo = False

    def __init__(self, palavra, quantidade_jogadores):
        self.letrasIncorretas = []
        self.lock = allocate_lock()
        self.palavra = palavra
        for i in range(len(palavra)):
            self.palavraString += "_"
        if quantidade_jogadores == 1:
            self.completo = True

    def getStatus(self):
        if self.digitadasIncorretas >= 6:
            return 'Você perdeu!'
        elif not '_' in self.palavraString:
            return 'Você ganhou!'
        else:
            return ''

    def guess(self, letra):
        if letra not in self.palavra or letra in self.palavraString:
            self.digitadasIncorretas += 1
            self.letrasIncorretas.append(letra)
            return 'Incorreta!'
        else:
            palavraString = list(self.palavraString)
            for i in range(len(self.palavra)):
                if self.palavra[i] == letra:
                    palavraString[i] = letra
            self.palavraString = ''.join(palavraString)
            return 'Correta!'

    def mudarVez(self):
        if self.vez == 1:
            self.vez = 2
        else:
            self.vez = 1


def main():
    global numeroCliente
    global palavras

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print('Servidor rodando no Host 127.0.0.1 | Porta 6000')

    try:
        s.bind(('127.0.0.1', 6000))  
    except socket.error as e:
        print(str(e))
    s.listen()  

    while True:
        c, addr = s.accept()
        numeroCliente += 1
        print("Conexão " + str(numeroCliente) + " estabelecida a partir do: " + str(addr))
        start_new_thread(clienteThread, (c,))

def getGame(quantidade_jogadores):
    if quantidade_jogadores == 2:
        for game in games:
            if not game.completo:
                game.completo = True
                return (game, 2)
    if len(games) < 3:
        palavra = palavras[random.randint(0, 3)]
        game = Game(palavra, quantidade_jogadores)
        games.append(game)
        return (game, 1)
    else:
        return -1

def clienteThread(c):
    global numeroCliente

    doisJogadoresSinal = c.recv(1024).decode('utf-8')

    if doisJogadoresSinal == '2':
        x = getGame(2)
        if x == -1:
            send(c, 'Servidor sobrecarregado')
        else:
            game, jogador = x
            send(c, 'Aguardando outro jogador!')

            while not game.completo:
                continue
            send(c, 'Jogo iniciado!')
            doisJogadoresGame(c, jogador, game)

    else:
        x = getGame(1)
        if x == -1:
            send(c, 'Servidor sobrecarregado')
        else:
            game, jogador = x
            umJogadorGame(c, game)

def send(c, msg):
    packet = bytes([len(msg)]) + bytes(msg, 'utf8')
    c.send(packet)

def send_game_control_packet(c, game):
    msgFlag = bytes([0])
    data = bytes(game.palavraString + ''.join(game.letrasIncorretas), 'utf8')
    gamePacket = msgFlag + bytes([len(game.palavra)]) + bytes([game.digitadasIncorretas]) + data
    c.send(gamePacket)

def doisJogadoresGame(c, jogador, game):
    global numeroCliente                                                 

    while True:
        while game.vez != jogador:
            continue
        game.lock.acquire()

        status = game.getStatus()
        if status != '':
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "Fim de jogo!")
            game.mudarVez()
            game.lock.release()
            break

        send(c, 'Sua vez!')

        send_game_control_packet(c, game)

        rcvd = c.recv(1024)
        letraDigitada = bytes([rcvd[1]]).decode('utf-8')

        send(c, game.guess(letraDigitada))

        status = game.getStatus()
        if len(status) > 0:
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "Fim de jogo!")
            game.mudarVez()
            game.lock.release()
            break

        send(c, "Aguardando outro jogador...")
        game.mudarVez()
        game.lock.release()

    if game in games:
        games.remove(game)
    c.close()
    numeroCliente -= 1


def umJogadorGame(c, game):
    global numeroCliente

    while True:
        send_game_control_packet(c, game)

        rcvd = c.recv(1024)
        letraDigitada = bytes([rcvd[1]]).decode('utf-8')

        send(c, game.guess(letraDigitada))

        status = game.getStatus()
        if len(status) > 0:
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "Fim de jogo!")
            break
    games.remove(game)
    c.close()
    numeroCliente -= 1

main()
