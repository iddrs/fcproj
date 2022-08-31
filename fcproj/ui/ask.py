""" Rotinas de entrada de usuário.
"""

def month():
    while True:
        entry = int(input('Digite o mês desejado (entre 1 e 12): '))
        if (entry >= 1) and (entry <= 12):
            return str(entry).zfill(2)
        print('Mês inválido. Preste mais atenção!')


def year():
    return input('Digite o ano (com 4 algarismos): ')