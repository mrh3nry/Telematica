# encoding: utf-8
from random import randint

attack = []
defense = []
tamanho = 12

'''

5 = 1x Porta-aviões
4 = 2x Encouraçados 
3 = 3x Cruzadores 
2 = 4x subimarinos

'''


# range de letra a letra
def crange(c1, c2):
    yield from range(ord(c1), ord(c2) + 1)


# inicia os tabulheiros
def init():
    for c in range(tamanho):
        attack.append([0 for k in range(tamanho)])
        defense.append([0 for k in range(tamanho)])

    for i in range(2, 6):
        preencher(i, 6 - i)


# verifica os arredores das posições dos navios
def verificar(linha, coluna, confirmed):
    global defense

    if linha == tamanho - 1:
        linha_verificar = [linha - 1, linha + 1]
    elif linha == 0:
        linha_verificar = [linha, linha + 2]
    else:  # linha > 0:
        linha_verificar = [linha - 1, linha + 2]

    if coluna == tamanho - 1:
        coluna_verificar = [coluna - 1, coluna + 1]
    elif coluna == 0:
        coluna_verificar = [coluna, coluna + 2]
    else:  # coluna > 0:
        coluna_verificar = [coluna - 1, coluna + 2]

    for li in range(linha_verificar[0], linha_verificar[1]):
        for co in range(coluna_verificar[0], coluna_verificar[1]):
            print('li ', li)
            print('co', co)
            if defense[li][co] != 0:
                confirmed = False
                print('entrou')
    return confirmed


# preencher de forma aleatoria segundo as regras do jogo o tabulheiro de defesa da maquina
def preencher(tipo, quantidade):
    global defense
    c = 0

    while c < quantidade:
        # 0 = horizontal ; 1 = Vertical
        sentido = randint(0, 1)

        if sentido == 0:
            # aleatorizando uma posição
            linha = randint(0, tamanho - 1)
            coluna = randint(0, tamanho - tipo)

            # confirmando se a posição que foi aleatorizada está livre
            confirmed = True
            for i in range(tipo):
                print('linha', linha)
                print('coluna', coluna)
                print('coluna + tipo', coluna + i)
                confirmed = verificar(linha, coluna + i, confirmed)

                if defense[linha][coluna + i] != 0:
                    confirmed = False

            # se for confirmado, preenche
            if confirmed:
                for i in range(tipo):
                    defense[linha][coluna + i] = tipo
                c += 1

                bloco(defense)
                print(confirmed)
                print('------------')

        else:
            linha = randint(0, tamanho - tipo)
            coluna = randint(0, tamanho - 1)

            confirmed = True
            for i in range(tipo):
                print('linha', linha)
                print('coluna', coluna)
                print('linha + tipo', linha + i)
                confirmed = verificar(linha + i, coluna, confirmed)

            if confirmed:
                for i in range(tipo):
                    defense[linha + i][coluna] = tipo
                c += 1

                bloco(defense)
                print(confirmed)
                print('------------')


# print o tabulheiro
def bloco(bloc):
    for c in range(tamanho):
        print(c, ' ', bloc[c])


if __name__ == '__main__':
    init()
    bloco(defense)
