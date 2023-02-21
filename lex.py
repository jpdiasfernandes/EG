#!/usr/bin/env python3
import ply.lex as lex

tokens = "SINAL PA PF NUM VIR".split(" ")

t_PA = r'\['
t_PF = r'\]'
t_NUM = r'[-+]?\d+'
t_VIR = r','
t_SINAL =r'[+-]'

t_ignore = " \t\n"

def t_error(t):
    print('Carácter ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
