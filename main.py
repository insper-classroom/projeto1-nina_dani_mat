from Entregador import Entregador
from aigyminsper.search.SearchAlgorithms import AEstrela
import json

class Solucao:

    def __init__(self, mapa: list) -> None:
        self.mapa = mapa

    def run(self):
            
        resultados = []

        for i in range(len(self.mapa[2])):  
            state = Entregador("", self.mapa[0], self.mapa[1], self.mapa[2][i][0], self.mapa[3][i], self.mapa[4], "dir", False, False)
            algoritimo = AEstrela()
            result = algoritimo.search(state, trace=False, pruning="general")
            if result != None:
                resultado_ent = (result.show_path(), result.g, self.mapa[2][i][1])
                resultados.append(resultado_ent)
            else:
                resultados.append("não achei solução")


        menor_custo = float("inf")
        self.resultados = resultados
        for resultado in resultados:
            if type(resultado) == tuple:
                print(f"Custo para atender o cliente {resultado[2]}: {resultado[1]}")
            else:
                print(f"Não achou solução para o cliente {resultado[2]}")
            
            if resultado[1] < menor_custo:
                menor_custo = resultado[1]
                indice = resultados.index(resultado)
                self.indice = indice

        print(f"O cliente {resultados[indice][2]} será atendido")
    
        # mapa[1] = mapa[2][indice][0]
        # mapa[2].pop(indice)
        # mapa[3].pop(indice)

# solucao = Solucao('Mapa1.json')
# solucao.run()