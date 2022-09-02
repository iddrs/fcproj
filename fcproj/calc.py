""" Rotinas para cálculos.
"""

import pandas as pd


def saldo_atual(balver):
    df = balver[(balver.conta_contabil.str.startswith('1'))
                & (balver.indicador_superavit_financeiro.isin(['F', 'f']))]
    df = df.copy()
    df['saldo_atual'] = round(df['saldo_atual_debito'] - df['saldo_atual_credito'], 2)
    df = df[['recurso_vinculado', 'saldo_atual']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def a_empenhar(baldesp):
    baldesp['a_empenhar'] = round(baldesp.dotacao_atualizada - baldesp.valor_empenhado, 2)
    baldesp = baldesp[baldesp['funcao'] != 99]
    df = baldesp[['recurso_vinculado', 'a_empenhar']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def a_pagar(baldesp):
    baldesp['a_pagar'] = round(baldesp.valor_empenhado - baldesp.valor_pago, 2)
    df = baldesp[['recurso_vinculado', 'a_pagar']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def saldo_rp(rp):
    rp['saldo_rp'] = round(rp.saldo_final_nao_processados + rp.saldo_final_processados, 2)
    df = rp[['recurso_vinculado', 'saldo_rp']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def extra_a_pagar(balver):
    df = balver[(balver.indicador_superavit_financeiro.isin(['F', 'f']))
                & ((balver.conta_contabil.str.startswith('2.1.8.8.'))
                   | (balver.conta_contabil.str.startswith('1.1.3.2.3.')))]
    df = df.copy()
    df['extra_a_pagar'] = round(df.saldo_atual_credito - df.saldo_atual_debito, 2)
    df = df[['recurso_vinculado', 'extra_a_pagar']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def saldo_final(data):
    data['saldo_final'] = round(
        data.saldo_atual + data.a_arrecadar - data.a_empenhar - data.a_pagar - data.saldo_rp - data.extra_a_pagar, 2)
    return data


def total(data):
    total = data.copy()
    total['total'] = 'Total'
    total = total[
        ['total', 'saldo_atual', 'a_arrecadar', 'a_empenhar', 'a_pagar', 'saldo_rp', 'extra_a_pagar',
         'saldo_final']].groupby('total').sum()
    total['recurso_vinculado'] = 9999
    total['nome'] = 'Total'
    total = total.reset_index(level=0)
    total = total.drop('total', axis='columns')
    data = pd.concat([data, total])
    return data


def deficit_vinculados(data):
    vinculados = data[(data['recurso_vinculado'] > 0) & (data['recurso_vinculado'] != 50) & (data['saldo_final'] < 0)]
    resultado = round(vinculados['saldo_final'].sum(), 2)
    if resultado < 0:
        return resultado
    else:
        return 0.0


def resultado_proprio(data, deficit_vinculados):
    proprio = data[data['recurso_vinculado'] == 0]
    resultado = round(proprio['saldo_final'].sum(), 2)
    return (resultado + deficit_vinculados)


def a_arrecadar(balrec, receita, month):
    # pega receita realizada e previsão atualizada
    df1 = balrec[['recurso_vinculado', 'receita_realizada', 'previsao_atualizada']]
    df1 = df1[df1['recurso_vinculado'] > 0]
    df1 = df1.groupby('recurso_vinculado').sum()

    # Calcula reestimativa a partir do arrecadado + meta futura

    df2 = receita.copy()
    df2 = df2[df2['recurso_vinculado'] > 0]
    df2['meta_1'] = round(df2['meta_1bim'] / 2, 2)
    df2['meta_2'] = round(df2['meta_1bim'] / 2, 2)
    df2['meta_3'] = round(df2['meta_2bim'] / 2, 2)
    df2['meta_4'] = round(df2['meta_2bim'] / 2, 2)
    df2['meta_5'] = round(df2['meta_3bim'] / 2, 2)
    df2['meta_6'] = round(df2['meta_3bim'] / 2, 2)
    df2['meta_7'] = round(df2['meta_4bim'] / 2, 2)
    df2['meta_8'] = round(df2['meta_4bim'] / 2, 2)
    df2['meta_9'] = round(df2['meta_5bim'] / 2, 2)
    df2['meta_10'] = round(df2['meta_5bim'] / 2, 2)
    df2['meta_11'] = round(df2['meta_6bim'] / 2, 2)
    df2['meta_12'] = round(df2['meta_6bim'] / 2, 2)
    df2['reestimativa'] = 0.0
    for i in range(month + 1, 13, 1):
        df2['reestimativa'] += round(df2[f'meta_{i}'], 2)
    df2 = df2[['recurso_vinculado', 'reestimativa']]
    df2 = df2.groupby('recurso_vinculado').sum()

    # Mescla os df1 e df2
    df3 = pd.merge(df1, df2, on='recurso_vinculado', how='left')

    # Completa cálculo da reestimativa
    df3['reestimativa'] = round(df3['reestimativa'] + df3['receita_realizada'], 2)

    # Define o maior valore entre o arrecadado, a previsão atualizada e a reestimativa
    df3['a_arrecadar'] = 0.0
    df3['a_arrecadar'] = df3[['previsao_atualizada', 'receita_realizada', 'reestimativa']].max(axis=1, skipna=True,
                                                                                               numeric_only=True)

    # Define o valor a arrecadar final
    df3['a_arrecadar'] = round(df3['a_arrecadar'] - df3['receita_realizada'], 2)
    df3 = df3.reset_index(level=0)
    df = df3[['recurso_vinculado', 'a_arrecadar']]
    return df
