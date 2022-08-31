import pandas as pd

def join(left, right):
    df = pd.merge(left, right, on='recurso_vinculado', how='left')
    return df

def purge(data):
    data['purge'] = round(data.saldo_atual + data.a_arrecadar + data.a_empenhar + data.a_pagar + data.saldo_rp + data.extra_a_pagar, 2)
    data = data.drop(data[data.purge == 0.0].index)
    data = data.drop('purge', axis='columns')
    return data
