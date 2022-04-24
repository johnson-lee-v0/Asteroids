import pygame,sys,random,math,easygui
pygame.init()
pygame.key.set_repeat(1, 50)
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Asteroids')

black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
red = [255, 0, 0]

font = pygame.font.SysFont("Arial",14)
numAsteroids = 4
asteroidSize = 20.0
maxSpeed=10
bulletSpeed=10
reload=0
wave=1
score=0
lives=3

class Ship:
    def __init__(self):
        self.pos = [width/2,height/2]
        self.speed = 0
        self.angle = 0
        self.points = [[-5,0],[-15,-10],[15,0],[-15,10]]
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed*math.cos(self.angle*math.pi/180)) % width
        self.pos[1] = int(self.pos[1] + self.speed*math.sin(self.angle*math.pi/180)) % height
    def getShape(self):
        ang=self.angle*math.pi/180.0
        points=[]
        for p in self.points:
            x=p[0]*math.cos(ang)-p[1]*math.sin(ang)+self.pos[0]
            y=p[0]*math.sin(ang)+p[1]*math.cos(ang)+self.pos[1]
            points.append([x,y])
        return points

class Asteroid:
    def __init__(self,size,pos,speed=None):
        self.size=size
        self.points=[]
        for i in range(0,8):
            ang=math.pi*i/4
            l=size+random.randint(-int(size/2),int(size/2))
            self.points.append([l*math.cos(ang),l*math.sin(ang)])
        self.pos=pos	
        if speed==None:
            self.speed=[random.random()*10-4,random.random()*10-4]
        else:
            self.speed=speed
        self.angle=0.0
        self.rotation=random.random()*2-1
    def move(self):
        self.pos[0] = (self.pos[0] + self.speed[0]) % width
        self.pos[1] = (self.pos[1] + self.speed[1]) % height
        self.angle = self.angle + self.rotation
    def getShape(self):
        ang=self.angle*math.pi/180.0
        points=[]
        for p in self.points:
            x=p[0]*math.cos(ang)-p[1]*math.sin(ang)+self.pos[0]
            y=p[0]*math.sin(ang)+p[1]*math.cos(ang)+self.pos[1]
            points.append([x,y])
        return points

class Bullet:
    def __init__(self,pos,speed):
        self.pos = pos
        self.speed = speed
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed[0])
        self.pos[1] = int(self.pos[1] + self.speed[1])
def pointInsidePolygon(x,y,poly):
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside



ship = Ship()
asteroids=[]
bullets=[]

for a in range(0, numAsteroids):
    asteroids.append(Asteroid(asteroidSize, [random.random()*width,50.0]))
                


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.angle = ship.angle-10
        if keys[pygame.K_RIGHT]:
            ship.angle = ship.angle+10
        if keys[pygame.K_UP]:
            ship.speed = ship.speed+3
            if ship.speed>maxSpeed:
                ship.speed=maxSpeed
        if keys[pygame.K_DOWN]:
            ship.speed = ship.speed-3
            if ship.speed<0:
                ship.speed=0
        if keys[pygame.K_SPACE]:
            if reload>10:
                bx=bulletSpeed*math.cos(ship.angle*math.pi/180)
                by=bulletSpeed*math.sin(ship.angle*math.pi/180)
                bullet = Bullet([ship.pos[0],ship.pos[1]], [bx,by])
                bullets.append(bullet)
                reload=0
        reload=reload+10
        

    for p in ship.getShape():
        for a in asteroids:
            if pointInsidePolygon(p[0],p[1],a.getShape()):
                lives=lives-1

            if lives <=0:
                Gameover=easygui.buttonbox("Do you want to play again","Gameover",choices=("Yes","No"))
                if Gameover=="Yes":
                    lives = 3
                    wave=0
                    score = 0
                    ship = Ship()
                    asteroids=[]
                    bullets=[]
                    numAsteroids=4
                    for a in range(0, numAsteroids):
                        asteroids.append(Asteroid(asteroidSize, [random.random()*width,50.0]))
                else:
                    asteroids.remove(a)
                    pygame.quit()
                    sys.exit()
                    break

    ship.move()
    for a in asteroids:
        a.move()
    for b in bullets:
        b.move()
        if b.pos[0]<0 or b.pos[0]>width or b.pos[1]<0 or b.pos[1]>height:
            bullets.remove(b)
    for b in bullets:
        for a in asteroids:
            if pointInsidePolygon(b.pos[0],b.pos[1],a.getShape()):  
                bullets.remove(b)
                asteroids.remove
                score=score+40
                if a.size>10:
                    new=Asteroid(int(a.size/2),[a.pos[0],a.pos[1]],[a.speed[0],a.speed[1]])
                    asteroids.append(new)
                    new=Asteroid(int(a.size/2),[a.pos[0],a.pos[1]],[a.speed[1],a.speed[0]])
                    asteroids.append(new)
                    new=Asteroid(int(a.size/2),[a.pos[0],a.pos[1]],[-a.speed[0],a.speed[1]])
                    asteroids.append(new)
                    new=Asteroid(int(a.size/2),[a.pos[0],a.pos[1]],[-a.speed[1],a.speed[0]])
                    asteroids.append(new)
                asteroids.remove(a)
                break
            
    for b in bullets:
        b.move()
        if b.pos[0]<0 or b.pos[0]>width or b.pos[1]<0 or b.pos[1]>height:
            bullets.remove(b)

    if len(asteroids)==0:
        numAsteroids=numAsteroids+1
        wave=wave+1
        for a in range(0,numAsteroids):
            asteroids.append(Asteroid(asteroidSize, [random.random()*width,50.0]))

    

    screen.fill(black)
    # draw your game elements here:
    for a in asteroids:
        pygame.draw.polygon(screen, white, a.getShape(),1)
    for b in bullets:
        pygame.draw.circle(screen, red, b.pos, 1, 0)
    for x in range(0,lives):
        rct = pygame.Rect(10+x*40,height-25,35,25)
        pygame.draw.rect(screen,green,rct,0)

    renderedText = font.render("Score: "+str(score),1,white)
    renderedText1 = font.render("Wave: "+str(wave),1,white)
    screen.blit(renderedText, (width/2+50,10))
    screen.blit(renderedText1, (width/2,10))
    pygame.draw.polygon(screen, green, ship.getShape(),1)
    pygame.display.flip()
    pygame.time.wait(50)

    

    
