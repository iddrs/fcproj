"""Utilitários
"""

def currency(num):
    return f'{num:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
