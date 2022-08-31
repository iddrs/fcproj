"""Calcula o fluxo de caixa projetado para órgãos públicos.

O fluxo de caixa projetado é calculado a partir das informações contábeis e orçamentárias e é feito por fonte de
recursos.
"""
import sys
import fcproj.calc
import fcproj.output
import fcproj.data.load
import fcproj.ui.ask
import os
import configparser
import logging
import datetime
import locale
from fcproj.utils import currency

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')


def main():
    welcome = '''
    ======================================================================
    Bem-vindo ao FCPROJ.
    Programa calculador de fluxo de caixa projetado por fonte de recursos.
    ======================================================================
    '''
    print(welcome)
    # Carrega configurações
    config = configparser.ConfigParser()
    config.read('config.ini')
    print('Configurações carregadas')

    # Configura o logger
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('fcproj')
    logger.info('Logger pronto')

    # Usuário entra com o ano e o mês
    month = fcproj.ui.ask.month()
    year = fcproj.ui.ask.year()
    logger.info(f'O período escolhido foi {month}/{year}')

    # Define o caminho base dos arquivos de dados
    base_dir = os.path.join(config['SOURCE']['base_dir'], f"{year}-{month}")
    logger.info(f'A base de dados está em {base_dir}')

    # Carrega a lista de vínculos e anexa
    data = fcproj.data.load.vinculos(os.path.join(base_dir, config['SOURCE']['fvinculos']))
    logger.info(f'Foram encontrados {len(data)} fontes de recurso.')

    # Calcula o saldo de caixa atual e anexa
    balver = fcproj.data.load.balver(os.path.join(base_dir, config['SOURCE']['fbalver']))
    data = fcproj.data.join(data, fcproj.calc.saldo_atual(balver))
    logger.info(f'Foram processados {len(data)} saldos atuais para fontes de recurso.')

    # Calcula a receita a arrecadar
    balrec = fcproj.data.load.balrec(os.path.join(base_dir, config['SOURCE']['fbalrec']))
    receita = fcproj.data.load.receita(os.path.join(base_dir, config['SOURCE']['freceita']))
    data = fcproj.data.join(data, fcproj.calc.a_arrecadar(balrec, receita, int(month)))
    logger.info(f'Foram processados {len(data)} valores a arrecadar para fontes de recurso.')

    # Calcula a dotação a empenhar e anexa
    baldesp = fcproj.data.load.baldesp(os.path.join(base_dir, config['SOURCE']['fbaldesp']))
    data = fcproj.data.join(data, fcproj.calc.a_empenhar(baldesp))
    logger.info(f'Foram processados {len(data)} valores a empenhar para fontes de recurso.')

    # Calcula o empenhado a pagar e anexa
    data = fcproj.data.join(data, fcproj.calc.a_pagar(baldesp))
    logger.info(f'Foram processados {len(data)} valores a pagar para fontes de recurso.')

    # Calcula o saldo de restos a pagar e anexa
    rp = fcproj.data.load.rp(os.path.join(base_dir, config['SOURCE']['frp']))
    data = fcproj.data.join(data, fcproj.calc.saldo_rp(rp))
    logger.info(f'Foram processados {len(data)} saldos de restos a pagar para fontes de recurso.')

    # Calcula a despesa extra a recolher e anexa
    data = fcproj.data.join(data, fcproj.calc.extra_a_pagar(balver))
    logger.info(f'Foram processados {len(data)} saldos extra-orçamentários a pagar para fontes de recurso.')

    # Converte NaN para 0
    data.fillna(0.0, inplace=True)

    # Calcula o saldo final projetado e anexa
    data = fcproj.calc.saldo_final(data)
    logger.info(f'Foram processados {len(data)} saldos finais projetados para fontes de recurso.')

    # Remove linhas sem valores
    data = fcproj.data.purge(data)
    logger.info(f'Restaram {len(data)} fontes de recurso com valores.')

    # Agrupa algumas fontes em recurso próprio
    data = fcproj.data.agrupa_recurso_proprio(data)
    logger.info(f'Restaram {len(data)} fontes de recurso após agrupamento do recurso próprio.')

    # Calcula outros valores
    deficit_vinculados = fcproj.calc.deficit_vinculados(data)
    logger.info(f'Os recursos vinculados apresentam déficit {deficit_vinculados}')
    resultado_proprio = fcproj.calc.resultado_proprio(data, deficit_vinculados)
    logger.info(f'Os recursos próprios apresentam resultado {resultado_proprio}')

    # Calcula o total
    data = fcproj.calc.total(data)
    logger.info('Linha com totais adicionada.')

    # Salva o relatório
    destination = os.path.join(config['OUTPUT']['cache'], config['OUTPUT']['flatex'])
    char_writed = fcproj.output.latex(data, destination)
    logger.info(f'Foram escritos {char_writed} caracteres para {destination}')


    # Gerando dados auxiliares
    logger.info('Gerando arquivos auxiliares')
    with open(os.path.join(config['OUTPUT']['cache'], 'date.tex'), 'w', encoding='utf-8') as f:
        dt = datetime.datetime(2022, 7, 1)
        f.write('\\date{%s}' % (dt.strftime('%B de %Y')))
        f.write('\\newcommand{\\thedate}{%s}' % (dt.strftime('%B de %Y')))
        f.write('\\newcommand{\\deficitVinculado}{%s}' % (currency(deficit_vinculados)))
        f.write('\\newcommand{\\resultadoProprio}{%s}' % (currency(resultado_proprio)))
    with open(os.path.join(config['OUTPUT']['cache'], 'arquivo.txt'), 'w', encoding='utf-8') as f:
        f.write('fcproj_report_%s.pdf' % (dt.strftime('%Y-%m')))

if __name__ == '__main__':
    main()
