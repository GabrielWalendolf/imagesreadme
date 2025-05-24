# Função auxiliar para verificar se uma string é um binário válido
def eh_binario_8bits(s):
    return len(s) == 8 and all(c in '01' for c in s)

# Função auxiliar para verificar se o número binário é negativo (bit de sinal em complemento de dois)
def eh_negativo(s):
    return s[0] == '1'

# Função para inverter bits (usada no complemento de dois)
def inverter_bits(bits):
    return ''.join('1' if b == '0' else '0' for b in bits)

# Função para somar dois números binários de 8 bits (sem conversão para decimal)
def soma_binaria(a, b):
    resultado = ''
    carry = 0

    for i in range(7, -1, -1):  # Percorre os bits da direita para esquerda
        soma = carry
        soma += int(a[i])
        soma += int(b[i])
        resultado = str(soma % 2) + resultado
        carry = soma // 2

    # Verifica overflow
    if (a[0] == b[0]) and (resultado[0] != a[0]):
        raise Exception("overflow")

    return resultado

# Função para subtrair dois binários (a - b) usando complemento de dois
def subtracao_binaria(a, b):
    # Complemento de dois de b
    b_invertido = inverter_bits(b)
    b_complemento = soma_binaria(b_invertido, '00000001')
    return soma_binaria(a, b_complemento)

# Função de multiplicação usando soma e shifts
def multiplicacao_binaria(a, b):
    # Guarda sinal
    sinal_resultado = '0' if a[0] == b[0] else '1'

    # Converte ambos para positivo se forem negativos (complemento de dois)
    if eh_negativo(a):
        a = subtracao_binaria('00000000', a)
    if eh_negativo(b):
        b = subtracao_binaria('00000000', b)

    resultado = '00000000'
    temp_b = b

    for i in range(7, -1, -1):
        if temp_b[-1] == '1':
            resultado = soma_binaria(resultado, a)
        a = a[1:] + '0'  # shift left
        temp_b = '0' + temp_b[:-1]  # shift right

    if sinal_resultado == '1':
        resultado = subtracao_binaria('00000000', resultado)

    # Verifica overflow
    if resultado[0] != sinal_resultado:
        raise Exception("overflow")

    return resultado

# Função principal conforme especificado
def calcular(n1, n2, operacao):
    # Valida entrada
    if not (eh_binario_8bits(n1) and eh_binario_8bits(n2)):
        raise Exception("valor invalido")
    if len(n1) != 8 or len(n2) != 8:
        raise Exception("tamanho da entrada invalido")
    if operacao not in ['+', '-', 'x']:
        raise Exception("valor invalido")

    # Executa a operação desejada
    if operacao == '+':
        return soma_binaria(n1, n2)
    elif operacao == '-':
        return subtracao_binaria(n1, n2)
    elif operacao == 'x':
        return multiplicacao_binaria(n1, n2)