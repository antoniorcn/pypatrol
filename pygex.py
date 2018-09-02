import pygame
from pygame.locals import Rect


def top_point(center, size):
    top_x = center.x + round(size[0] / 2)
    top_y = center.y + round(size[1] / 2)
    return top_x, top_y


class Point(object):
    def __init__(self, *args):
        print(args)
        if type(args) == tuple:
            self.x = args[0][0]
            self.y = args[0][1]
        elif type(args) == int:
            self.x = args[0]
            self.y = args[1]
        elif type(args) == float:
            self.x = args[0]
            self.y = args[1]


class Spritesheet(object):
    def __init__(self, image_file, size, margin_left = 0, margin_top = 0, gap_x = 0, gap_y = 0):
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.gap_x = gap_x
        self.gap_y = gap_y
        self.image = pygame.image.load(image_file)
        self.quadro_size = size

    def get_image_by_id(self, id):
        num_quadros_x = round(self.image.get_rect().w / self.quadro_size[0])
        linha = int(id / num_quadros_x)
        coluna = id % num_quadros_x
        w = self.quadro_size[0]
        h = self.quadro_size[1]
        y = self.margin_top + (linha * (h + self.gap_y))
        x = self.margin_left + (coluna * (w + self.gap_x))
        rect = Rect((x, y), (w, h))
        return self.image.subsurface(rect)

    def get_rect(self):
        rect = Rect((0, 0), (self.quadro_size[0], self.quadro_size[1]))
        return rect


class ImageState(object):
    def __init__(self, states):
        self.frame_index = 0
        self.states = states
        self.current_state = self.get_default_state()

    def get_default_state(self):
        for st in self.states:
            if st['default'] == True:
                return st
        return self.states[0]

    def get_state_by_name(self, state_name):
        for st in self.states:
            if st['state'] == state_name:
                return st
        return None

    def next_frame_id(self):
        frame_id = self.current_state['frames'][self.frame_index]
        self.frame_index += 1
        if self.frame_index >= len(self.current_state['frames']):
            self.frame_index = 0
        return frame_id

    def change_state_by_name(self, state_name):
        temp_state = self.get_state_by_name(state_name)
        if temp_state != None:
            self.frame_index = 0
            self.current_state = temp_state


class Personagem(pygame.sprite.Sprite):

    def __init__(self, center, spritesheet, states):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.image_state = ImageState(states)
        self.rect = self.spritesheet.get_rect()
        self.center = Point(center)
        self.vel_x = 0
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = top_point(self.center, self.rect.size)

    def update(self):
        self.center.x += self.rect.vel_x
        self.center.y += self.rect.vel_y
        self.update_rect()

    def draw(self, surface):
        img = self.spritesheet.get_image_by_id(self.image_state.next_frame_id())
        surface.blit(img, self.rect.topleft)

    def change_state(self, new_state):
        self.image_state.change_state_by_name(new_state)


