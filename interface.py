import pygame
import json
import threading
from main import Solucao

class Deliveryman(pygame.sprite.Sprite):

    def __init__(self, x, y, grupos) -> None:
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
            if len(mapa[2]) != 0 and len(mapa[3]) != 0:
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
TAMANHO_BLOCO = 26
FPS = 60  # Frames per Second
BLACK = (0, 0, 0)
WHITE = (255,255,255)
VERMELHO = (255,0,0)

font = pygame.font.Font(None, 36)
text_novo = font.render("criar novo mapa", True, WHITE)
text_existente = font.render("usar mapa existente", True, WHITE)
criar = False
screen = pygame.display.set_mode(((text_existente.get_width()), text_novo.get_height() + text_existente.get_height()))

menu = True
texto_menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if text_novo.get_rect(x=0, y=0).collidepoint(mouse_x, mouse_y):
                criar = True
                texto_menu = False
            elif text_existente.get_rect(x=0, y=text_novo.get_height()).collidepoint(mouse_x, mouse_y):
                menu = False

    screen.fill(BLACK)
    if texto_menu:
        screen.blit(text_novo, (0, 0))
        screen.blit(text_existente, (0, text_novo.get_height()))

    pygame.display.update()

    if criar:
        linhas = 10
        colunas = 10
        screen = pygame.display.set_mode((colunas * TAMANHO_BLOCO + TAMANHO_BLOCO, linhas * TAMANHO_BLOCO))
        criando = True
        momento = 1
        novo_mapa = [[linhas, colunas]]
        entregador = []
        clientes = []
        encomendas = []
        obstaculos = []
        contador_cliente = 0
        while criando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    criando = False
                    menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    proximo_rect = pygame.Rect(colunas * TAMANHO_BLOCO, 0, proximo.get_width(), proximo.get_height())
                    if proximo_rect.collidepoint(mouse_x, mouse_y):
                        momento = 5
                    elif image_entregador.get_rect(x=colunas * TAMANHO_BLOCO, y=proximo.get_height()).collidepoint(mouse_x, mouse_y):
                        momento = 4
                    elif image_cliente.get_rect(x=colunas * TAMANHO_BLOCO, y=2 * TAMANHO_BLOCO).collidepoint(mouse_x, mouse_y):
                        momento = 3
                    elif image_encomenda.get_rect(x=colunas * TAMANHO_BLOCO, y=3 * TAMANHO_BLOCO).collidepoint(mouse_x, mouse_y):
                        momento = 2
                    elif pygame.rect.Rect(colunas * TAMANHO_BLOCO, 4 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO).collidepoint(mouse_x, mouse_y):
                        momento = 1

                    if momento >= 5:
                        novo_mapa.append(entregador)
                        novo_mapa.append(clientes)
                        novo_mapa.append(encomendas)
                        novo_mapa.append(obstaculos)
                        criando = False
                        menu = False

                    x = mouse_x // TAMANHO_BLOCO
                    y = mouse_y // TAMANHO_BLOCO
                    if mouse_x < colunas * TAMANHO_BLOCO and mouse_y < linhas * TAMANHO_BLOCO:
                        if momento == 1:
                            pygame.draw.rect(screen, WHITE, pygame.Rect(x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
                            obstaculos.append([y+1, x+1])
                        elif momento == 2:
                            image = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
                            screen.blit(image, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO))
                            encomendas.append([y+1, x+1])
                        elif momento == 3:
                            image = pygame.transform.scale(pygame.image.load('assets/pessoa.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
                            screen.blit(image, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO))
                            clientes.append([[y+1, x+1], contador_cliente])
                            contador_cliente += 1
                        elif momento == 4:
                            image = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
                            screen.blit(image, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO))
                            entregador.append(y+1)
                            entregador.append(x+1)

            # Draw the grid for map creation
            for i in range(linhas):
                for j in range(colunas):
                    pygame.draw.rect(screen, WHITE, pygame.Rect(j * TAMANHO_BLOCO, i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)
            
            font = pygame.font.Font(None, TAMANHO_BLOCO)
            text = font.render("", True, WHITE)

            proximo = font.render("OK", True, WHITE)
            screen.blit(proximo, (colunas * TAMANHO_BLOCO, 0))
            
            image_entregador = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
            screen.blit(image_entregador, (colunas * TAMANHO_BLOCO, proximo.get_height()))
            pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, proximo.get_height(), TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
            
            image_cliente = pygame.transform.scale(pygame.image.load('assets/pessoa.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
            screen.blit(image_cliente, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO))
            pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
            
            image_encomenda = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
            screen.blit(image_encomenda, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO))
            pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)

            pygame.draw.rect(screen, WHITE, (colunas * TAMANHO_BLOCO, 4 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
            pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, 4 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 2)

            if momento == 1:
                pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, 4 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
            elif momento == 2:
                pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO, image_encomenda.get_width(), image_encomenda.get_height()), 3)
            elif momento == 3:
                pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO, image_cliente.get_width(), image_cliente.get_height()), 3)
            elif momento == 4:
                pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, proximo.get_height(), image_entregador.get_width(), image_entregador.get_height()), 3)
            

            pygame.display.update()

grupos = {'all_sprites': pygame.sprite.Group(),
          'entregadores': pygame.sprite.Group(),
          'encomendas': pygame.sprite.Group(),
          'clientes': pygame.sprite.Group()}

if not criar:
    nome_mapa = 'Mapa1.json'

    with open(nome_mapa, 'r') as arquivo:
        mapa = json.load(arquivo)
else:
    mapa = novo_mapa

tamanho_mapa = mapa[0]

#x é a coluna e y é a linha
entregador = Deliveryman(mapa[1][1] , mapa[1][0], grupos)

for cliente in mapa[2]:
    Cliente(cliente[0], grupos)

for encomenda in mapa[3]:
    Encomenda(encomenda, grupos)

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode(((tamanho_mapa[1] * TAMANHO_BLOCO) + TAMANHO_BLOCO, tamanho_mapa[0] * TAMANHO_BLOCO))
clock = pygame.time.Clock()
t = 0
contador_cliente = len(mapa[2])
momento = 0
colunas = tamanho_mapa[1]
linhas = tamanho_mapa[0]
# entregador = []
clientes = []
encomendas = []
image_encomenda = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
image_cliente = pygame.transform.scale(pygame.image.load('assets/pessoa.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
image_entregador = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))

rodando = True
while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            proximo_rect = pygame.Rect(colunas * TAMANHO_BLOCO, 0, proximo.get_width(), proximo.get_height())
            if proximo_rect.collidepoint(mouse_x, mouse_y):
                momento = 5
            elif image_entregador.get_rect(x=colunas * TAMANHO_BLOCO, y=proximo.get_height()).collidepoint(mouse_x, mouse_y):
                momento = 4
            elif image_cliente.get_rect(x=colunas * TAMANHO_BLOCO, y=2 * TAMANHO_BLOCO).collidepoint(mouse_x, mouse_y):
                momento = 3
            elif image_encomenda.get_rect(x=colunas * TAMANHO_BLOCO, y=3 * TAMANHO_BLOCO).collidepoint(mouse_x, mouse_y):
                momento = 2

        x = mouse_x // TAMANHO_BLOCO
        y = mouse_y // TAMANHO_BLOCO
        if mouse_x < tamanho_mapa[1] * TAMANHO_BLOCO and mouse_y < tamanho_mapa[0] * TAMANHO_BLOCO:
            if momento == 2:
                image = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
                encomendas.append([y+1, x+1])
                Encomenda([y+1, x+1], grupos)
                momento = 0
            elif momento == 3:
                Cliente([y+1, x+1], grupos)
                clientes.append([[y+1, x+1], contador_cliente])
                contador_cliente += 1
                momento = 0
            # elif momento == 4:
            #     image = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
            #     screen.blit(image, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO))
            #     mapa[]

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

    font = pygame.font.Font(None, TAMANHO_BLOCO)
    text = font.render("", True, WHITE)

    proximo = font.render("OK", True, WHITE)
    screen.blit(proximo, (colunas * TAMANHO_BLOCO, 0))
    
    # image_entregador = pygame.transform.scale(pygame.image.load('assets/entregador.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
    # screen.blit(image_entregador, (colunas * TAMANHO_BLOCO, proximo.get_height()))
    # pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, proximo.get_height(), TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
    
    image_cliente = pygame.transform.scale(pygame.image.load('assets/pessoa.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
    screen.blit(image_cliente, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO))
    pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
    
    image_encomenda = pygame.transform.scale(pygame.image.load('assets/encomenda.webp'), (TAMANHO_BLOCO,TAMANHO_BLOCO))
    screen.blit(image_encomenda, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO))
    pygame.draw.rect(screen, BLACK, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)

    if momento == 2:
        pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, 3 * TAMANHO_BLOCO, image_encomenda.get_width(), image_encomenda.get_height()), 3)
    elif momento == 3:
        pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO, image_cliente.get_width(), image_cliente.get_height()), 3)
    # elif momento == 4:
    #     pygame.draw.rect(screen, VERMELHO, (colunas * TAMANHO_BLOCO, proximo.get_height(), image_entregador.get_width(), image_entregador.get_height()), 3)
    if momento == 5:
        # novo_mapa.append(entregador)
        for cliente in clientes:
            mapa[2].append(cliente)
        for encomenda in encomendas:
            mapa[3].append(encomenda)
        momento = 0
        clientes = []
        encomendas = []

    grupos['all_sprites'].draw(screen)

    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()