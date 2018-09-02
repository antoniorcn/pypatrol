import pygame
import Box2D as b2

em_jogo = True
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
clk = pygame.time.Clock()
FPS = 30.0
PPM = 800 / 100

def draw(screen, corpo):
    global PPM
    for fix in corpo.fixtures:
        if fix.shape.type == b2.b2Shape.e_circle:
            pos = body.position
            x = int(pos[0] * PPM)
            y = int(pos[1] * PPM)
            rad = int(fix.shape.radius * PPM)
            pygame.draw.circle(screen, (255, 255, 0), (x, y), rad)
        elif fix.shape.type == b2.b2Shape.e_polygon:
            pontos = []
            for v in fix.shape.vertices:
                v = (corpo.transform * v)
                vertice = [v[0] * PPM, screen.get_height() - (v[1] * PPM)]
                pontos.append(vertice)
            pygame.draw.polygon(screen, corpo.userData, pontos, 0)

def by_center(imagem, pos):
    r = imagem.get_rect()
    top_x = pos[0] - int(r.w / 2)
    top_y = pos[1] - int(r.h / 2)
    return top_x, top_y

cenario = b2.b2World((0.0, -9.8), True)

bodyDef = b2.b2BodyDef()
bodyDef.angle = 5 * 3.14 / 180.0
bodyDef.position = (10, 80)
bodyDef.type = b2.b2_dynamicBody

body = cenario.CreateBody(bodyDef)

fixDef = b2.b2FixtureDef()
fixDef.shape = b2.b2PolygonShape(box=(1, 2))
fixDef.restitution = 0.8
fixDef.friction = 0.5
fixDef.density = 10


pisoDef = b2.b2BodyDef()
pisoDef.angle = 0
pisoDef.position = (0, 1)
pisoDef.type = b2.b2_staticBody

piso = cenario.CreateBody(pisoDef)

fixPisoDef = b2.b2FixtureDef()
fixPisoDef.shape = b2.b2PolygonShape(box=(100, 0.5))
fixPisoDef.restitution = 0.6
fixPisoDef.friction = 0.5
fixPisoDef.density = 100

fixture = body.CreateFixture(fixDef)
fixturePiso = piso.CreateFixture(fixPisoDef)
body.userData = (255, 255, 0)
piso.userData = (255, 255, 0)

while True:
    cenario.Step(1.0/FPS, 8, 3)
    screen.fill((0, 0, 0))
    for contato in cenario.contacts:
        corpoA = contato.fixtureA.body
        corpoB = contato.fixtureB.body
        corpoA.userData = (255, 0, 0)
        corpoB.userData = (255, 0, 0)
        #print(corpoA, corpoB)

    draw(screen, body)
    draw(screen, piso)
    pygame.display.update()
    clk.tick(FPS * 2)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
