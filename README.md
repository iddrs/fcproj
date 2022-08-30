# fcproj
**Fluxo de Caixa Projetado**

---

ESte programa gera um relatório com o fluxo de caixa projetado por fonte de 
recursos (recurso vinculado) para entidades públicas.

## Metodologia de cálculo

```
Saldo de Caixa Projetado = 
Saldo de caixa atual
+ Receita a arrecadar
- Dotação a empenhar
- Empenhado a pagar
- Saldo e Restos a Pagar
- Despesa Extra-Orçamentária a recolher
+ Valores a compensar
```

Onde:

```
Receita a Arrecadar = o maior valor entre
(Previsão Atualizada da Receita
- Valor arrecadado)
or
[(Valor Arrecadado
 + Valor a arrecadar da programação financeira)
- Valor arrecadado]
```

## Requerimentos

Vide `requeriments.txt`.

O programa trabalha com os arquivos `csv` gerados por [PAD-Converter](https://github.com/iddrs/pad-converter).

## Autor

[Everton da Rosa](https://everton3x.github.io)
