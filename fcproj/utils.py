"""Utilitários
"""
from os import environ

def currency(num):
    return f'{num:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def check_venv():
    """Verifica se o script está rodando num ambiente virtual
    """
    if 'VIRTUAL_ENV' in environ:
        return True
    else:
        return False