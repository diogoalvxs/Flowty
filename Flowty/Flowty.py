import pygame
import sys
from button import Button  # Importa a classe Button de um módulo chamado "button"
import os
import time

# Define o nome do arquivo de configuração
filename = "level.txt"

# Verifica se o arquivo não existe e o cria com valores padrão
if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("1\n0")

# Lê o conteúdo do arquivo de configuração
with open(filename, "r") as f:
    level, xp = map(int, f.read().split())

# Inicializa o módulo Pygame
pygame.init()

# Define as dimensões da tela
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flowty")

# Carrega o ícone da janela e define o ícone
icon = pygame.image.load("assets/tomato.png")
pygame.display.set_icon(icon)

# Inicializa o relógio do Pygame
CLOCK = pygame.time.Clock()

# Carrega as imagens de fundo e botão
BACKDROP = pygame.image.load("assets/backdrop.png")
WHITE_BUTTON = pygame.image.load("assets/button.png")

# Carrega a fonte para o temporizador e cria o texto inicial
FONT = pygame.font.Font("assets/digital-7.ttf", 120)
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))

# Cria botões para diferentes períodos de tempo
POMODORO_BUTTON = Button(None, (WIDTH/2-150, HEIGHT/2-140), 120, 30, "Pomodoro", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#f1f1f1", "#c0c0c0")
SHORT_BREAK_BUTTON = Button(None, (WIDTH/2, HEIGHT/2-140), 120, 30, "Short Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#f1f1f1", "#c0c0c0")
LONG_BREAK_BUTTON = Button(None, (WIDTH/2+150, HEIGHT/2-140), 120, 30, "Long Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#f1f1f1", "#c0c0c0")

# Define a duração dos diferentes períodos de tempo em segundos
POMODORO_LENGTH = 1500  # 25 minutos em segundos
SHORT_BREAK_LENGTH = 300  # 5 minutos em segundos
LONG_BREAK_LENGTH = 900  # 15 minutos em segundos

# Inicializa o contador de segundos
current_seconds = POMODORO_LENGTH

# Define um temporizador que gera um evento a cada segundo
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Define a variável "started" para controlar se o temporizador está em execução
started = False

# Carrega a fonte para exibir informações de nível e experiência
font = pygame.font.Font('assets/ArialRoundedMTBold.ttf', 32)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Salva o nível e experiência no arquivo de configuração antes de sair
            with open(filename, "w") as f:
                f.write(str(level) + "\n" + str(xp))
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se os botões foram clicados e atualiza o estado do temporizador
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                if started:
                    started = False
                    START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#181818", "#0078d4")
                else:
                    started = True
                    START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "STOP", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#181818", "#0078d4")

            # Define a duração do temporizador com base no botão clicado
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = POMODORO_LENGTH
                started = False
            
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = SHORT_BREAK_LENGTH
                started = False

            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = LONG_BREAK_LENGTH
                started = False
                    
        if event.type == pygame.USEREVENT and started:
            # Reduz o contador de segundos a cada evento de temporizador, se o temporizador estiver em execução
            current_seconds -= 1

    # Preenche a tela com uma cor de fundo
    SCREEN.fill("#181818")

    # Exibe o plano de fundo
    SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH/2, HEIGHT/2)))

    # Atualiza os botões na tela
    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())

    # Atualiza o texto do temporizador com os minutos e segundos restantes
    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
        timer_text = FONT.render(f"{display_minutes:02d}:{display_seconds:02d}", True, "white") 
        SCREEN.blit(timer_text, timer_text_rect)

    # Verifica se o temporizador chegou a zero
    if display_minutes == 0 and display_seconds == 0:
        time.sleep(1)  # Aguarda 1 segundo antes de reiniciar o temporizador
        current_seconds = POMODORO_LENGTH
        xp += 10  # Adiciona 10 pontos de experiência ao completar um ciclo
        started = False
        START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#181818", "#0078d4")

    # Verifica se a experiência atingiu o limite para subir de nível
    if xp >= 100:
        level += 1
        xp -= 100

    # Renderiza e exibe informações de nível e experiência na tela
    text = font.render(f"Level: {level}     XP: {xp}", True, ("#f1f1f1"))
    SCREEN.blit(text, (600, 10))

    # Atualiza a tela
    pygame.display.update()
