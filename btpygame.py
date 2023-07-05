import pygame

class pygameimage():

    def __init__(self, image, pos):
        self.image = image
        self.pos = pos
        self.size = image.get_size()

    def gethitbox(self):
        return (self.pos[0], self.pos[0] + self.size[0], self.pos[1], self.pos[1] + self.size[1])

class pygamebutton():
    def __init__(self, image, image_t, pos):
        assert image.get_size() == image_t.get_size()
        self.away = pygameimage(image, pos)
        self.target = pygameimage(image_t, pos)
        self.pos = pos
        self.size = image.get_size()

    def display(self, screen):
        if not collide(self.away, pygame.mouse.get_pos()):
            screen.blit(self.away.image, self.away.pos)
        else:
            screen.blit(self.target.image, self.target.pos)

    def gethitbox(self):
        return (self.pos[0], self.pos[0] + self.size[0], self.pos[1], self.pos[1] + self.size[1])

    def setpos(self, newpos):
        self.pos = newpos
        self.target.pos = newpos
        self.away.pos = newpos

def collide(image, mouse):
    """
    Check if the mouse cursor collide with an image.
    """
    hitbox = image.gethitbox()
    return hitbox[0] <= mouse[0] <= hitbox[1] and hitbox[2] <= mouse[1] <= hitbox[3]

def showtext(screen, text, font, size, pos, color, align):
    """
    Show text on the screen
    """
    final_font = pygame.font.Font(font, size)
    text_shown = final_font.render(text, True, color)
    text_rect = text_shown.get_rect()
    if align.lower() == "center":
        text_rect.center = pos
    elif align.lower() == "midleft":
        text_rect.midleft = pos
    elif align.lower() == "midright":
        text_rect.midright = pos
    elif align.lower() == "topleft":
        text_rect.topleft = pos
    elif align.lower() == "topright":
        text_rect.topright = pos
    elif align.lower() == "bottomleft":
        text_rect.bottomleft = pos
    else:
        text_rect.bottomright = pos
    screen.blit(text_shown, text_rect)
    return final_font.size(text)