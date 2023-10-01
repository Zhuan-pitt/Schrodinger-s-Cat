import pygame

class Button():

    def __init__(self, x, y, width, height, buttonText='Button', command=lambda: print("press")):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.font = pygame.font.SysFont('calibri', 25)
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
        self.pressed = 1

    def process(self, surface):
        
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        surface.blit(self.buttonSurface, self.buttonRect)
