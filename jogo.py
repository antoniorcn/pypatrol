import pygame
import pygex
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_SPACE
from pygex import Personagem, Spritesheet


em_jogo = True
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
clk = pygame.time.Clock()

sprite_sheet_tank = Spritesheet("./assets/image/tank.png", (70, 64), 6, 6)
tank_states = [
    { "state":"walking",
      "default":True,
      "frames":[18, 19, 20, 21, 22, 23, 24, 25, 26, 25, 24, 23, 22, 21, 20, 19]
    },
    {"state": "stop",
     "default": False,
     "frames": [0]
     },
    {"state": "death",
     "default": False,
     "frames": [36]
     }
]
tank = Personagem( (100, 100), sprite_sheet_tank, tank_states)


def calcular_regras():
    pass


def pintar():
    screen.fill((0, 0, 0))
    tank.draw(screen)
    pygame.display.update()


def interceptar_eventos():
    global em_jogo
    for ev in pygame.event.get():
        if ev.type == QUIT:
            em_jogo = False
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                tank.change_state("stop")


def main():
    print ("Iniciando o jogo")
    while em_jogo:
        calcular_regras()
        pintar()
        interceptar_eventos()
        clk.tick(10)
    print("Iniciando fim do jogo")


if __name__ == "__main__":
    main()