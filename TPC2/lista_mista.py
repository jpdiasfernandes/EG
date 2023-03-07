#!/usr/bin/env python3
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark import Transformer
from lark import Discard
import sys

grammar = '''
//Regras Sintaticas
start: elemento "."
elemento : elem (VIR elem)*
elem: WORD | NUMERO
//Regras Lexicográficas
NUMERO:"0".."9"+
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WORD
%import common.WS
%ignore WS
'''
# Soma da lista, encontrar o maior da lista
def getSoma(lista):
  soma = 0
  soma_ant = 0
  start = False

  for elem in lista:
    if start:
      if type(elem) == int:
        soma += elem
      elif elem == "fim":
        soma_ant += soma
        soma = 0
        start = False
    elif elem == "agora":
      start = True

  return soma_ant

def verifica(lista):
  abre_count = 0
  abriu_last = False
  for elem in lista:
    if elem == 'agora':
      abriu_last = True
      abre_count += 1
    elif elem == 'fim':
      if abriu_last:
        return False
      abre_count -= 1
    else:
      abriu_last = False
  return abre_count == 0

class ExemploTransformer(Transformer):
  max = None
  soma = None
  def start(self,elementos):
    #print("start")
    #print(str(elementos))
    #elemento = elementos[1]
    #print("Lista: " + str(elemento) + "\nSomatório: " + str(sum(elemento)) + "\nMáximo: " + str(max(elemento)) + "\n")
    lista = elementos[0]
    soma = 0
    print("Lista " + str(lista) + "")
    print("Há " + str(len(lista)) + " elementos.")
    print("O elemento mais frequente é " + str(max(set(lista), key = lista.count)) + ".")
    print("A soma total de número entre Agora e fins é: " + str(getSoma(lista)))
    valida = "A lista é considerada "
    if not verifica(lista):
      valida += "não "
    print(valida + "válida.")

    ##print(elementos)

  def elemento(self,elemento):
    #print("elemento")
    elemento = [item for sublist in elemento for item in sublist]
    #print(elemento)
    return elemento

  def elem (self,elem):
    #print("elem")
    return elem
    #return int(elem)

  def WORD (self,word):
      return str(word)

  def NUMERO(self, numero):
      print(numero)
      return int(numero)

  def VIR(self,vir):
    #print("vir")
    #print(vir)
    return Discard

  pass


p = Lark(grammar)   #não muito bem
#p = Lark(grammar1)  #recomendada
#p = Lark(grammar2)  #incorreta
#p = Lark(grammar3)  #incorreta
#p = Lark(grammar4)   #aceitável


for frase in sys.stdin:
    tree = p.parse(frase)
    print(tree.pretty())
    data = ExemploTransformer().transform(tree) # chamar o transformer para obter
#for element in tree.children:
  #print(element)


#print(data)
