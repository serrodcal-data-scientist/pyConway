import pygame
import numpy as np
import time

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((height,width))

bg = 25, 25, 25
# Pintamos el fondo con el color elegido
screen.fill(bg)

# Número de celdas
rows, cols = 50, 50
# Dimensiones de la celda
dimCW = width / cols
dimCH = height / rows

# Estado de las celdas: Vivas = 1; Muertas = 0
gameState = np.zeros((rows, cols))

# Autómata palo
#gameState[5, 3] = 1
#gameState[5, 4] = 1
#gameState[5, 5] = 1

# Autómata nave
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecución del juego
pauseExect = False

# Bucle de ejecución
while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y ratón
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se presiona el ratón
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celY, celX] = not mouseClick[2]

    for x in range(rows):
        for y in range(cols):

            if not pauseExect:

                # Calculamos el número de vecinos cercanos (módulo para seguir regla del toróide)
                n_neigh = gameState[(x - 1) % rows, (y - 1) % cols ] + \
                          gameState[(x)     % rows, (y - 1) % cols] + \
                          gameState[(x + 1) % rows, (y - 1) % cols] + \
                          gameState[(x - 1) % rows, (y)     % cols] + \
                          gameState[(x + 1) % rows, (y)     % cols] + \
                          gameState[(x - 1) % rows, (y + 1) % cols] + \
                          gameState[(x)     % rows, (y + 1) % cols] + \
                          gameState[(x + 1) % rows, (y + 1) % cols]

                # Regla 1: Una célula muerta con exáctamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creamos el polígono de cada
            poly = [((y)   * dimCW, x * dimCH),
                    ((y+1) * dimCW, x * dimCH),
                    ((y+1) * dimCW, (x+1) * dimCH),
                    ((y)   * dimCW, (x+1) * dimCH)]

            # Y dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla
    pygame.display.flip()
