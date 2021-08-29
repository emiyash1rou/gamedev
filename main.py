import pygame
import os
pygame.font.init()
 #use path to get the assets
WIDTH,HEIGHT= 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
WHITE=(255,255,255) 
BORDER=pygame.Rect(WIDTH//2-5,0, 10,HEIGHT)
HEALTH_FONT=pygame.font.SysFont('comicsans',40)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BULLET_VEL=10
MAX_BULLETS=3
WINNER_FONT=pygame.font.SysFont('comicsans',100)
VEL=5 #VELOCITY SPEED OF WHICH OBJECTS WILL BE MOVING
FPS=60 #DECLARE HOW FPS TO RUN BECAUSE IF NOT CAPPED THEN IT WILL DEPEND BASED ON THE UNIT
SPACESHIP_WIDTH, SPACESHIP_HEIGHT=55,40
YELLOW_HIT=pygame.USEREVENT+1 #PLUS 1 IS JUST THE NUMBER OF USER EVENT ITS LIKE A NAME FOR THE CUSTOM EVENT
RED_HIT=pygame.USEREVENT+2
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90) #55 width, 40 height. Use this to resize images. Transform.rotate rotates the imagery, with the 90 as its degrees
SPACE=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)  #55 width, 40 height. Use this to resize images. Transform.rotate rotates the imagery, with the 270 as its degrees
def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)
        
def draw_window(red,yellow,red_bullets,yellow_bullets,yellow_health, red_health):

     #Take an argument whatever we want to draw
     WIN.blit(SPACE,(0,0))#RGB 1,255. 
     pygame.draw.rect(WIN, BLACK, BORDER)
     red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1 ,WHITE) #1 is antialising always 1
     yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1 ,WHITE) #1 is antialising always 1
     WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
     WIN.blit(yellow_health_text,(10,10))
     WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y)) # draw the surface onto the screen. Put them onto the screen. When you draw something to the screen, it starts at the left hand corner. Top Left =(0,0) vertical y positive
     WIN.blit(RED_SPACESHIP,(red.x,red.y)) # ARGUMENTS RED AND YELLOW PASSES  A PYGAME RECT THAT HAS A COORDINATES. X AND Y

     for bullets in red_bullets:
         pygame.draw.rect(WIN,RED,bullets)
     for bullets in yellow_bullets:
         pygame.draw.rect(WIN,YELLOW,bullets)
     pygame.display.update() #TO UPDATE THE DISPLAY. IT's Like saving changes but for appearance.

def yellow_handle_movement(keys_pressed,yellow):
    
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:  #LEFT
        yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x: #RIGHT PASABOT ANE GI ADD NIYA ANG YELLOW.X+VEL PARA MAKUHA ANG ROOT NA MEASUREMENT SA X KUNG MUPADAYON PA BA. KARON ANG YELLOW.WIDTH MAO NA ANG X NA MEASUREMENT SA KADAKO SA SPACESHIP SO GIPLUS RA NA SIYA. ANG GIPLUS KAY ANG RESULTING SA PAG MOVE OG ANG KADAKO SA SPACESHIP TAPOS GICHECK IF MILAMPAS BA SA BORDER.x
        yellow.x+=VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0: #UP
        yellow.y-=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT: #DOWN
        yellow.y+=VEL
def red_handle_movement(keys_pressed,red):
    
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:  #LEFT CHECKS ANG BORDER.X ASA SIYA LOCATED OG PILA IYANG KADAKO WIDTH
        red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH: #RIGHT
        red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0: #UP
        red.y-=VEL
    if keys_pressed[pygame.K_DOWN] and  red.y+VEL+red.height<HEIGHT: #DOWN
        red.y+=VEL
def main():
    yellow_health=10
    red_health=10
    red_bullets=[] #BULLET LIST
    yellow_bullets=[] #BULLET LIST
    red= pygame.Rect(700,300,SPACESHIP_HEIGHT,SPACESHIP_WIDTH)
    yellow= pygame.Rect(100,300,SPACESHIP_HEIGHT,SPACESHIP_WIDTH) # SWITCHED HEIGHT AND WIDTH BECAUSE IT IS ROTATED FOR THE HITBOX TO MAKE SENSE
    clock= pygame.time.Clock() #CONTROL THE TICK OF THIS WHILE LOOP
    run=True
    while run:
        clock.tick(FPS) #CONTROL THE TICK OF THIS WHILE LOOP TO NEVER GO OVER 60
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                #ENDS THE GAME
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)

                if event.key==pygame.K_RCTRL  and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
            winner_text=""
            if event.type==YELLOW_HIT:
                yellow_health-=1
            
            if event.type==RED_HIT:
                red_health-=1
            if yellow_health<=0:
                winner_text="Red Wins"
            if red_health<=0:
                winner_text="Yellow Wins"
            if winner_text!="":
                draw_winner(winner_text) # SOMEONE WON
                pygame.quit()
        
    
        
        #MULTIPLE KEY AT ONE TIME
        keys_pressed=pygame.key.get_pressed() #REGISTER WHEN A KEY IS PRESSED DOWN, even when its still being press/hold
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,yellow_health,red_health)
    
if __name__=="__main__":
    main()
            

