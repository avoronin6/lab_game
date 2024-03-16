from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((1000, 700))
display.set_caption('космос')
background = transform.scale(image.load('1660294702_1-kartinkin-net-p-fon-dlya-igri-kosmos-krasivo-1.png'),(1200, 600))



mixer.init()
mixer.music.load('ljapis-trubeckojj-nu-chto-zh-ty-strashnaja-takaja.mp3')
mixer.music.play()
#fire1 = mixer.Sound('1.mp3')
#death = mixer.Sound('wilhelm_scream.mp3')
#lose = mixer.Sound('d19400703bb8adc.mp3')

font.init()
font2 = font.Font(None, 70)
win = font2.render('YOU WIN', True, (0, 255, 0))
loser = font2.render('YOU LOSE', True, (0, 255, 0))
font2 = font.Font(None, 30)







class GameSprite(sprite.Sprite):
    def __init__(self, p_i, p_x, p_y, p_s, p_s_x, p_s_y):
        super().__init__()
        self.image = transform.scale(image.load(p_i), (p_s_x, p_s_y))
        self.speed = p_s
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        global last_time
        global num_fire
        global rel_time
        
        
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 950:
            self.rect.x += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                #fire1.play()
                self.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
        
    def fire(self):
        pulia = Pulia('Без названия.jpg', self.rect.centerx, self.rect.top, 10, 15, 30)
        pulias.add(pulia)


class Pulia(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 950:
            self.rect.y = 0
            self.rect.x = randint(50, 900)
            lost = lost + 1
        
class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 950:
            self.rect.y = 0
            self.rect.x = randint(50, 900)
            lost = lost + 1


boss = Boss('Без названия (1).jpg', randint(50, 900), 10, 1, 150, 150)
pulia = GameSprite('Без названия.jpg', 118, 570, 10, 15, 30)
hero = Player('images.jpg', 100, 600, 10, 50, 50)
#enemy = Enemy('Без названия (1).jpg', 700, 400, 15, 50, 50)            
background = GameSprite('1660294702_1-kartinkin-net-p-fon-dlya-igri-kosmos-krasivo-1.png', 0, 0, 0, 1000, 700)
pulias = sprite.Group()
enemys = sprite.Group()

score = 0
goal = 1000

for i in range(1, 9):
    enemy = Enemy('Без названия (1).jpg', randint(50, 900), 10, 1, 50, 50)
    enemys.add(enemy)

finish = False
clock = time.Clock()
FPS = 60
game = True

num_fire = 0
last_time = 0
rel_time = False

boss_hp = 10

life = 3

while game:
    text_score = font2.render('Счёт: ' + str(score), True, (255, 255, 255))
    text_lose = font2.render('Проигрыши: ' + str(lost), True, (255, 255, 255))
    text_life = font2.render('Жизни: ' + str(life), True, (255, 0, 0))
    
    for i in event.get():
        if i.type == QUIT:
            game = False
    
    collide = sprite.groupcollide(enemys, pulias, True, True)
    #if collide:
        #death.play()
    for i in collide:
        score = score + 1
        enemy = Enemy('Без названия (1).jpg', randint(50, 900), 10, 1, 50, 50)
        enemys.add(enemy)
    
    
    if not finish:
        background.reset()
        
        hero.reset()
        enemys.draw(window)
        enemys.update()
        pulias.draw(window)
        pulias.update()
        
        window.blit(text_score, (10, 10))
        window.blit(text_lose, (10, 50))
        window.blit(text_life, (10, 90))
        
        if score > 10:
            boss.reset()
            boss.update()


        hero.update()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                ammo_no = font2.render('Reload', 1, (255, 0, 0))
                window.blit(ammo_no, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
        if sprite.spritecollide(boss, pulias, True):
            boss_hp -= 1
        
        
        if sprite.spritecollide(hero, enemys, True):
            life -= 1
            enemy = Enemy('Без названия (1).jpg', randint(50, 900), 10, 1, 50, 50)
            enemys.add(enemy)
        if score >= goal or boss_hp <= 0:
            finish = True
            window.blit(win, (200, 50))
            
        if life <= 0:
            finish = True
            window.blit(loser, (200, 50))

    
        display.update()
    
    clock.tick(FPS)










