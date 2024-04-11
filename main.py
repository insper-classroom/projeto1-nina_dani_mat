from Entregador import Entregador
from aigyminsper.search.SearchAlgorithms import AEstrela
import json

class Solucao:

    def __init__(self, mapa: list, indice_entregador) -> None:
        self.mapa = mapa
        self.indice_entregador = indice_entregador

    def run(self):
        disponivel = False
            
        resultados = []

        for entrega in self.mapa[3]:
            if entrega[1] == -1:
                disponivel = True
                break
        if disponivel:
            for j in range(len(self.mapa[1])):
                for i in range(len(self.mapa[2])):  
                    if self.mapa[3][i][1] == -1:
                        state = Entregador("", self.mapa[0], self.mapa[1][j][0], self.mapa[2][i][0], self.mapa[3][i][0], self.mapa[4], "dir", False, False)
                        algoritimo = AEstrela()
                        result = algoritimo.search(state, trace=False, pruning="general")
                        if result != None:
                            # caminho; custo; id do cliente; id do entregador; indice da encomenda; cliente; encomenda
                            resultado_ent = (result.show_path(), result.g, self.mapa[2][i][1], self.mapa[1][j][1], i, self.mapa[2][i], self.mapa[3][i])
                            resultados.append(resultado_ent)
                        else:
                            resultados.append("não achei solução")


            menor_custo = float("inf")
            indice = -1
            self.resultados = resultados
            for resultado in resultados:
                if type(resultado) == tuple:
                    print(f"Custo do entregador {resultado[3]} para atender o cliente {resultado[2]}: {resultado[1]}")
                else:
                    print(f"Não achou solução para o cliente {resultado[2]}")
                
                if resultado[1] < menor_custo and resultado[3] == self.indice_entregador:
                    menor_custo = resultado[1]
                    indice = resultados.index(resultado)
                    self.indice = indice

            #pego o id do intregador e indico na encomenda
            self.mapa[3][resultados[indice][4]][1] = resultados[indice][3]
            print(f"O entregador {resultados[indice][3]} vai antender o cliente {resultados[indice][2]}")
        else:
            self.resultados = [None]
            self.indice = 0
    
        # mapa[1] = mapa[2][indice][0]
        # mapa[2].pop(indice)
        # mapa[3].pop(indice)

# solucao = Solucao('Mapa1.json')
# solucao.run()