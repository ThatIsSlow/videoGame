# content from kids can code: http://kidscancode.org/blog/
# Sources:
    # Content from Mr Cozy, written in class and drawn from Class files
    # https://stackoverflow.com/questions/20359845/how-would-i-add-a-running-timer-that-shows-up-on-the-screen-in-pygame
        # used stack overflow too help me set up the timer that displays top left
    # My father helped me figure out how to reset the timer every game run, also advised me to use variables that mean something

### THINGS TO DO ###
# 1. game is done, I have a starting screen and a goal and so and so
# 2. make a way to restart game (a loop, but where)
        # Completed this

# 3. add images, make the game a theme
# 4. make the mobs speed up and slow down
# 5. add a points leaderboard





# import libraries and modules
# from platform import platform
from ast import Global
import pygame as pg
from pygame.sprite import Sprite
from random import randint

vec = pg.math.Vector2

# game settings 
WIDTH = 1000
HEIGHT = 850
FPS = 30

# player settings
PLAYER_FRIC = -0.28
PLAYER_GRAV = .98
POINTS = 0


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




#Sets up the draw text feature to allow me to draw text on the window
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

#sets up a starting screen as a function so I can call it later
def screen1():
    screen.fill(WHITE)
    draw_text("Welcome To This Game. Your objective is to hunt down the cubes", 25, BLACK, WIDTH/2, HEIGHT/3)
    draw_text("Press Enter to Continue", 20,BLACK, WIDTH/2, HEIGHT/2-40)
    
# sets up the actual game screen, also as a function  
def screen2():
    screen.fill(BLACK)
    draw_text("POINTS: " + str(POINTS), 22, WHITE, WIDTH / 2, HEIGHT / 24)
#sets up the start again screen, also a function
def screen3(score):
    screen.fill(WHITE)
    draw_text("Welcome Back. Your objective is to hunt down the cubes", 25, BLACK, WIDTH/2, HEIGHT/3)
    draw_text("Press Enter to Continue", 20,BLACK, WIDTH/2, HEIGHT/2-40)
    draw_text("Your last score was:" + score, 30, BLACK, WIDTH/2, HEIGHT/2+40 )
    
    
  

# sprites...

# makes the player sprite
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # Enables movement
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -5
        if keys[pg.K_RIGHT]:
            self.acc.x = 5
        if keys[pg.K_UP]:
            self.acc.y = -5
        if keys[pg.K_DOWN]:
            self.acc.y = 5
    # bread and ptoatoes of the player class, prevents it from leaving screen and enables movement
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        # friction
        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.topleft = self.pos
        # This block prevents the player from leaving the screen, took a while to figure out, had to make acceleration and position equal
        # whatever they were supposed to equal. 
        if self.rect.right > WIDTH:
            self.rect.x = WIDTH - 50
            self.pos.x = WIDTH-50
            self.acc = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = 0
            self.acc = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = 0
            self.acc = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = HEIGHT-50
            self.acc = 0

# Not using the platform sprite but It is here
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# mob sprrite, it bounces around the screen
class Mob(Sprite):
    def __init__(self, x, y, color):
        Sprite.__init__(self)
        self.image = pg.Surface((randint(15,25),randint(15,25)))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width/2, self.rect.height/2)
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x,y)
        self.vel = vec(randint(-7,7),randint(-7,7))
        
    def update(self):
        # allows for the movement of the mob
        self.pos += self.vel
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        # prevents mob from bouncing off of screen by mulitplying velocity by negative 1
        if (self.pos.x + self.rect.width > WIDTH or self.pos.x < 0):
            self.vel.x *= -1
        if (self.pos.y + self.rect.height > HEIGHT or self.pos.y < 0):
            self.vel.y *= -1

    
# init pygame and create a window
pg.init()
pg.mixer.init()

#creats a variable called a screen
screen = pg.display.set_mode((WIDTH, HEIGHT))

    
#captions the game and sets the variable clock 
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
start_time = pg.time.get_ticks() 
font = pg.font.SysFont(None, 40)

  
# create a group for all sprites, also creates group for the mobs
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate player class
player = Player()

# add instances to groups
all_sprites.add(player)

#sets variable for number of mobs, its a variable so I can use it down below
mob_numb = 10

#made into a fucntion so that it could be called within the game loop
def mob_create():
    print(mob_numb)
    for i in range(mob_numb):
        # instantiate mob class repeatedly with randomized arguments
        m = Mob(randint(0, WIDTH-20), randint(0,HEIGHT-20),(randint(75,255), randint(75,255) , randint(75,255)))
        #adds them all to the sprites group and the mobs group
        all_sprites.add(m)
        mobs.add(m)

# counter to instantiate a wide variety of mob classes
# variable to allow the spawning of mobs every time the player wants to restart
mobGenerated = False

# Game loop
running = True
# possible states of the game are WELCOME, RUNNING, and END
state = "WELCOME"
paused  = False
timer = False
counting_time = 0


while running:
    
    # lil thing right here lets mobs generate if they have not generated yet, mobGenerated becomes false again if the player chooses to play again
    if (not mobGenerated):
        mob_numb = (randint(5,15))
        mobGenerated = True
        mob_create()

    # keep the loop running using clock
    delta = clock.tick(FPS)
    
    # Lets player close out of game by pressing the lil X
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
        # Checks if the player collided with the mobs, and if they did collide, it eats them and then it adds to the score
        # uses built in function from Pygame
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        POINTS += 1
        print(POINTS)
        print("i've collided...with a mob")
        
        
    #used for ending the game after enough mobs are eaten
    win_condition = 0
    
    ############ Draw ################
    # draw the background screen
    
    #this thing runs the screen functions to enable the starting screen
    # uses functions from above to display differeent thing onto the screen, each screen has a different set of things
    # that can happen when something ocurs
    if state == "WELCOME":
        screen1() 
        start_time = pg.time.get_ticks()      
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            state = "RUNNING"
            
            
     # this screen is the only screen that sprties update and draw on
     # This is the actual game here
    elif state == "RUNNING":
        screen2()
        all_sprites.update()
        all_sprites.draw(screen)
        # This timer was pulled from external source, modified slightly to fit my code. 
        if not paused:
            counting_time = pg.time.get_ticks() - start_time     
            
            # change milliseconds into minutes, seconds, milliseconds
            # as long as the win condition isin't met, the timer keeps counting
            if POINTS != mob_numb:
                # MATH #
                counting_minutes = int(counting_time/60000)
                counting_minutes = round(counting_minutes)
                counting_seconds = int( (counting_time%60000)/1000 )
                counting_seconds = round(counting_seconds)
                counting_millisecond = int(counting_time%1000)
                counting_millisecond = round(counting_millisecond)

                # MATH #
                counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)

                counting_text = font.render(str(counting_string), 1, (255,255,255))
                counting_rect = counting_text.get_rect(left = screen.get_rect().left)

            # ACtually prints the timer. 
            screen.blit(counting_text, counting_rect)
     # This is the start again screen, also displays the players final score from their last round.        
    else:
        screen3(score)
        start_time = pg.time.get_ticks() 
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            state = "RUNNING"
            
            
# enables the scoring system using the timer. If win conditin is met, and the timer is False, then the score is updated
# and made global. 
    if POINTS == mob_numb and timer == False:
        timer = True 
        score = counting_string 
        Global(score)
        
    
    #point counter that shows the point total and draws " winner" if you eat all of the mobs
    # its a little messy because I spent a lot of time goint through it and trying different things
    # eventually I got something that worked, but I did not wan to risk breaking it so I didnt clean it up
    if POINTS == mob_numb:
        # Mostly for player enjoyement
        draw_text("POINTS: " + str(POINTS), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        draw_text("WINNER", 100, BLUE, WIDTH/2, HEIGHT/2-50)
        draw_text("Press BACKSPACE to play again", 20, RED, WIDTH/2, HEIGHT/2 + 50)
        pg.display.flip()
        win_condition += 1
        if win_condition == 1:
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                # resets all the variabls so the game can run again. 
                POINTS = 0
                state = "END"
                mobGenerated = False
                timer = False
                counting_time = 0
                
                
               
    
    
    # buffer - after drawing everything, flip display
    pg.display.flip()
    
    

pg.quit()
