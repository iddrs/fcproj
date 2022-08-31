import pandas as pd


def join(left, right):
    df = pd.merge(left, right, on='recurso_vinculado', how='left')
    return df


def purge(data):
    data['purge'] = round(
        data.saldo_atual + data.a_arrecadar + data.a_empenhar + data.a_pagar + data.saldo_rp + data.extra_a_pagar, 2)
    data = data.drop(data[data.purge == 0.0].index)
    data = data.drop('purge', axis='columns')
    return data


def agrupa_recurso_proprio(data):
    vinculos = (1, 20, 40)
    recurso_proprio = data[(data['recurso_vinculado'] == 1)
                           | (data['recurso_vinculado'] == 20)
                           | (data['recurso_vinculado'] == 40)]
    recurso_proprio['group'] = 0
    recurso_proprio = recurso_proprio[
        ['group', 'saldo_atual', 'a_arrecadar', 'a_empenhar', 'a_pagar', 'saldo_rp', 'extra_a_pagar', 'saldo_final']].groupby('group').sum()
    recurso_proprio['recurso_vinculado'] = 0
    recurso_proprio['nome'] = 'RECURSO PRÓPRIO'
    recurso_proprio = recurso_proprio.reset_index(level=0)
    recurso_proprio = recurso_proprio.drop('group', axis='columns')
    data = data.drop(data[(data['recurso_vinculado'] == 1) | (data['recurso_vinculado'] == 20) | (
    data['recurso_vinculado'] == 40)].index)
    data = pd.concat([data, recurso_proprio])
    data = data.sort_values('recurso_vinculado')
    return data

