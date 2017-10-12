
import pygame, string
from pygame.locals import *
from constants import *

pygame.init()

#Printing Text on screen code
#
#

def print_text (fontname, fontsize, string, textcolor, backcolor, centerX, centerY):
    fontObj = pygame.font.Font(fontname, fontsize)
    if backcolor != None:
        textSurfaceObj = fontObj.render(string, True, textcolor, backcolor)
    else:
        textSurfaceObj = fontObj.render(string, True, textcolor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (centerX, centerY)
    return textSurfaceObj, textRectObj

#Button Code
#
#

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        self.text = text
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, True, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def create_button_image(self, surface, image, x, y, length, height, text="", text_size=0, text_color=None, text_font = "freesansbold.ttf"):

        image = pygame.transform.scale(image, (length,height))
        surface.blit(image, (x, y))
        if text !="":
            surface = self.write_text_image(surface, text, text_color, text_size, text_font, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        self.text = text
        return surface

    def write_text_image(self, surface, text, text_color, font_size, text_font, length, height, x, y):

        myFont = pygame.font.Font(text_font, font_size)
        myText = myFont.render(text, True, text_color)
        textRectObj = myText.get_rect()
        textRectObj.center = (x + length/2, y + height/2)
        surface.blit(myText, textRectObj)
        # surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        # print  self.text + " button was pressed!"
                        return True
        return False

    def hover(self, mouse):
        return self.rect.collidepoint(mouse)



#TextBox Code
#
#
ACCEPTED = string.ascii_letters+string.digits+string.punctuation+" "

class TextBox(object):
    def __init__(self,rect,**kwargs):
        self.rect = pygame.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)

    def get_text(self):
        return self.final

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pygame.Color("white"),
                    "font_color" : pygame.Color("black"),
                    "outline_color" : pygame.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pygame.Color("black"),
                    "font" : pygame.font.Font('freesansbold.ttf', 3*self.rect.height/4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in ACCEPTED:
                self.buffer.append(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pygame.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pygame.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw(self,surface):
        self.update()
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))


class Slider():
    def __init__(self,screen, (posX,posY),(minVal,maxVal)):
        self.surRect = Rect(0,0,0,0)

        self.minVal = minVal
        self.maxVal = maxVal
        self.SLIDERX = posX
        self.SLIDERY = posY
        self.SLIDERLEN = 170
        self.SLIDERWID = 4
        self.SLIDERBUTLEN = 39
        self.SLIDERBUTWID = 20
        self.imgX=self.SLIDERX
        self.imgY=self.SLIDERY
        self.exImgX=self.imgX
        self.value = self.minVal
        self.rect = pygame.Rect(posX,posY-((self.SLIDERBUTWID-self.SLIDERWID)/2), self.SLIDERLEN,self.SLIDERBUTWID )

        self.s = mygui.Button()
        self.s1 = mygui.Button()
        self.s.create_button_image(screen, SL1, self.imgX,self.imgY,self.SLIDERLEN,self.SLIDERWID)
        self.s1.create_button_image(screen, SL2, self.imgX,self.imgY-((self.SLIDERBUTWID-self.SLIDERWID)/2),self.SLIDERBUTLEN,self.SLIDERBUTWID)
        pygame.display.update()

    def event_slider(self, event, mouse):
        if event.type == MOUSEMOTION:
            if ((event.buttons[0] and self.s1.pressed(pygame.mouse.get_pos())) or (self.s1.pressed(pygame.mouse.get_pos()))):
                rel = event.rel
                self.imgX += rel[0]
                if self.imgX > (self.SLIDERX+self.SLIDERLEN-self.SLIDERBUTLEN): self.imgX = (self.SLIDERX+self.SLIDERLEN-self.SLIDERBUTLEN)
                if self.imgX < self.SLIDERX: self.imgX = self.SLIDERX

        if event.type == MOUSEBUTTONDOWN:
            if self.pressed(mouse):
                self.imgX = mouse[0] - self.SLIDERBUTLEN/2
                if self.imgX > (self.SLIDERX+self.SLIDERLEN-self.SLIDERBUTLEN): self.imgX = (self.SLIDERX+self.SLIDERLEN-self.SLIDERBUTLEN)
                if self.imgX < self.SLIDERX: self.imgX = self.SLIDERX


    def slider_update(self, screen):
        screen.blit(BG1,(self.exImgX,self.SLIDERY-((self.SLIDERBUTWID-self.SLIDERWID)/2)),(self.exImgX,self.imgY-((self.SLIDERBUTWID-self.SLIDERWID)/2),self.SLIDERLEN,self.SLIDERBUTWID))
        self.s.create_button_image(screen, SL1, self.SLIDERX,self.SLIDERY,self.SLIDERLEN,self.SLIDERWID)
        self.s1.create_button_image(screen, SL2, self.imgX,self.imgY-((self.SLIDERBUTWID-self.SLIDERWID)/2),self.SLIDERBUTLEN,self.SLIDERBUTWID)

        exSurRect = self.surRect
        screen.blit(BG1,(exSurRect.topleft),exSurRect)

        self.value = int((float(self.imgX-self.SLIDERX)/(self.SLIDERLEN-self.SLIDERBUTLEN)) * (self.maxVal-self.minVal) + self.minVal)
        sur,self.surRect = mygui.print_text('freesansbold.ttf', 13, str(self.value), WHITE, None, self.imgX+(self.SLIDERBUTLEN/2), self.imgY-15)
        screen.blit(sur,self.surRect)
        pygame.display.update()

    def getValue(self):
        return self.value

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        # print  self.text + " button was pressed!"
                        return True
        return False
