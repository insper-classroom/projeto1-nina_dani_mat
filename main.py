from Entregador import Entregador
from aigyminsper.search.SearchAlgorithms import AEstrela
import json


with open('Mapa1.json', 'r') as arquivo:
    mapa = json.load(arquivo)
    
    while len(mapa[2]) > 0:
        resultados = []

        for i in range(len(mapa[2])):    
            state = Entregador("", mapa[0], mapa[1], mapa[2][i][0], mapa[3][i], mapa[4], "dir", False, False)
            algoritimo = AEstrela()
            result = algoritimo.search(state, trace=False, pruning="general")
            if result != None:
                resultado_ent = (result.show_path(), result.g, mapa[2][i][1])
                resultados.append(resultado_ent)
            else:
                resultados.append("não achei solução")


        menor_custo = float("inf")
        for resultado in resultados:
            if type(resultado) == tuple:
                print(f"Custo para atender o cliente {resultado[2]}: {resultado[1]}")
            else:
                print(f"Não achou solução para o cliente {resultado[2]}")
            
            if resultado[1] < menor_custo:
                menor_custo = resultado[1]
                indice = resultados.index(resultado)

        print(f"O cliente {indice} será atendido")
        mapa[1] = mapa[2][indice]
        mapa[2].pop(indice)
        mapa[3].pop(indice)
        print(mapa[2])





