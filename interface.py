import pygame
import json
import threading
from main import Solucao

class Deliveryman(pygame.sprite.Sprite):

    def __init__(self, x, y, grupos, nome_mapa) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
        self.rect = self.image.get_rect()
        #vou fazer o x e o y -1 pq no dicionario do mapa a posicao é em linha, coluna
        self.rect.x = (x - 1) * TAMANHO_BLOCO
        self.rect.y = (y - 1) * TAMANHO_BLOCO
        self.grupos = grupos
        self.grupos['all_sprites'].add(self)
        self.caminho = None
        self.nome_mapa = nome_mapa

    def update(self) -> None:
        if self.caminho == None:
            solucao = Solucao(self.nome_mapa)
            threading.Thread(target=solucao.run())
            self.caminho = solucao.resultados[solucao.indice][0]
        else:
            print(self.caminho)

class Cliente(pygame.sprite.Sprite):

    def __init__(self, pos, grupos) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/pessoa.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
        self.rect = self.image.get_rect()
        #vou fazer o x e o y -1 pq no dicionario do mapa a posicao é em linha, coluna
        #o x é a coluna e o y é a linha
        self.rect.x = (pos[1] - 1) * TAMANHO_BLOCO
        self.rect.y = (pos[0] - 1) * TAMANHO_BLOCO
        self.grupos = grupos
        self.grupos['all_sprites'].add(self)

class Encomenda(pygame.sprite.Sprite):

    def __init__(self, pos, grupos) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
        self.rect = self.image.get_rect()
        #vou fazer o x e o y -1 pq no dicionario do mapa a posicao é em linha, coluna
        #o x é a coluna e o y é a linha
        self.rect.x = (pos[1] - 1) * TAMANHO_BLOCO
        self.rect.y = (pos[0] - 1) * TAMANHO_BLOCO
        self.grupos = grupos
        self.grupos['all_sprites'].add(self)
    

pygame.init()

#constantes
TAMANHO_BLOCO = 50
FPS = 60  # Frames per Second
BLACK = (0, 0, 0)
WHITE = (255,255,255)

grupos = {'all_sprites': pygame.sprite.Group()}
nome_mapa = 'Mapa1.json'

with open(nome_mapa, 'r') as arquivo:
    mapa = json.load(arquivo)

tamanho_mapa = mapa[0]

#x é a coluna e y é a linha
entregador = Deliveryman(mapa[1][1], mapa[1][0], grupos, nome_mapa)

for cliente in mapa[2]:
    Cliente(cliente[0], grupos)

for encomenda in mapa[3]:
    Encomenda(encomenda, grupos)

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((tamanho_mapa[1] * TAMANHO_BLOCO, tamanho_mapa[0] * TAMANHO_BLOCO))
clock = pygame.time.Clock()

rodando = True
while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    grupos['all_sprites'].update()

    # Controlar frame rate
    clock.tick(FPS)

    # Desenhar fundo
    screen.fill(BLACK)

    #Desenhar mapa
    for i in range(tamanho_mapa[0]):
        for j in range(tamanho_mapa[1]):
            pygame.draw.rect(screen, WHITE, pygame.Rect(j * TAMANHO_BLOCO, i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

    #Desenhar os obstaculos
    for pos in mapa[4]:
        pygame.draw.rect(screen, WHITE, pygame.Rect((pos[1] - 1) * TAMANHO_BLOCO, (pos[0] - 1) * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))

    grupos['all_sprites'].draw(screen)

    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()