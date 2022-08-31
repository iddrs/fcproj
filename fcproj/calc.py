""" Rotinas para cálculos.
"""
import numpy as np
import pandas as pd


def saldo_atual(balver):
    df = balver[(balver.conta_contabil.str.startswith('1'))
                & (balver.indicador_superavit_financeiro.isin(['F', 'f']))]
    df['saldo_atual'] = round(df['saldo_atual_debito'] - df['saldo_atual_credito'], 2)
    df = df[['recurso_vinculado', 'saldo_atual']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def a_arrecadar(balrec, receita, month):
    balrec['balrec'] = np.where(balrec.receita_realizada > balrec.previsao_atualizada, balrec.receita_realizada,
                                balrec.previsao_atualizada)
    receita['meta_1'] = round(receita.meta_1bim / 2, 2)
    receita['meta_2'] = round(receita.meta_1bim / 2, 2)
    receita['meta_3'] = round(receita.meta_2bim / 2, 2)
    receita['meta_4'] = round(receita.meta_2bim / 2, 2)
    receita['meta_5'] = round(receita.meta_3bim / 2, 2)
    receita['meta_6'] = round(receita.meta_3bim / 2, 2)
    receita['meta_7'] = round(receita.meta_4bim / 2, 2)
    receita['meta_8'] = round(receita.meta_4bim / 2, 2)
    receita['meta_9'] = round(receita.meta_5bim / 2, 2)
    receita['meta_10'] = round(receita.meta_5bim / 2, 2)
    receita['meta_11'] = round(receita.meta_6bim / 2, 2)
    receita['meta_12'] = round(receita.meta_6bim / 2, 2)
    receita['receita'] = 0.0
    for i in range(1, month, 1):
        receita['receita'] += round(receita[f'meta_{i}'], 2)
    receita = receita[['recurso_vinculado', 'receita']]
    receita = receita.groupby('recurso_vinculado').sum()
    balrec = balrec[['recurso_vinculado', 'balrec']]
    balrec = balrec.groupby('recurso_vinculado').sum()
    df = pd.merge(balrec, receita, on='recurso_vinculado', how='left')
    df['a_arrecadar'] = np.where(df.balrec > df.receita, df.balrec, df.receita)
    df = df.drop(['balrec', 'receita'], axis='columns')
    return df


def a_empenhar(baldesp):
    baldesp['a_empenhar'] = round(baldesp.dotacao_atualizada - baldesp.valor_empenhado, 2)
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
    df['extra_a_pagar'] = round(df.saldo_atual_credito - df.saldo_atual_debito, 2)
    df = df[['recurso_vinculado', 'extra_a_pagar']]
    df = df.groupby('recurso_vinculado').sum()
    return df


def saldo_final(data):
    data['saldo_final'] = round(
        data.saldo_atual + data.a_arrecadar - data.a_empenhar - data.a_pagar - data.saldo_rp - data.extra_a_pagar, 2)
    return data
