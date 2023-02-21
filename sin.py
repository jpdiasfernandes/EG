#!/usr/bin/env python3


import ply.yacc as yacc

from lex import tokens

def limites(lista, sinal):
    for elem in lista:
        if sinal == '+':
            if elem[0] >= elem[1]:
                return False
        else:
            if elem[0] <= elem[1]:
                return False
    return True

def intercetam(lista, sinal):
    top = None

    for elem in lista:
        if top != None:
            if sinal == '+':
                if elem[0] < top:
                    return True
            else:
                if elem[0] > top:
                    return True
        if sinal == '+':
            top = elem[1]
        else:
            top = elem[0]

    return False

def comp_intervalos(lista):
    res = []
    for elem in lista:
        res.append(elem[1] - elem[0])
    return res

def int_longo(lista):
    max = None
    max_int = None
    for elem in lista:
        diff = abs(elem[1] - elem[0])
        if max == None or diff > max:
            max = diff
            max_int = elem

    return max_int

def int_curto(lista):
    min = None
    min_int = None
    for elem in lista:
        diff = abs(elem[1] - elem[0])
        if min == None or diff < min:
            min = diff
            min_int = elem

    return min_int

def amplitude(lista):
    first = lista[0][0]
    last = lista[len(lista)-1][1]
    return abs(last - first)


def validacao_semantica(lista, sinal,p):
    if intercetam(lista,sinal) or not limites(lista,sinal):
        print("erro sintático: ", p)
        parser.success = False
    else:
        parser.no_intervalos = len(lista)
        parser.comp_int = comp_intervalos(lista)
        parser.int_longo = int_longo(lista)
        parser.int_curto = int_curto(lista)
        parser.amplitude = amplitude(lista)



def p_Axioma(p):
    "Axioma : SINAL Intervalos"
    lista = p[2]
    sinal = p[1]
    validacao_semantica(lista,sinal,p)
    if parser.success:
        print("Número de intervalos: ", parser.no_intervalos)
        print("Lista de comprimento dos intervalos: ", parser.comp_int)
        print("Intervalo mais longo: ", parser.int_longo)
        print("Intervalo mais curto: ", parser.int_curto)
        print("Amplitude lista: ", parser.amplitude)



def p_Intervalos(p):
    "Intervalos : Intervalos Intervalo"
    p[0] = p[1] + [p[2]]

def p_Intervalos_empty(p):
    "Intervalos : Intervalo"
    p[0] = [p[1]]

def p_Intervalo(p):
    "Intervalo : PA NUM VIR NUM PF"
    res = []
    res.append(int(p[2]))
    res.append(int(p[4]))
    p[0] = res

def p_error(p):
    print("erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()

parser.intervalos = []
parser.crescente = None

import sys

for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
        print("Frase válida: ", linha)
    else:
        print("Frase inválida... Corrija e tente novamente")
