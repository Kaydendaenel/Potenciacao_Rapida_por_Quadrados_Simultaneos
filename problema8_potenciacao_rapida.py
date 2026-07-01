"""
=================================================================
Problema 8: Potenciacao Rapida por Quadrados Simultaneos
Disciplina: Matematica Discreta - Verificacao Formal de Programas
=================================================================

Especificacao:
    Pre-condicao:  base > 0, exp >= 0
    Pos-condicao:  p = base ** exp
    Invariante de loop: res * (base ** exp) == original_base ** original_exp
    Funcao Variante: V(state) = exp  (deve decrescer estritamente ate 0)

Data Set:
    base=2, exp=10  -> p=1024
    base=5, exp=0   -> p=1


-----------------------------------------------------------------
PASSO 6 - EXECUCAO E ANALISE DA FALHA (codigo original/buggy)
-----------------------------------------------------------------
Ao rodar fast_exponentiation_broken(2, 10) com as assercoes do
roteiro, o programa estoura um AssertionError logo na 1a iteracao,
na assercao de MANUTENCAO (passo indutivo):

    assert res * (base ** exp) == original_base ** original_exp, \
        "Erro: Invariante violado no corpo do loop!"

Razao aritmetica do bug:
    O algoritmo de potenciacao rapida (exponenciacao por quadrados)
    se baseia na identidade:
        base^exp = (base^2)^(exp//2)              , se exp par
        base^exp = base * (base^2)^((exp-1)//2)   , se exp impar
    Ou seja, a cada passo a "massa" da potencia que falta ser
    calculada deve ser reduzida pela METADE (exp // 2), compensando
    o fato de que 'base' foi elevado ao quadrado.

    No codigo buggy, a linha
        exp = exp - 1     # BUG
    decrementa exp de 1 em 1, mas 'base' continua sendo elevado ao
    quadrado a cada iteracao. Isso quebra a relacao entre quanto
    'base' cresceu e quanto 'exp' diminuiu: o produto
    res * base^exp deixa de ser igual a original_base^original_exp
    ja na primeira iteracao.

    Exemplo numerico (base=2, exp=10):
      Antes do loop: res=1, base=2, exp=10  -> 1*2^10 = 1024 (OK)
      1a iteracao (exp par, res nao muda):
          base = 2*2 = 4
          exp  = 10-1 = 9   (deveria ser 10//2 = 5)
          Verificacao: res*base^exp = 1*4^9 = 262144 != 1024
      O invariante quebra porque o quadrado de 'base' "vale" por uma
      divisao por 2 do expoente, nao por uma subtracao de 1.

    Consequencia secundaria: alem de dar resultado errado, o
    decremento linear faz o algoritmo perder sua principal vantagem
    (complexidade O(log exp) vira O(exp)).

Correcao:
    Trocar exp = exp - 1  por  exp = exp // 2
"""


def fast_exponentiation_broken(base: int, exp: int) -> int:
    """Versao ORIGINAL com bug, instrumentada com assercoes."""
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


def fast_exponentiation_fixed(base: int, exp: int) -> int:
    """Versao CORRIGIDA, instrumentada com assercoes."""
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
        exp = exp // 2  # CORRECAO: divisao inteira por 2

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


if __name__ == "__main__":
    dataset = [(2, 10, 1024), (5, 0, 1)]

    print("=== 1) Rodando a versao BUGGY (deve estourar AssertionError) ===")
    try:
        fast_exponentiation_broken(2, 10)
    except AssertionError as e:
        print(f"AssertionError capturado, como esperado: {e}\n")

    print("=== 2) Rodando a versao CORRIGIDA no Data Set completo ===")
    for base, exp, esperado in dataset:
        resultado = fast_exponentiation_fixed(base, exp)
        status = "OK" if resultado == esperado else "FALHOU"
        print(f"base={base}, exp={exp} -> resultado={resultado} "
              f"(esperado={esperado}) [{status}]")
