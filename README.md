# Planejando rotas para entregadores

Neste projeto, usamos do algoritimo AEstrela para fazer uma IA que indica aos entregadores o caminho até a entrega de menor custo.

## Authors

- [@ninasavoy](https://github.com/ninasavoy)
- [@mmp052](https://github.com/mmp052)
- [@danielprado99](https://github.com/danielprado99)

# Instruções
O arquivo que deve ser executado é o interface.py

Depois de executar é só clicar ou em usar o mapa pelo arquivo, o nome padrão do arquivo de mapa que o programa lê é Mapa1.json, pra mudar é só mexer na linha 275 do interface.py. Ou voce pode criar o mapa do zero.

No menu de criação do mapa basta clicar no elemento que voce quer adicionar, o elemento sera marcado de vermelho, dai clicar em qual quadrado do mapa voce quer botar o elemento.
Algumas observações:
- a entrega precisa ter um cliente e vice versa, então se nessa tela você adicionar um 2 clientes e só uma entrega e apertar ok, só vai renderizar o par 1 cliente e 1 entrega.
- depois de adicionar todos os elementos que voce quer no mapa clique em "OK"

A proxima tela é a de execução onde você pode adicionar elementos em tempo real, seguindo o mesmo esquema da tela de criar mapa, mas sem precisar apertar ok no final e não é possivel adicionar obstaculos.
