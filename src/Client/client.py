import socket
import sys

def main():
    print('Cliente rodando no Host 127.0.0.1 | Porta 6000')

    s = socket.socket()
    s.connect(('127.0.0.1', 6000))

    print("----------------------------")
    print("Bem-vindo ao jogo da forca!")
    print("----------------------------")
    print("Dois jogadores? (s/n)")
    print(">>", end='')
    
    msg = input().lower()

    while 1:
        if msg == 's' or msg == 'n':
            break
        msg = input('Por favor digite s (Sim) ou n (Não)')

    if msg == 's':
        doisJogadoresSinal = '2'.encode('utf-8')
        s.send(doisJogadoresSinal)

        jogarGame(s)
    else:
        doisJogadoresSinal = '0'.encode('utf-8')
        s.send(doisJogadoresSinal)

        print("Jogo iniciado! Tema: Animais")
        jogarGame(s)

def recv_helper(socket):
    first_byte_value = int(socket.recv(1)[0])

    if first_byte_value == 0:
        x, y = socket.recv(2)
        return 0, socket.recv(int(x)), socket.recv(int(y))
    else:
        return 1, socket.recv(first_byte_value)

def jogarGame(s):
    while True:
        pkt = recv_helper(s)
        msgFlag = pkt[0]
        if msgFlag != 0:
            msg = pkt[1].decode('utf8')
            print(msg)
            if msg == 'Servidor sobrecarregado' or 'Fim de jogo!' in msg:
                break
        else:
            gameString = pkt[1].decode('utf8')
            digitadasIncorretas = pkt[2].decode('utf8')

            print(" ".join(list(gameString)))
            print("Letras incorretas: " + " ".join(digitadasIncorretas) + "\n")

            if "_" not in gameString or len(digitadasIncorretas) >= 6:
                continue
            else:
                letraDigitada = ''
                valid = False
                while not valid:
                    letraDigitada = input('Digite uma letra: ').lower()
                    if letraDigitada in digitadasIncorretas or letraDigitada in gameString:
                        print("Error! Letra " + letraDigitada.upper() + " já foi digitada anteriormente, por favor digite outra letra.")
                    elif len(letraDigitada) > 1 or not letraDigitada.isalpha():
                        print("Error! Por favor digite apenas uma letra")
                    else:
                        valid = True
                msg = bytes([len(letraDigitada)]) + bytes(letraDigitada, 'utf8')
                s.send(msg)

    s.shutdown(socket.SHUT_RDWR)
    s.close()

main()
