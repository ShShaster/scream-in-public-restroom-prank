from pygame import *
from random import *
window=display.set_mode((700, 500))
max_lost=30
score = 0  
lost = 0
x1,y1=100,100
x2,y2=40, 90
height=500
width=700
imgbg="background.png"
imgfish="fish.png"
imgsub="submarine.png"
imgbul="net.png"
font.init()
font2 = font.Font(None, 36)
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<width - 80:
            self.rect.x+=self.speed
    
    def fire(self):
        bullet=Bullet(imgbul, self.rect.centerx, self.rect.top, 80, 100, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>=height:
            self.rect.x=randint(80,width - 80)
            self.rect.y=0
            lost=lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global score
        if self.rect.y<0:
            self.kill()


bullets=sprite.Group()

display.set_caption("Shooter")
window=display.set_mode((width, height))
background=transform.scale(image.load("background.png"), (width, height))
submarine=Player(imgsub, 5, height - 100, 80, 100,  5)

entities=sprite.Group()
for i in range(1,6):
    entity=Enemy("fish.png", randint(80, width-80,), -40,80,50, randint(1,3))
    entities.add(entity)
end=False
run=True
clock=time.Clock()
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type==KEYDOWN:
            if e.key ==K_SPACE:
                submarine.fire()

    if not end:
        # оновлюємо фон
        window.blit(background, (0, 0))
 
        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_gameover=font2.render("Ви програли", 1, (255,255,255))

        window.blit(text_lose, (10, 50))
        collides=sprite.groupcollide(entities, bullets, True, True)

        for c in collides:
            score=score+1
            entity=Enemy(imgfish, randint(80, width-80), -40, 80, 50, randint(1,5))
            entities.add(entity)
        if sprite.spritecollide(submarine, entities, False) or lost >=max_lost:
            
            window.blit(text_gameover,(0, 0))
            end=True





        submarine.update()
        entities.update()
        bullets.update()
        submarine.reset()
        bullets.draw(window)
        entities.draw(window)
        display.update()
        clock.tick(60)
