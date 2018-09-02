import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
from pygex import Personagem, Spritesheet
import parallax
import os

em_jogo = True
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
clk = pygame.time.Clock()
backgrounds = []

sprite_sheet_runner = Spritesheet("./assets/image/runner.png", (150, 150), 0, 0)
''' tank_states = [
    { "state":"walking_up",
      "default":False,
      "frames":[1, 2, 3, 4, 5, 6, 7, 8]
    },
    {"state": "walking_left",
     "default": False,
     "frames": [10, 11, 12, 13, 14, 15, 16, 17]
     },
    {"state": "walking_down",
     "default": False,
     "frames": [19, 20, 21, 22, 23, 24, 25, 26]
     },
    {"state": "walking_right",
     "default": True,
     "frames": [28, 29, 30, 31, 32, 33, 34, 35]
     },
    {"state": "stop_up",
     "default": False,
     "frames": [0]
     },
    {"state": "stop_left",
     "default": False,
     "frames": [9]
     },
    {"state": "stop_down",
     "default": False,
     "frames": [18]
     },
    {"state": "stop_right",
     "default": False,
     "frames": [27]
     },
    {"state": "death",
     "default": False,
     "frames": [0]
     }
]'''

# tank = Personagem( (100, 250), sprite_sheet_tank, tank_states)

runner_states = [
    {   "state": "running",
        "default": True,
        "frames": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
                   #22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    }
]

runner = Personagem( (100, 150), sprite_sheet_runner, runner_states)


def calcular_regras(time_passed_seconds):
    for parallax in backgrounds:
        parallax.process(time_passed_seconds)


def pintar():
    screen.fill((0, 0, 0))
    backgrounds[0].render(screen)
    backgrounds[1].render(screen)
    backgrounds[2].render(screen)
    backgrounds[3].render(screen)
    backgrounds[4].render(screen)
    runner.draw(screen)
    backgrounds[5].render(screen)
    pygame.display.update()


def interceptar_eventos():
    global em_jogo
    for ev in pygame.event.get():
        if ev.type == QUIT:
            em_jogo = False
'''            
        elif ev.type == KEYDOWN:
            if ev.key == K_DOWN:
                runner.change_state("walking_down")
            elif ev.key == K_UP:
                runner.change_state("walking_up")
            elif ev.key == K_LEFT:
                runner.change_state("walking_left")
            elif ev.key == K_RIGHT:
                runner.change_state("walking_right")
        elif ev.type == KEYUP:
            if ev.key == K_DOWN:
                runner.change_state("stop_down")
            elif ev.key == K_UP:
                runner.change_state("stop_up")
            elif ev.key == K_LEFT:
                runner.change_state("stop_left")
            elif ev.key == K_RIGHT:
                runner.change_state("stop_right")
'''


def load_sliced_sprites(w, h, filename):
    '''
    Specs :
    	Master can be any height.
    	Sprites frames width must be the same width
    	Master width must be len(frames)*frame.width
    '''
    images = []
    master_image = pygame.image.load(os.path.join('', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in range(int(master_width/w)):
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images


def load_parallax():
    parallax_1 	= load_sliced_sprites(800, 200, 'parallax-1-800x200.png')
    parallax_2 	= load_sliced_sprites(800, 120, 'parallax-2-800x120.png')
    parallax_3 	= load_sliced_sprites(800, 200, 'parallax-3-800x200.png')
    parallax_4 	= load_sliced_sprites(800, 200, 'parallax-4-800x200.png')
    parallax_5 	= load_sliced_sprites(1600, 400, 'parallax-5-1600x400.png')
    parallax_6 = load_sliced_sprites(1600, 400, 'parallax-6-1600x400.png')

    prlx1 = parallax.Parallax(parallax_1, 60)
    prlx1.speed = 10.
    prlx1.location = (0, 0)
    prlx1.destination = parallax.Vector2(*(-parallax_1[0].get_rect().w, 0))
    backgrounds.append(prlx1)

    prlx2 = parallax.Parallax(parallax_2, 60)
    prlx2.speed = 40.0
    prlx2.location = (0, 110)
    prlx2.destination = parallax.Vector2(*(-parallax_2[0].get_rect().w, 110))
    backgrounds.append(prlx2)

    prlx3 = parallax.Parallax(parallax_3, 60)
    prlx3.speed = 80.0
    prlx3.location = (0, 60)
    prlx3.destination = parallax.Vector2(*(-parallax_3[0].get_rect().w, 60))
    backgrounds.append(prlx3)

    prlx4 = parallax.Parallax(parallax_4, 60)
    prlx4.speed = 120.
    prlx4.location = (0, 90)
    prlx4.destination = parallax.Vector2(*(-parallax_4[0].get_rect().w, 90))
    backgrounds.append(prlx4)

    prlx5 = parallax.Parallax(parallax_5, 60)
    prlx5.speed = 900.
    prlx5.location = (0, 0)
    prlx5.destination = parallax.Vector2(*(-parallax_5[0].get_rect().w, 0))
    backgrounds.append(prlx5)

    prlx6 = parallax.Parallax(parallax_6, 60)
    prlx6.speed = 900.
    prlx6.location = (0, 0)
    prlx6.destination = parallax.Vector2(*(-parallax_6[0].get_rect().w, 0))
    backgrounds.append(prlx6)


def main():
    print ("Iniciando o jogo")
    load_parallax()
    while em_jogo:
        time_passed = clk.tick(10)
        time_passed_seconds = time_passed / 1000.0
        calcular_regras(time_passed_seconds)
        pintar()
        interceptar_eventos()
    print("Iniciando fim do jogo")


if __name__ == "__main__":
    main()