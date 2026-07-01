# Problema 8 — Potenciação Rápida por Quadrados Simultâneos

**Disciplina:** Matemática Discreta — Verificação Formal de Programas
**Professor:** Edjard Mota — Instituto de Computação, UFAM
**Módulo 4:** Problemas Combinados (Indução + Terminação)
# Trabalho de Matemática Discreta — Verificação de Código via Asserções
**Equipe:** Nícolas Torres Ferreira, Robert Marques De Lima, Guilherme Martins Da Silva

---

## 1. Especificação

- **Pré-condição:** `base > 0`, `exp >= 0`
- **Pós-condição:** `p = base ** exp`
- **Invariante de loop:** `res * (base ** exp) == original_base ** original_exp`
- **Função Variante:** `V(state) = exp` (deve decrescer estritamente em direção a 0)

**Data Set:**

| base | exp | resultado esperado |
|------|-----|---------------------|
| 2    | 10  | 1024                |
| 5    | 0   | 1                   |

---

## 2. Código original (buggy)

```python
def fast_exponentiation_broken(base: int, exp: int) -> int:
    assert exp >= 0, "Expoente nao pode ser negativo"
    res = 1
    # Invariante de Loop: res * (base ** exp) == original_base ** original_exp
    while exp > 0:
        if exp % 2 == 1:
            res = res * base
        base = base * base
        exp = exp - 1  # BUG: Decremento linear em vez de divisao por 2 (exp // 2)
    return res
```

---

## 3. Instrumentação com asserções (passos 1–5 do roteiro)

```python
def fast_exponentiation_broken(base: int, exp: int) -> int:
    original_base, original_exp = base, exp

    # 1. ASSERCAO DE PRE-CONDICAO
    assert base > 0 and exp >= 0, "Erro: Pre-condicao violada!"

    res = 1
    # Invariante de loop: res * (base ** exp) == original_base ** original_exp

    # 2. ASSERCAO DE INICIALIZACAO (CASO BASE)
    assert res * (base ** exp) == original_base ** original_exp, \
        "Erro: Invariante falhou na inicializacao!"

    while exp > 0:
        # Funcao Variante: V(state) = exp
        velha_variante = exp
        assert velha_variante >= 0, "Erro: Variante violou o limite inferior!"

        if exp % 2 == 1:
            res = res * base
        base = base * base
        exp = exp - 1  # BUG: decremento linear em vez de exp // 2

        # 3. ASSERCAO DE MANUTENCAO (PASSO INDUTIVO)
        assert res * (base ** exp) == original_base ** original_exp, \
            "Erro: Invariante violado no corpo do loop!"

        # 4. ASSERCAO DE DECREMENTO (PROGRESSO DA TERMINACAO)
        assert exp < velha_variante, \
            "Erro: Loop em execucao infinita (sem progresso)!"

    # 5. ASSERCAO DE POS-CONDICAO (DEDUCAO FINAL)
    assert res == original_base ** original_exp, \
        "Erro: A pos-condicao falhou na terminacao!"
    return res
```

---

## 4. Execução e análise da falha (passo 6 do roteiro)

Ao rodar `fast_exponentiation_broken(2, 10)` com o Data Set, o programa
estoura um `AssertionError` já na **1ª iteração do loop**, na asserção
de **manutenção (passo indutivo)**, linha 88 de
`problema8_potenciacao_rapida.py`:

```
Traceback (most recent call last):
  File "problema8_potenciacao_rapida.py", line 88, in fast_exponentiation_broken
    assert res * (base ** exp) == original_base ** original_exp, \
AssertionError: Erro: Invariante violado no corpo do loop!
```

### Razão aritmética do bug

O algoritmo de exponenciação por quadrados (fast exponentiation) se
baseia na identidade:

```
base^exp = (base^2)^(exp//2)              , se exp par
base^exp = base * (base^2)^((exp-1)//2)   , se exp ímpar
```

A cada iteração, o expoente que falta calcular deve ser reduzido pela
**metade** (`exp // 2`), compensando o fato de que `base` foi elevado
ao quadrado naquela mesma iteração. O invariante de loop
`res * base^exp == original_base^original_exp` só se mantém se essas
duas operações (elevar `base` ao quadrado e dividir `exp` por 2)
acontecerem em sincronia.

No código original, a linha `exp = exp - 1` decrementa o expoente de
1 em 1, enquanto `base` continua sendo elevado ao quadrado a cada
passo. Isso desequilibra a relação entre o crescimento de `base` e a
redução de `exp`, e o invariante deixa de valer já na primeira
iteração.

**Exemplo numérico (base=2, exp=10):**

| Estado | base | exp | `res * base^exp` |
|---|---|---|---|
| Antes do loop | 2 | 10 | `1 * 2^10 = 1024` ✅ (== esperado) |
| Após 1ª iteração (buggy) | 4 | 9 | `1 * 4^9 = 262144` ❌ (deveria continuar 1024) |

O quadrado de `base` "vale" uma divisão por 2 do expoente — não uma
subtração de 1. Além de produzir resultado incorreto, o decremento
linear também faz o algoritmo perder sua principal vantagem: a
complexidade deixa de ser `O(log exp)` e passa a ser `O(exp)`.

### Correção

```python
exp = exp // 2   # em vez de exp = exp - 1
```

---

## 5. Versão corrigida

```python
def fast_exponentiation_fixed(base: int, exp: int) -> int:
    original_base, original_exp = base, exp

    assert base > 0 and exp >= 0, "Erro: Pre-condicao violada!"

    res = 1
    assert res * (base ** exp) == original_base ** original_exp, \
        "Erro: Invariante falhou na inicializacao!"

    while exp > 0:
        velha_variante = exp
        assert velha_variante >= 0, "Erro: Variante violou o limite inferior!"

        if exp % 2 == 1:
            res = res * base
        base = base * base
        exp = exp // 2  # CORRECAO

        assert res * (base ** exp) == original_base ** original_exp, \
            "Erro: Invariante violado no corpo do loop!"
        assert exp < velha_variante, \
            "Erro: Loop em execucao infinita (sem progresso)!"

    assert res == original_base ** original_exp, \
        "Erro: A pos-condicao falhou na terminacao!"
    return res
```

### Resultado dos testes (Data Set)

```
base=2, exp=10 -> resultado=1024 (esperado=1024) [OK]
base=5, exp=0  -> resultado=1    (esperado=1)    [OK]
```

---

## 6. Como executar

```bash
python3 problema8_potenciacao_rapida.py
```

**Saída esperada:**

```
=== 1) Rodando a versao BUGGY (deve estourar AssertionError) ===
AssertionError capturado, como esperado: Erro: Invariante violado no corpo do loop!

=== 2) Rodando a versao CORRIGIDA no Data Set completo ===
base=2, exp=10 -> resultado=1024 (esperado=1024) [OK]
base=5, exp=0 -> resultado=1 (esperado=1) [OK]
```

## 7. Arquivos desta pasta

```
problema8/
├── README.md
└── problema8_potenciacao_rapida.py
```
