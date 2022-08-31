""" Rotinas de saída de dados.
"""

from pandas.io.formats.style import Styler


def latex(data, destination):
    tex = data.to_latex(header=['Código', 'Fonte de Recursos', 'Saldo financeiro', 'A Arrecadar', 'A Empenhar',
                                'Empenhado a Pagar', 'Saldo de RP', 'Saldo Extra', 'Saldo Final'],
                        index=False, float_format='%.2f',
                        column_format='>{\\raggedleft}p{1.5cm}>{\\raggedright}p{5cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2.5cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2cm}>{\\raggedleft\\arraybackslash}p{2cm}',
                        longtable=True, decimal=',',
                        caption='Fluxo de Caixa Projetado por Fonte de Recurso', position='H')
    # tex = data.style.to_latex(column_format='rlrrrrrrr', position='H', caption='Fluxo de Caixa Projetado por Fonte de Recurso', environment='tabular')
    with open(destination, 'w', encoding='utf-8') as f:
        return f.write(tex)
