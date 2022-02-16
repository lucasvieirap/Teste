import pygame, random
from pygame import * 
from sys import exit

pygame.init()
mixer.init()

size = [800, 600]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Black Cock Jumper')

clock = pygame.time.Clock()

class Galinhou:
    def __init__(self, GalinhouPos, GalinhouImg, GalinhouRect):
        GalinhouPos = [100, 300]
        GalinhouImg = pygame.transform.scale(pygame.image.load('assets/galinhou.png'), [64, 64])
        GalinhouRect = GalinhouImg.get_rect(center = GalinhouPos)
        self.GalinhouPos = GalinhouPos
        self.GalinhouImg = GalinhouImg
        self.GalinhouRect = GalinhouRect
    
    def atirar(self, TiroPos, TiroImg, TiroRect, GalinhouRect):
        TiroPos = [GalinhouRect[0] + 32, GalinhouRect[1] + 32]
        TiroImg = pygame.transform.scale(pygame.image.load("assets/tiro.png"), [64, 64])
        TiroRect = TiroImg.get_rect(center = TiroPos)
        self.TiroPos = TiroPos
        self.TiroImg = TiroImg
        self.TiroRect = TiroRect
        screen.blit(self.TiroImg, self.TiroRect)
        TiroRect[0] += 5
        return TiroImg, TiroRect

def display_message(Message, MessageRect, display, pos=[400, 300]):
    Message = font.render(display, False, (255, 255, 255))
    MessageRect = Message.get_rect(center = pos)
    screen.blit(Message, MessageRect)

def scoreadd(score):
    score += 0.008
    return score

# GALINHOU:
galinhou = Galinhou('GalinhouPos', 'GalinhouImg', "GalinhouRect")
bemtevi = pygame.mixer.music.load("assets/bemtevi.mp3")

# PIPE:
PipePos = [600, random.randint(250, 600)]
PipeImg = pygame.transform.scale(pygame.image.load('assets/pipe.png'), [64, 600])
PipeRect = PipeImg.get_rect(midtop = PipePos)

# PIPE2:
Pipe2Pos = [600, (PipePos[1] - 250)]
Pipe2Img = pygame.transform.scale(pygame.image.load('assets/pipe2.png'), [64, 600])
Pipe2Rect = Pipe2Img.get_rect(midbottom=Pipe2Pos)

# TIRO:
TiroPos = [900, 800]
TiroImg = pygame.transform.scale(pygame.image.load("assets/tiro.png"), [64, 64])
TiroRect = TiroImg.get_rect(center = TiroPos)

font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
gravidade = 0
GameAtivo = False
score = 0

while True:
    a = open('highscore', 'r')
    data = a.read()
    a.close()
    a = open('highscore', 'w')
    a.write(data)
    score2 = f'{scoreadd(score) :.0f}'
    if score > float(data):
        a.seek(0)
        a.truncate(0)
        a.write(str(score2))
    a.close()
    a = open('highscore', 'r')
    highscore = font.render(f'Highscore: {a.read()}', False, (255, 255, 255))
    highscoreRect = highscore.get_rect(center = [400, 50])
    a.close()

    if GameAtivo:
        screen.fill((0, 0, 0))
        screen.blit(galinhou.GalinhouImg, galinhou.GalinhouRect)
        screen.blit(PipeImg, PipeRect)
        screen.blit(Pipe2Img, Pipe2Rect)

        display_message('ScoreMessage', 'ScoreMessRect', f'Score: {score :.0f}', [150, 50])
        score = scoreadd(score)
        
        gravidade += 1.5
        if gravidade > 15:
            gravidade = 15
        galinhou.GalinhouRect[1] += gravidade
        TiroPos[0] += 10
        if galinhou.GalinhouRect[1] >= 536:
            GameAtivo = False
        if galinhou.GalinhouRect[1] <= -8:
            GameAtivo = False

        PipePos[0] -= 8
        Pipe2Pos[0] -= 8
        
        if PipePos[0] < -100:
            PipePos = [900, random.randint(250, 600)]
            PipeRect = PipeImg.get_rect(midtop=PipePos)
            screen.blit(PipeImg, PipeRect)
        if Pipe2Pos[0] < -100:
            Pipe2Pos = [900, (PipePos[1] - 250)]
            Pipe2Rect = Pipe2Img.get_rect(midbottom=Pipe2Pos)
            screen.blit(Pipe2Img, Pipe2Rect)
        PipeRect[0] = PipePos[0]
        Pipe2Rect[0] = PipePos[0]
        if galinhou.GalinhouRect.colliderect(PipeRect) or galinhou.GalinhouRect.colliderect(Pipe2Rect):
            GameAtivo = False

    else:
        score = 0
        PipePos = [600, random.randint(250, 600)]
        Pipe2Pos = [600, (PipePos[1] - 250)]
        PipeRect = PipeImg.get_rect(midtop=PipePos)
        Pipe2Rect = Pipe2Img.get_rect(midbottom=Pipe2Pos)
        galinhou.GalinhouRect = galinhou.GalinhouImg.get_rect(center=galinhou.GalinhouPos)
        TiroPos = [900, 700]
        screen.fill((0, 0, 0))
        display_message('message', 'MessageRect', 'Press Space To Play', [400, 300])
        screen.blit(highscore, highscoreRect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP and GameAtivo:
                gravidade = -23
            if GameAtivo == False and event.key == K_SPACE:
                GameAtivo = True
            if GameAtivo and event.key == K_z:
                galinhou.atirar('TiroPos', 'TiroImg', 'TiroRect', galinhou.GalinhouRect)
            if GameAtivo and event.key == K_x:
                bemtevi.play()
    if GameAtivo:
        screen.blit(TiroImg, TiroRect)

    pygame.display.update()
    clock.tick(60)
