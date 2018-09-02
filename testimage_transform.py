import pygame

em_jogo = True
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
clk = pygame.time.Clock()

def by_center(imagem, pos):
    r = imagem.get_rect()
    top_x = pos[0] - int(r.w / 2)
    top_y = pos[1] - int(r.h / 2)
    return top_x, top_y

imagem = pygame.image.load("./assets/image/pac.png")
angulo = 0
while True:
    screen.fill((0,0,0))
    imagem_rot = pygame.transform.rotate(imagem, angulo)
    top_left = by_center(imagem_rot, (400, 300))
    screen.blit(imagem_rot, top_left)
    #screen.blit(imagem_rot, (100, 100))
    r = imagem_rot.get_rect()
    r.x = top_left[0]
    r.y = top_left[1]
    pygame.draw.rect(screen, (255, 0, 0), r, 3)
    pygame.display.update()
    clk.tick(20)
    angulo += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

