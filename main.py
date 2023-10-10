import time

import pygame as pg
import sys
import random

pg.init()
vec = pg.math.Vector2

HEIGHT = 720
WIDTH = 1280
ACC = 2
FRIC = -0.22
FPS = 60
MAX_OBJWID = 400
FramePerSec = pg.time.Clock()

displaysurface = pg.display.set_mode((WIDTH, HEIGHT), flags = pg.SCALED, vsync=1)
pg.display.set_caption("Shadow Jumper")


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.image = pg.image.load("img/shadow1.png")

        self.rect = self.surf.get_rect()

        self.pos = vec((100, 700))
        displaysurface.blit(self.image,(self.pos.x-30, self.pos.y-60))

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dj = 1

    def move(self):
        self.acc = vec(0, 0.6)

        pressed_keys = pg.key.get_pressed()
        if self.vel.y < 20:
            self.vel += self.acc
        if self.vel.y > 20:
            self.vel.y = 15
        self.pos += self.vel + 0.5 * self.acc


        self.rect.midbottom = self.pos

    def jump(self):
        hits = pg.sprite.spritecollide(self, platforms, False)
        if self.dj == 1:
            self.vel.y = -20
            self.dj = 0
        if hits:
            self.vel.y = -20
            self.dj = 1
        hits = pg.sprite.spritecollide(self, buildings, False)
        if hits:
            self.vel.y = -20
            self.dj = 1


    def update(self):
        hits = pg.sprite.spritecollide(P, platforms, False)
        if P.vel.y > 0 :
            if hits:
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1

        hits = pg.sprite.spritecollide(P, buildings, False)

        if True:
            if hits:
                # print(hits[0].pos.x)
                print(self.pos.y, hits[0].size.y)
                if self.pos.y <= HEIGHT -  hits[0].size.y  and self.pos.x < hits[0].pos.x + hits[0].size.x :

                    # print("On top")
                    self.dj = 1
                    # print("RESET DJ")
                    if self.vel.y > 0:
                        self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1
                    return True
                elif self.pos.y < hits[0].rect.top:
                    # print("You suck!")
                    return False
                else:
                    # print("COLLIDED")
                    return False
        elif hits:
            return False







class Building(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        buildingNum = random.randint(1, 15)
        building = "img/building" + str(buildingNum) + ".jpg"
        self.image = pg.image.load(building)
        self.h = self.image.get_height()
        self.w = self.image.get_width()
        self.size = pg.Vector2(self.w,self.h)
        self.surf = pg.Surface(self.size)
        self.surf.fill((100,120,150))
        self.pos = pg.Vector2(WIDTH + MAX_OBJWID, HEIGHT - 20)
        self.rect = self.surf.get_rect(center = self.pos)
        self.passed = 0



    def move(self, speed):
        self.pos.x -= speed
        self.rect.midbottom = self.pos
        if self.pos.x < - self.size.x:
            print("KILL")
            self.kill()
        if self.pos.x < P.pos.x and self.passed != -1:
            self.passed = 1


class Bg(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pg.Vector2((0,0))


    def start(self, img, speed):
        self.vel = speed
        self.image = pg.image.load(img)
        displaysurface.blit(self.image,self.pos)

    def move(self,speed):
        if (self.pos.x < - self.image.get_width()):
            self.pos.x = WIDTH
        else:
            self.pos.x -= speed




# movingSprites.add(bg1)



def mainloop(displaysurface):
    global score

    music = pg.mixer.Sound("sdt.wav")
    music.play(loops = 999)
    score = 0
    timeDif = 0
    global flag
    flag = False

    count = 0
    end = 9999999999999999
    start = time.time()
    playerImage = pg.image.load("img/shadow1.png")
    swap = True
    while True:
        end = time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    P.jump()
        # backgrounds
        displaysurface.blit(bg, (0,0))
        displaysurface.blit(bg2.image, bg2.pos)
        displaysurface.blit(bg1.image, bg1.pos)


        if count%5 == 0:
            print("VEL",P.vel.y)
            print("ACC", P.acc.y)
            if P.acc.y == 0.6 and P.vel.y == 0.6:
                if swap:
                    swap = False
                    playerImage = pg.image.load("img/shadow1.png")
                else:
                    swap = True
                    playerImage = pg.image.load("img/shadow2.png")

            elif P.vel.y > 0:
                playerImage = pg.image.load("img/shadow3.png")

            else:
                playerImage = pg.image.load("img/shadow4.png")

        bg1.move(1 + (count/3000))
        bg2.move(0.5 + (count/3000))
        if (P.update() == False):
            music.stop()
            break
        font = pg.font.Font("ShadowsIntoLight-Regular.ttf", 64)
        text = font.render("Score: " +str(score), True, (255, 255, 255))
        textRect = text.get_rect()


        displaysurface.blit(text, (1010,-10))
        displaysurface.blit(Floor.surf, Floor.rect)
        for entity in movingSprites:
            if entity != P:
                displaysurface.blit(entity.image, entity.rect)
                entity.move(4 + (count/3000))
                if (entity.passed == 1):
                    score += 1
                    entity.passed = -1
                    # display updated score

                    displaysurface.blit(text, (1010,-10))
        P.move()

        #store time since last building
        # adds buildings occasionally
        # print("START", start)
        # print("END", end)
        if (len(movingSprites) < 5 and time.time() - start > random.randint(50,2500)/100 ):
            # print(start - end )
            b = Building()
            movingSprites.add(b)
            buildings.add(b)
            start = time.time()
        displaysurface.blit(playerImage, (P.pos.x -30 , P.pos.y - 60))

        pg.display.update()
        FramePerSec.tick(FPS)
        count += 1
        print(score)
        if count == 1:
            end = time.time()

global flag
flag = True

def init(displaysurface):
    global movingSprites
    global Floor
    global buildings
    global bg1
    global bg2
    global P
    global platforms
    global bg
    bg = pg.image.load("bg.jpg")
    Floor = Building()
    Floor.surf = pg.Surface((WIDTH, 20))
    Floor.surf.fill((20, 20, 20))
    Floor.rect = Floor.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    P = Player()

    all_sprites = pg.sprite.Group()
    all_sprites.add(Floor)
    all_sprites.add(P)

    b1 = Building()

    platforms = pg.sprite.Group()
    platforms.add(Floor)

    buildings = pg.sprite.Group()
    buildings.add(b1)

    all_sprites.add(b1)

    bg1 = Bg()
    bg2 = Bg()
    bg1.start("foreground.png", 5)
    bg2.start("clouds.jpg", 2)
    movingSprites = pg.sprite.Group()
    movingSprites.add(b1)
    movingSprites.add(P)
    # main title screen
    ## display something
    displaysurface.blit(bg, (0, 0))
    titleFont = pg.font.Font("ShadowsIntoLight-Regular.ttf", 128)
    title = titleFont.render("Shadow Jumper", True, (255, 255, 255))
    titleRect = title.get_rect(center=(WIDTH / 2, 150))

    if flag:


        displaysurface.blit(bg2.image, (0,0 ))
        displaysurface.blit(bg1.image, (0,0))
        displaysurface.blit(P.image, (70, 640))
        displaysurface.blit(Floor.surf, (0, 700))
        displaysurface.blit(title, titleRect)
        scoreTextFont = pg.font.Font("ShadowsIntoLight-Regular.ttf", 64)

        continueText = scoreTextFont.render("Press Space to Start", True, (255, 255, 255))
        continueTextRect = continueText.get_rect(center=(WIDTH/2, 350))
        displaysurface.blit(continueText,continueTextRect)
        pg.display.update()
    end = False

    while not end:

        event = pg.event.wait()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            end = True
            mainloop(displaysurface)
            break


while True:
    init(displaysurface)
    font = pg.font.Font("ShadowsIntoLight-Regular.ttf", 128)
    gameOver = font.render("Game Over!", True, (255, 255, 255))
    gameOverRect = gameOver.get_rect(center=(WIDTH / 2, 150))
    displaysurface.blit(gameOver, gameOverRect)

    scoreTextFont = pg.font.Font("ShadowsIntoLight-Regular.ttf", 64)
    scoreText = scoreTextFont.render("Score: " + str(score), True, (255, 255, 255))
    scoreTextRect = scoreText.get_rect(center=(WIDTH / 2, 250))
    displaysurface.blit(scoreText,scoreTextRect)

    continueText = scoreTextFont.render("Press Space to Continue", True, (255, 255, 255))
    continueTextRect = continueText.get_rect(center=(WIDTH/2, 500))
    displaysurface.blit(continueText,continueTextRect)

    pg.display.update()