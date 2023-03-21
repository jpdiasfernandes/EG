#!/usr/bin/env python3
from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
import sys
from statistics import mean


class Aluno:
    def __init__(self, nome, notas):
        self.nome = nome
        self.notas = notas
        self.media = mean(notas)

    def printMedia(self):
        print(self.nome + ": " + str(self.media))

class Turma:
    def __init__(self, id_turma, alunos):
        self.id_turma = id_turma
        self.alunos = alunos

    def printMedia(self):
        print("Média turma " + str(self.id_turma) + ": ")
        for aluno in self.alunos:
            aluno.printMedia()
        print(" ")

class State:
    def __init__(self):
        self.turma_atual = None
        self.alunos_atual = set()
        self.no_alunos = 0
        self.turmas = {}
        self.groupByNotas = {}
        self.queries = '''CREATE TABLE escola (
        nomeAluno VARCHAR(50) PRIMARY KEY,
        nota INT,
        turma VARCHAR(50),
        dataInsercao DATETIME
); INSERT INTO Resultado (nomeAluno, nota, dataInsercao, turma)\nVALUES\n
'''
        self.markdown = "# Visualizador de turmas\n"
        self.html = ''' <html> <!DOCTYPE html>
               <body>
        '''

    def addInitHtmlTurma(self, turma_id):
        self.html += f'''
<h1>Turma {turma_id}<code><br /></code></h1>
<table style="border-collapse: collapse; width: 100%; height: 81px;" border="1">
<tbody>
<tr style="height: 18px;">
<td style="width: 10%; height: 18px; text-align: center;">Nome</td>
        '''

    def addQueryAluno(self, nome, nota, turma_id):
        #garante que o "
        self.queries += f"({nome}, {nota}, NOW(), {turma_id});\n"

    def addTurmaInitMd(self, id):
        md = f"## Turma {id}\n### Lista de alunos\n"
        self.markdown += md

    def addNameMd(self, nome):
        self.markdown += f"- {nome}\n"

    def addTurmaMd(self, t):
        md = ""
        md += "### Notas \n\n"

        md += "| Aluno | Media |\n| --------- | ---------|\n"

        for aluno in t.alunos:
            md += f"| {aluno.nome} | {aluno.media} |\n"

        self.markdown += md

    def addTurmaHTML(self, t):
        _max = 0
        for aluno in t.alunos:
            if _max < len(aluno.notas):
                _max = len(aluno.notas)

        tmp = ""
        for i in range(0,_max):
            tmp += f'<td style="width: 10%; height: 18px; text-align: center;">Nota{i}</td>'

        tmp += '''
<td style="width: 10%; height: 18px; text-align: center;">M&eacute;dia</td>
<td style="width: 10%; height: 18px; text-align: center;">&nbsp;</td>
</tr>
        '''

        for aluno in t.alunos:
            tmp += f'''
<tr style="height: 21px;">
<td style="width: 10%; text-align: center; height: 21px;">{aluno.nome}</td>
            '''
            for i in range(0,_max):
                value = '-'
                if i < len(aluno.notas):
                    value = aluno.notas[i]
                tmp += f'<td style="width: 10%; text-align: center; height: 21px;">{value}</td>\n'

            tmp += f'<td style="width: 10%; text-align: center; height: 21px;">{round(sum(aluno.notas) / _max)}</td>'
            if sum(aluno.notas) / _max > 10:
                tmp += f'<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-embarassed.gif" alt="embarassed" /></td>\n'
            else:
                tmp += '<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-cry.gif" alt="cry" /></td>\n'

            tmp += '</tr>\n'
        tmp += '</table>\n'

        self.html += tmp






class MyInterpreter(Interpreter):
  def __init__(self):
      self.medias = {}
      self.atual = ""
      self.contagem = 0
      self.state = State()

  def turmas(self,listaTurmas):
    #start: turma+
    for turma in listaTurmas.children:
      self.visit(turma)

    self.state.html += '''</body></html>'''
    print(self.state.html)

  def turma(self,turma):
    #turma : ("TURMA" MAIUSCULA+ alunos PONTO)
    #turma : "TURMA" ID (aluno ";")* aluno "."

    id = turma.children[0].value
    self.state.turma_atual = id
    self.state.alunos_atual = set()
    self.state.addInitHtmlTurma(self.state.turma_atual)
    self.state.addTurmaInitMd(self.state.turma_atual)
    alunos = []
    for elemento in turma.children:
      if (type(elemento) == Tree):
        #print("TURMA",turma.children[0])
        alunos.append(self.visit(elemento))

    # Tenho todos os alunos adicionar ao dicionário de turmas
    t = Turma(id, alunos)

    # Fazer append de informação sobre a turma no markdown
    self.state.addTurmaMd(t)
    # Fazer append de informação sobre a turma no html
    self.state.addTurmaHTML(t)
    self.state.turmas[id] = t

  #def alunos(self,alunos):
  #  #alunos: aluno (PONTOVIRGULA aluno)*
  #  print("Visitar os alunos")
  #  alunosList = []
  #  # Visitar todos os alunos
  #  for element in alunos.children:
  #    # So visitamos os tipo tree que sao os alunos
  #    if (type(element) == Tree and element.data == "aluno"):
  #      aluno = self.visit(element)
  #      alunosList.append(aluno)
  #  return alunosList

  def aluno(self,aluno):
    #aluno: idaluno "(" (nota ("," nota)*)? ")"
    #print("Visitar o aluno",aluno.children[0])
    # atualizar número de alunos
    self.state.no_alunos += 1

    notas = []
    nome = None
    if aluno.children[0].data == "idaluno":
        nome = aluno.children[0].children[0].value
        # adicionar nome ao markdown
        self.state.addNameMd(nome)

        # Se o nome já existir avisar que o registo a ser
        # feito na base dados vai ser ignorado
        if nome in self.state.alunos_atual:
            print(f"Registo ignorado porque o nome {nome} já existe na turma {self.state.turma_atual}.", file=sys.stderr)
        else:
            self.state.alunos_atual.add(nome)

    for nota_it in aluno.children[1:]:
        if nota_it.data == "nota" and nota_it.children[0].type == "NUMBER":
            # visitar a nota e retornar o valor dela
            nota = self.visit(nota_it)
            # append da nota
            notas.append(nota)

            if nota not in self.state.groupByNotas.keys():
                self.state.groupByNotas[nota] = set()
            # adicionar a nota e o nome ao groupBy
            self.state.groupByNotas[nota].add(nome)

            # adicionar informações do aluno à query
            self.state.addQueryAluno(nome, nota, self.state.turma_atual)

    return Aluno(nome, notas)

  def nota(self, nota):
      nota = float(nota.children[0].value)
      return nota

grammar = '''
turmas: turma+
turma : "TURMA" ID (aluno ";")* aluno "."
aluno: idaluno "(" (nota ("," nota)*)? ")"
idaluno: WORD
nota: NUMBER
ID: "A".."Z"+

%import common.NUMBER
%import common.UCASE_LETTER
%import common.WORD
%import common.WS
%ignore WS
'''

# Definir o texto-fonte (input) a analisar
#frase = "TURMA A ana (12, 13, 15, 12, 13, 15, 14); joao (9,7,3,6,9,12); xico (12,16).TURMA B lucas (12, 13, 15, 12, 13, 15, 14); joana (9,7,3,6,9,12); xica (12,16)."
frase = "TURMA A ana (1,2,3); ze (2,4);rui(12). TURMA PL zeca(2); rita(2,4,6). TURMA EG rosa (10,11,12,13)."

# Inicializar o objeto lark
p = Lark(grammar,start="turmas")
# Criar a parsing tree
parse_tree = p.parse(frase)
# Utilizar o Interpreter para visitar a parsing tree
data = MyInterpreter().visit(parse_tree)
