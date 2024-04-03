from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from aigyminsper.search.SearchAlgorithms import BuscaGananciosa
from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.SearchAlgorithms import AEstrela
from aigyminsper.search.Graph import State
import json

class Entregador(State):
    def __init__(self, op: str, tamanho: list, pos: list, pos_pessoa: list, pos_encomenda: list, pos_obstaculos: list, direcao: str, encomenda: bool, pessoa: bool):
        self.operator = op # ação que ele vai realizar
        self.tamanho = tamanho # dimensão do mapa, pra um mapa com 5 linhas e 7 colunos fica [5,7]
        self.pos = pos # posição do entregador em [linha, coluna]. lembrando que as linhas e colunas começão pelo 1, então a primeira da esquerda em cima é a pos [1,1]
        self.pos_pessoa = pos_pessoa # posição do cliente
        self.pos_encomenda = pos_encomenda # posição da encomenda
        self.pos_obstaculos = pos_obstaculos # posições dos obstaculos
        self.direcao = direcao # direção pra onde o entregador está olhando
        self.encomenda = encomenda # boleano pra indicar se pegou a encomenda
        self.pessoa = pessoa # boleano pra indicar se entregou a encomenda
        print(self.pos)
        print(self.pos_encomenda)
    

    def successors(self):
        successors = []

        if self.pos == self.pos_encomenda and self.encomenda == False:
            successors.append(Entregador("pegar encomenda", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, True, self.pessoa))

        if self.pos == self.pos_pessoa and self.pessoa == False and self.encomenda == True:
            successors.append(Entregador("entregar encomenda", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, self.encomenda, True))

        if self.direcao == "dir":
            successors.append(Entregador("virar dir", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "baixo", self.encomenda, self.pessoa))
            successors.append(Entregador("virar esq", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "cima", self.encomenda, self.pessoa))
            if self.pos[1] + 1 <= self.tamanho[1] and [self.pos[0],self.pos[1] + 1] not in self.pos_obstaculos:
                successors.append(Entregador("ir pra frente", self.tamanho, [self.pos[0], self.pos[1] + 1], self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, self.encomenda, self.pessoa))

        if self.direcao == "esq":
            successors.append(Entregador("virar dir", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "cima", self.encomenda, self.pessoa))
            successors.append(Entregador("virar esq", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "baixo", self.encomenda, self.pessoa))
            if self.pos[1] - 1 > 0 and [self.pos[0],self.pos[1] - 1] not in self.pos_obstaculos:
                successors.append(Entregador("ir pra frente", self.tamanho, [self.pos[0], self.pos[1] - 1], self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, self.encomenda, self.pessoa))
        
        if self.direcao == "cima":
            successors.append(Entregador("virar dir", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "dir", self.encomenda, self.pessoa))
            successors.append(Entregador("virar esq", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "esq", self.encomenda, self.pessoa))
            if self.pos[0] - 1 > 0 and [self.pos[0] - 1,self.pos[1]] not in self.pos_obstaculos:
                successors.append(Entregador("ir pra frente", self.tamanho, [self.pos[0] - 1, self.pos[1]], self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, self.encomenda, self.pessoa))
        
        if self.direcao == "baixo":
            successors.append(Entregador("virar dir", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "esq", self.encomenda, self.pessoa))
            successors.append(Entregador("virar esq", self.tamanho, self.pos, self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, "dir", self.encomenda, self.pessoa))
            if self.pos[0] + 1 <= self.tamanho[0] and [self.pos[0] + 1,self.pos[1]] not in self.pos_obstaculos:
                successors.append(Entregador("ir pra frente", self.tamanho, [self.pos[0] + 1, self.pos[1]], self.pos_pessoa, self.pos_encomenda, self.pos_obstaculos, self.direcao, self.encomenda, self.pessoa))

        
        return successors
    
    def is_goal(self):
        return self.encomenda and self.pessoa
    
    def description(self):
        return "entregador pica"
    
    def cost(self):
        return 1
    
    def print(self):
        return str(self.operator)
    
    def env(self):
        return f"{self.pos} {self.direcao} {self.encomenda} {self.pessoa}"
    
    def h(self):
        if not self.encomenda:
            distancia = abs(self.pos[0] - self.pos_encomenda[0] ) + abs(self.pos[1] - self.pos_encomenda[1])
        else:
            distancia = abs(self.pos[0] - self.pos_pessoa[0] ) + abs(self.pos[1] - self.pos_pessoa[1])
        return distancia
    


