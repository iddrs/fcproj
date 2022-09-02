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

    tex = df.to_latex(columns=['recurso_vinculado', 'saldo_atual', 'a_arrecadar', 'a_empenhar', 'a_pagar', 'saldo_rp', 'extra_a_pagar', 'saldo_final'], header=['Código', 'Saldo financeiro', 'A Arrecadar', 'A Empenhar',
                                'Empenhado a Pagar', 'Saldo de RP', 'Saldo Extra', 'Saldo Final'],
                        index=False, float_format='%.2f',
                        column_format='lrrrrrrr',
                        longtable=True, decimal=',',
                        caption='Fluxo de Caixa Projetado por Fonte de Recurso', position='H')
    with open(destination, 'w', encoding='utf-8') as f:
        return f.write(tex)

def latex_vinculos(data, destination):
    df = data.copy()
    df['recurso_vinculado'] = df['recurso_vinculado'].astype(str)
    df['recurso_vinculado'] = df['recurso_vinculado'].str.zfill(4)

    tex = df.to_latex(columns=['recurso_vinculado', 'nome'], header=['Código', 'Fonte de recurso'],
                        index=False,
                        column_format='ll',
                        longtable=True,
                        caption='Fontes de recursos', position='H')
    with open(destination, 'w', encoding='utf-8') as f:
        return f.write(tex)