""" Rotinas para carregar dados.
"""
import pandas as pd


def vinculos(file):
    df = pd.read_csv(file, sep=";", usecols=['recurso_vinculado', 'nome'],
                     dtype={'recurso_vinculado': int, 'nome': str})
    df = df.drop_duplicates()
    return df


def balver(file):
    df = pd.read_csv(file, sep=";",
                     usecols=['conta_contabil', 'saldo_atual_debito', 'saldo_atual_credito', 'escrituracao',
                              'indicador_superavit_financeiro', 'recurso_vinculado'],
                     dtype={'conta_contabil': str, 'saldo_atual_debito': float, 'saldo_atual_credito': float,
                            'escrituracao': str, 'indicador_superavit_financeiro': str, 'recurso_vinculado': int},
                     thousands='.', decimal=',', encoding_errors='ignore')
    df = df[df.escrituracao.isin(['S', 's'])]
    return df


def balrec(file):
    df = pd.read_csv(file, sep=";",
                     usecols=['receita_realizada', 'previsao_atualizada', 'recurso_vinculado'],
                     dtype={'receita_realizada': float, 'previsao_atualizada': float, 'recurso_vinculado': int},
                     thousands='.', decimal=',', encoding_errors='ignore')
    df = df[df.recurso_vinculado > 0]
    return df


def receita(file):
    df = pd.read_csv(file, sep=";",
                     usecols=['meta_1bim', 'meta_2bim', 'meta_3bim', 'meta_4bim', 'meta_5bim', 'meta_6bim',
                              'recurso_vinculado'],
                     dtype={'meta_1bim': float, 'meta_2bim': float, 'meta_3bim': float, 'meta_4bim': float,
                            'meta_5bim': float, 'meta_6bim': float, 'recurso_vinculado': int},
                     thousands='.', decimal=',', encoding_errors='ignore')
    df = df[df.recurso_vinculado > 0]
    return df


def baldesp(file):
    df = pd.read_csv(file, sep=";",
                     usecols=['funcao', 'recurso_vinculado', 'dotacao_inicial', 'atualizacao_monetaria', 'creditos_suplementares',
                              'creditos_especiais', 'creditos_extraordinarios', 'reducao_dotacao',
                              'suplementacao_recurso_vinculado', 'reducao_recurso_vinculado', 'valor_empenhado',
                              'valor_pago', 'transferencia', 'transposicao', 'remanejamento'],
                     dtype={'funcao': int, 'recurso_vinculado': int, 'dotacao_inicial': float, 'atualizacao_monetaria': float,
                            'creditos_suplementares': float,
                            'creditos_especiais': float, 'creditos_extraordinarios': float, 'reducao_dotacao': float,
                            'suplementacao_recurso_vinculado': float, 'reducao_recurso_vinculado': float,
                            'valor_empenhado': float, 'valor_pago': float,
                            'transferencia': float, 'transposicao': float, 'remanejamento': float},
                     thousands='.', decimal=',', encoding_errors='ignore')
    df['dotacao_atualizada'] = round(df.dotacao_inicial + df.atualizacao_monetaria + df.creditos_suplementares + df.creditos_especiais + df.creditos_extraordinarios - df.reducao_dotacao + df.suplementacao_recurso_vinculado - df.reducao_recurso_vinculado + df.transferencia + df.transposicao + df.remanejamento, 2)
    return df


def rp(file):
    df = pd.read_csv(file, sep=";",
                     usecols=['recurso_vinculado', 'saldo_final_nao_processados', 'saldo_final_processados'],
                     dtype={'recurso_vinculado': int, 'saldo_final_nao_processados': float, 'saldo_final_processados': float},
                     thousands='.', decimal=',', encoding_errors='ignore')
    return df
