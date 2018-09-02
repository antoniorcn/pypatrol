'''
Created on 12/05/2014

@author: Aluno
'''
import os
import Box2D as b2
import pygame
from pygame.locals import QUIT
from math import pi
from pygame.constants import KEYDOWN, K_SPACE, KEYUP, MOUSEBUTTONDOWN, \
    MOUSEBUTTONUP, MOUSEMOTION
import math

FPS = 30.0
PPM = 16.0

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

gatoImg = pygame.image.load(os.path.join('', 'Gato.png')).convert_alpha()
muroImg = pygame.image.load(os.path.join('', 'muro.jpg')).convert_alpha()
pisoImg = pygame.image.load(os.path.join('', 'ground.png')).convert_alpha()
estilingImg = pygame.image.load(os.path.join('', 'Estilingue.png')).convert_alpha()

gato = {"pos": [5.0, 6.0], "angle": 0.0, "type": b2.b2_dynamicBody, "shape": b2.b2PolygonShape(box=[4.0, 2.0]),
        "density": 15.0, "restitution": 0.5, "friction": 0.5, "image": gatoImg, "scale": [10.0, 5.0]}

parede1 = {"pos": [40.0, 3.5], "angle": 0.0, "type": b2.b2_dynamicBody, "shape": b2.b2PolygonShape(box=[1.0, 3.0]),
           "density": 15.0, "restitution": 0.5, "friction": 0.5, "image": muroImg, "scale": [10.0, 5.0]}
bloco1 = {"pos": [40.0, 9.0], "angle": 0.0, "type": b2.b2_dynamicBody, "shape": b2.b2PolygonShape(box=[2.0, 2.0]),
          "density": 15.0, "restitution": 0.5, "friction": 0.5, "image": muroImg, "scale": [10.0, 5.0]}

piso = {"pos": [25.0, 0.5], "angle": 0.0, "type": b2.b2_staticBody, "shape": b2.b2PolygonShape(box=[25.0, 0.5]),
        "density": 100.0, "restitution": 0.2, "friction": 0.3, "image": pisoImg, "scale": [10.0, 5.0]}


def get_position_from_center(center_pos, size):
    (center_x, center_y) = center_pos
    (comprimento, altura) = size
    pos_x = (center_x) - (comprimento / 2)
    pos_y = (center_y) - (altura / 2)
    return (int(pos_x), int(pos_y))


def geraBody(world, obj):
    bodyDef = b2.b2BodyDef()
    bodyDef.position = obj["pos"]
    bodyDef.type = obj["type"]
    bodyDef.angle = obj["angle"]

    body = world.CreateBody(bodyDef)

    fixDef = b2.b2FixtureDef()
    fixDef.shape = obj["shape"]
    fixDef.restitution = obj["restitution"]
    fixDef.friction = obj["friction"]
    fixDef.density = obj["density"]
    body.CreateFixture(fixDef)

    body.userData = obj

    return body


g = b2.b2Vec2(0.0, -9.8)
mundo = b2.b2World(g, True)
gatoBody = geraBody(mundo, gato)
parede1Body = geraBody(mundo, parede1)
bloco1Body = geraBody(mundo, bloco1)
pisoBody = geraBody(mundo, piso)


def distancia(ponto1, ponto2):
    dist = math.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)
    return dist


def drawPolygon(scr, obj, ppm):
    pontos = []
    shape = obj.fixtures[0].shape
    for v in shape.vertices:
        v = (obj.transform * v)
        vertice = [v[0] * ppm, scr.get_height() - (v[1] * ppm)]
        pontos.append(vertice)

    # print pontos
    # print pontos
    pygame.draw.polygon(scr, (255, 0, 0), pontos, 2)


def draw(scr, obj, ppm):
    drawPolygon(scr, obj, ppm)
    if 'image' in obj.userData:
        image = obj.userData["image"]
        image_scale = obj.userData["scale"]
        image_transformed = pygame.transform.scale(image,
                                                   (int(image_scale[0] * ppm), int(image_scale[1] * ppm)))
        image_transformed = pygame.transform.rotate(image_transformed, (obj.transform.angle * 180 / pi))
        #        if ( int(body.transform.angle) != 0):
        #            imagem = pygame.transform.rotate(imagem, (body.transform.angle * math.pi / 180)).copy()
        pos = obj.position.copy()
        pos[0] = (pos[0]) * ppm
        pos[1] = scr.get_height() - (pos[1] * ppm)
        #         pos = (int(pos[0] * PPM), int(pos[1] * PPM))
        size = (image_transformed.get_width(), image_transformed.get_height())
        screen.blit(image_transformed, get_position_from_center(pos, size))


clk = pygame.time.Clock()
incForca = 0
forca = 1
disparo = False
initialPos = (200, 400)
mousePos = initialPos

while (True):
    screen.fill((0, 0, 0))
    draw(screen, gatoBody, PPM)
    draw(screen, pisoBody, PPM)
    draw(screen, parede1Body, PPM)
    draw(screen, bloco1Body, PPM)
    pygame.display.update()
    clk.tick(30)
    if (disparo == False):
        gatoBody.position = [mousePos[0] / PPM, (screen.get_height() - mousePos[1]) / PPM]
        gatoBody.linearVelocity = (0, 0)
        gatoBody.angularVelocity = 0
        gatoBody.awake = True

    mundo.Step(1.0 / FPS, 8, 3)

    for e in pygame.event.get():
        if (e.type == QUIT):
            exit()
        elif (e.type == MOUSEBUTTONDOWN):
            if (e.button == 1):
                mousePos = e.pos

        elif (e.type == MOUSEMOTION):
            if (e.buttons[0] == 1):
                mousePos = e.pos
                forca = distancia(initialPos, mousePos)



        elif (e.type == MOUSEBUTTONUP):
            if (e.button == 1):
                print
                forca
                gatoBody.ApplyForce((gatoBody.fixtures[0].density * forca * 1000, 0), gatoBody.position, True)
                disparo = True