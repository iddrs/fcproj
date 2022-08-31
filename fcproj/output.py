""" Rotinas de saída de dados.
"""

from fcproj.utils import currency

def latex(data, destination):
    # Processa as colunas numéricas porque tá osso conseguir formatar os números para o padrão pt-br com latex
    df = data.copy()
    df['saldo_atual'] = df['saldo_atual'].map(currency)
    df['a_arrecadar'] = df['a_arrecadar'].map(currency)
    df['a_empenhar'] = df['a_empenhar'].map(currency)
    df['a_pagar'] = df['a_pagar'].map(currency)
    df['saldo_rp'] = df['saldo_rp'].map(currency)
    df['extra_a_pagar'] = df['extra_a_pagar'].map(currency)
    df['saldo_final'] = df['saldo_final'].map(currency)

    df['recurso_vinculado'] = df['recurso_vinculado'].astype(str)
    df['recurso_vinculado'] = df['recurso_vinculado'].str.zfill(4)

    tex = df.to_latex(header=['Código', 'Fonte de Recursos', 'Saldo financeiro', 'A Arrecadar', 'A Empenhar',
                                'Empenhado a Pagar', 'Saldo de RP', 'Saldo Extra', 'Saldo Final'],
                        index=False, float_format='%.2f',
                        column_format='>{\\raggedleft}p{1cm}>{\\raggedright}p{5cm}>{\\raggedleft}p{2.5cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{3cm}>{\\raggedleft}p{2cm}>{\\raggedleft}p{2cm}>{\\raggedleft\\arraybackslash}p{2cm}',
                        longtable=True, decimal=',',
                        caption='Fluxo de Caixa Projetado por Fonte de Recurso', position='H')
    with open(destination, 'w', encoding='utf-8') as f:
        return f.write(tex)
