import pygame
import json
import threading
from main import Solucao

class Deliveryman(pygame.sprite.Sprite):

    def __init__(self, x, y, grupos, nome_mapa) -> None:
        super().__init__()
        self.imagem_direita = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
        self.imagem_baixo = pygame.transform.rotate(self.imagem_direita, -90)
        self.imagem_esquerda = pygame.transform.flip(self.imagem_direita, True, False)
        self.imagem_cima = pygame.transform.rotate(self.imagem_esquerda, -90)
        self.image = self.imagem_direita
        self.rect = self.image.get_rect()
        #vou fazer o x e o y -1 pq no dicionario do mapa a posicao é em linha, coluna
        self.rect.x = (x - 1) * TAMANHO_BLOCO
        self.rect.y = (y - 1) * TAMANHO_BLOCO
        self.grupos = grupos
        self.grupos['all_sprites'].add(self)
        self.grupos['entregadores'].add(self)
        self.caminho = None
        self.nome_mapa = nome_mapa
        self.direcao = 'direita'

    def update(self) -> None:
        if self.direcao == 'direita':
            self.image = self.imagem_direita
        
        if self.direcao == 'esquerda':
            self.image = self.imagem_esquerda

        if self.direcao == 'cima':
            self.image = self.imagem_cima

        if self.direcao == 'baixo':
            self.image = self.imagem_baixo

        if self.caminho == None:
            if len(mapa[2]) != 0:
                self.solucao = Solucao(mapa)
                threading.Thread(target=self.solucao.run())
                self.caminho = self.solucao.resultados[self.solucao.indice][0].split(';')
        else:
            passo = self.caminho[0].strip()

            if passo == 'ir pra frente':
                if self.direcao == 'direita':
                    self.rect.x += TAMANHO_BLOCO

                elif self.direcao == 'esquerda':
                    self.rect.x -= TAMANHO_BLOCO
                
                elif self.direcao == 'cima':
                    self.rect.y -= TAMANHO_BLOCO
                    
                elif self.direcao == 'baixo':
                    self.rect.y += TAMANHO_BLOCO

            if passo == 'virar dir':
                if self.direcao == 'direita':
                    self.direcao = 'baixo'

                elif self.direcao == 'esquerda':
                    self.direcao = 'cima'
                
                elif self.direcao == 'cima':
                    self.direcao = 'direita'
                    
                elif self.direcao == 'baixo':
                    self.direcao = 'esquerda'

            if passo == 'virar esq':
                if self.direcao == 'direita':
                    self.direcao = 'cima'

                elif self.direcao == 'esquerda':
                    self.direcao = 'baixo'
                
                elif self.direcao == 'cima':
                    self.direcao = 'esquerda'
                    
                elif self.direcao == 'baixo':
                    self.direcao = 'direita'

            if passo == 'pegar encomenda':
                pygame.sprite.spritecollide(self, self.grupos['encomendas'], True)

            if passo == 'entregar encomenda':
                pygame.sprite.spritecollide(self, self.grupos['clientes'], True)

            del self.caminho[0]

            mapa[1] = [self.rect.y / TAMANHO_BLOCO + 1, self.rect.x / TAMANHO_BLOCO + 1]

            if len(self.caminho) == 0:
                self.caminho = None 
                del mapa[2][self.solucao.indice]
                del mapa[3][self.solucao.indice]
                self.direcao = 'direita'


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
        self.grupos['clientes'].add(self)

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
        self.grupos['encomendas'].add(self)
    

pygame.init()

#constantes
TAMANHO_BLOCO = 50
FPS = 60  # Frames per Second
BLACK = (0, 0, 0)
WHITE = (255,255,255)

grupos = {'all_sprites': pygame.sprite.Group(),
          'entregadores': pygame.sprite.Group(),
          'encomendas': pygame.sprite.Group(),
          'clientes': pygame.sprite.Group()}
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
screen = pygame.display.set_mode(((tamanho_mapa[1] * TAMANHO_BLOCO) + 2 * TAMANHO_BLOCO, tamanho_mapa[0] * TAMANHO_BLOCO))
clock = pygame.time.Clock()
t = 0

rodando = True
while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Controlar frame rate
    clock.tick(FPS)

    if t >= 0.5:
        grupos['all_sprites'].update()
        t = 0

    t += 1/FPS


    # Desenhar fundo
    screen.fill(BLACK)

    #Desenhar mapa
    for i in range(tamanho_mapa[0]):
        for j in range(tamanho_mapa[1]):
            pygame.draw.rect(screen, WHITE, pygame.Rect(j * TAMANHO_BLOCO, i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

    #Desenhar os obstaculos
    for pos in mapa[4]:
        pygame.draw.rect(screen, WHITE, pygame.Rect((pos[1] - 1) * TAMANHO_BLOCO, (pos[0] - 1) * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))

    num_clientes = len(grupos['clientes'])
    num_encomendas = len(grupos['encomendas'])
    num_entregadores = len(grupos['entregadores'])

    font = pygame.font.Font(None, 16)
    text_clientes = font.render("Clientes: {}".format(num_clientes), True, WHITE)
    text_encomendas = font.render("Encomendas: {}".format(num_encomendas), True, WHITE)
    text_entregadores = font.render("Entregadores: {}".format(num_entregadores), True, WHITE)
    
    screen.blit(text_clientes, ((tamanho_mapa[1] * TAMANHO_BLOCO) + 5, 15))
    screen.blit(text_encomendas, ((tamanho_mapa[1] * TAMANHO_BLOCO) + 5, 65))
    screen.blit(text_entregadores, ((tamanho_mapa[1] * TAMANHO_BLOCO) + 5, 115))

    if num_clientes == 0:
        imagem = pygame.transform.scale(pygame.image.load('assets/balloon-yesss.png'), (150, 81))
        screen.blit(imagem, ((tamanho_mapa[1] * TAMANHO_BLOCO) - 25, 145))

    grupos['all_sprites'].draw(screen)

    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()