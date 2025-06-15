import pgzrun
import random
from pygame import Rect

#estados do jogo
game_state = 'menu'  # Estado inicial do jogo
music_on = True  # Estado inicial da música
sounds_on = True  # Estado inicial dos sons

# Configurações da janela e da grade
WIDTH = 1000
HEIGHT = 600
CELL_SIZE = 64
blue = 150
blueforward = True
groundcolour = 0,0,139
TITLE = "Ninja vs Soldados"

#botões da tela de menu
start_button = Rect((400, 200), (200, 50))  # Botão de iniciar
options_button = Rect((400, 300), (200, 50))  # Botão de opções
exit_button = Rect((400, 400), (200, 50))  # Botão de sair
#botão para voltar ao menu da tela de Game Over
menu_button = Rect((400, 300), (200, 50))  # Botão de voltar ao menu
game_over = False  # Variável para controlar o estado de Game Over

#Herói ninja
frames = ['ninja_idle1', 'ninja_idle2']
ninja = Actor(frames[0], (500, 300))
ninja_x_velocity = 0
ninja_y_velocity = 0
gravity = 1
jumping = False
jumped = False
frame_index = 0 #indice do quadro atual
animation_counter = 0 #contador para controlar o delay da animação
animation_delay = 10 #delay de frames de delay entre as trocas de quadros
ninja_x_velocity = 0 #velocidade horizontal do ninja
ninja_y_velocity = 0 #velocidade vertical do ninja
ninja_gravity = 1 #gravidade do ninja
jumping = False #verifica se o ninja está pulando
ninja.vy = 0 #velocidade vertical do ninja

#Inimigo
enemy_x = [950,50,850,150,750,250,650,350,500]
enemy_y = [70,70,170,170,270,270,370,370,470]
d_xy = random.randint(0, 8)
frames_soldier = ['soldier-attack02-1', 'soldier-attack02-2', 'soldier-attack02-3', 'soldier-attack02-4', 'soldier-attack02-5', 'soldier-attack02-6']
soldier = Actor(frames_soldier[0], (enemy_x[d_xy], enemy_y[d_xy]))
diamond = Actor('diamond_s', (random.randint(100, 900), random.randint(100, 500))) #Diamante
points = 0
vida = 3 #Vida do jogador
#plataformas
platform1 = Rect((450, 500), (20, 0))
platform2 = Rect((380, 400), (20, 0))
platform3 = Rect((680, 400), (20, 0))
platform4 = Rect((200, 300), (20, 0))
platform5 = Rect((700, 300), (20, 0))
platform6 = Rect((100, 200), (20, 0))
plat61_x = 200
plat62_x = 700
platform61 = Rect((plat61_x, 200), (20, 0))  # Plataforma móvel
platform62 = Rect((plat62_x, 200), (20, 0))  # Plataforma móvel
platform7 = Rect((800, 200), (20, 0))
platform8 = Rect((0, 100), (20, 0))
platform9 = Rect((900, 100), (20, 0))
platformf = Rect((0, 600), (1000, 0))  # Plataforma fixa
platforms = [platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9, platform61, platform62, platformf] #listas para as plataformas
plat61left = True  # Direção inicial da plataforma móvel
plat62left = True  # Direção inicial da plataforma móvel

#musica
#sounds.ninja_music.play(-1)  # Toca a música de fundo em loop


def animate_sprite():
    global frame_index, animation_counter
    animation_counter += 1
    if animation_counter >= animation_delay:
        animation_counter = 0  # Reseta o contador
        frame_index = (frame_index + 1) % len(frames)  # Atualiza o índice do quadro
        ninja.image = frames[frame_index]
    #animação do soldado
    if animation_counter >= animation_delay:  # Animação do soldado
        animation_counter = 0  # Reseta o contador
        frame_index = (frame_index + 1) % len(frames_soldier)
        soldier.image = frames_soldier[frame_index]  # Atualiza a imagem do soldado

def draw():
    global platform61, platform62
    
    if game_over:
        screen.clear()
        screen.fill((0, 0, 0))  # Cor de fundo preta
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="red", owidth=1)  # Texto de Game Over  
    else:
        screen.fill((173, 216, blue))  # Cor de fundo
        screen.blit('skyline_large', (0, 0))  # Imagem do céu

        platform61 = Rect((plat61_x, 200), (100, 10))
        platform62 = Rect((plat62_x, 200), (100, 10))
        platforms[9] = platform61  # Atualiza a plataforma móvel
        platforms[10] = platform62  # Atualiza a plataforma móvel
        for i in platforms:
            screen.blit('platform1', i) # Desenha as plataformas
        ninja.draw()  # Desenha o herói ninja
        soldier.draw()  # Desenha o inimigo soldado
        diamond.draw()  # Desenha o diamante
        screen.draw.text(f'Pontos: {points}', (10, 10),shadow=(1,1), color='black', scolor = 'white', fontsize=30)  # Exibe os pontos
        screen.draw.text(f'Life: {vida} ', (350, 10), shadow=(1,1), color='black', scolor = 'white', fontsize=30)  # Título do jogo

def update():
    backgroundcolourfade()
    platform_mover()
    animate_sprite()
    ninja_move()
    game_over_screen()  # Verifica se o jogo acabou

def game_over_screen():
    global game_over
              
def ninja_move():
    global ninja_x_velocity, ninja_y_velocity, jumping, gravity, jumped, points, vida, soldier, d_xy
    
    if ninja_x_velocity == 0 and not jumped:
        ninja.image = 'jumper-1'
    #gravidade
    if collidecheck():
        gravity = 1
        ninja.y -= 1
    #if not collidecheck():
    if not collidecheck():
        ninja.y += gravity
        if gravity <= 20:
           gravity += 0.5

    #movimento horizontal
    if (keyboard.left):
        if (ninja.x > 40) and (ninja_x_velocity > -8):
            ninja_x_velocity -= 2
            ninja.image  = 'jumper-left'
            if (keyboard.left) and jumped:
                ninja.image = 'jumper-jleft'
    if (keyboard.right):
        if (ninja.x < 960) and (ninja_x_velocity < 8):
            ninja_x_velocity += 2
            ninja.image  = 'jumper-right'
            if (keyboard.right) and jumped:
                ninja.image = 'jumper-jright'
    ninja.x += ninja_x_velocity
    #velocidade horizontal
    if ninja_x_velocity > 0:
        ninja_x_velocity -= 1
    if ninja_x_velocity < 0:
        ninja_x_velocity += 1
        
    if ninja.x < 50 or ninja.x > 950:
        ninja_x_velocity = 0

    #pulo
    if (keyboard.up) and collidecheck():
        sounds.jump.play()  # Toca o som do pulo
        jumping = True
        jumped = True
        clock.schedule(jumpedrecently, 0.4)  # Agendar a função jumpedrecently para ser chamada após 0.4 segundos
        ninja.image  = 'jumper-up'
        ninja_y_velocity = 95
    if jumping and ninja_y_velocity > 25:
        ninja_y_velocity = ninja_y_velocity - ((100 - ninja_y_velocity) / 2)
        ninja.y -= ninja_y_velocity/3 #altura do pulo
    else:
        ninja_y_velocity = 0
        jumping = False
    
    #colisão com o diamante
    if ninja.colliderect(diamond):
        points += 1
        sounds.gem.play()  # Toca o som do diamante
        old_d_xy = d_xy
        d_xy = random.randint(0, 8)
        while d_xy == old_d_xy:  # Garante que o novo índice seja diferente do antigo
            d_xy = random.randint(0, 8)
        diamond.x = random.randint(100, 900)
        diamond.y = random.randint(100, 500)
    
    #colisão com o soldado
    if ninja.colliderect(soldier):
        ninja.image = 'jumper-fall'
        vida -= 1
        old_d_xy = d_xy
        d_xy = random.randint(0, 8)
        while d_xy == old_d_xy:
           d_xy = random.randint(0, 8)
        soldier.x = random.randint(100, 900)
        soldier.y = random.randint(100, 500)    
        if vida <= 0:
            game_over = True  # Define o estado de Game Over se a vida chegar a zero
            
def platform_mover():
    global plat61_x, plat62_x, plat61left, plat62left
    #plataforma esquerda
    if plat61left:
        plat61_x += 2
        if plat61_x >= 400:
            plat61left = False
        if ninja.colliderect(platform61):
            ninja.x += 2
    else:
        plat61_x -= 2
        if plat61_x <= 200:
            plat61left = True
        if ninja.colliderect(platform61):
            ninja.x -= 2
    #plataforma direita
    if plat62left:
        plat62_x -= 2
        if plat62_x <= 400:
            plat62left = False
        if ninja.colliderect(platform62):
            ninja.x -= 2
    else:
        plat62_x += 2
        if plat62_x >= 700:
            plat62left = True
        if ninja.colliderect(platform62):
            ninja.x += 2
            
def collidecheck():
    collide = False
    for i in platforms:
        if ninja.colliderect(i):
            collide = True
    return collide

def jumpedrecently():
    global jumping
    jumped = False

def backgroundcolourfade():
    global blue, blueforward
    if blue < 255 and blueforward:
        blue += 1
    else:
        blueforward = False
    if blue > 130 and not blueforward:
        blue -= 1
    else:
        blueforward = True


