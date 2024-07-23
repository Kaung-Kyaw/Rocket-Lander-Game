# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:18:11 2021

@author: kaung
"""

import pygame
import time

#starting game
pygame.init()

#screen and UI and Intiial Conditions and defining colours using RGB
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (180,180,180)
clock = pygame.time.Clock()
TARGET_FPS = 100
#pixels chosen at 940 as that's the original aspect of the background image 
screen = pygame.display.set_mode((940,579))

rocketimg = pygame.image.load("ufo.png")
rocketimg = pygame.transform.scale(rocketimg, (50, 50))
rocketx = 445
rockety = 0

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background,(940,579))

crashimg = pygame.image.load("crash.png")
crashimg = pygame.transform.scale(crashimg, (70,70))
crashx = rocketx-15
crashy = 295-20




#condition for running pygame and also for flying mechanism, fly_velocity will determine how fast the rocket is pushed up while falling
start = False
running = True
fly = False 
fly_velocity = 0.028
fuel = 100

v = 0
g = 1                               




#caption and icon
pygame.display.set_caption("Rocket Lander")
icon = pygame.image.load("astronaut.png")
pygame.display.set_icon(icon) #reaches planet at 295 pixels 

#Menu screen/Start Screen
menu_font = pygame.font.Font("8-BIT WONDER.TTF",25)
menu_text1 = menu_font.render("ROCKET LANDER DESCENDING ON THE MOON",True, WHITE, BLACK)
menu_text1Rect = menu_text1.get_rect()
menu_text1Rect.center = (940/2,579/2 - 40)
menu_font = pygame.font.Font("8-BIT WONDER.TTF",20)
menu_text2 = menu_font.render("PRESS SPACE BAR TO PLAY AND TO USE FUEL IN GAME",True, WHITE, BLACK)
menu_text2Rect = menu_text2.get_rect()
menu_text2Rect.center = (940/2,579/2)




#instructions
font = pygame.font.Font("freesansbold.ttf", 28)
instruction_text = font.render("LAND SLOWER THAN 8 m/s!",True, RED, BLACK)
instruction_textRect = instruction_text.get_rect()
instruction_textRect.center = (220,25)

#creating variables and setting conditions to show velocity of rocket, will have to repeat in while loop to update 
velocity_text = font.render(str(v)+"m/s", True, WHITE, BLACK)
velocity_textRect = velocity_text.get_rect()
velocity_textRect.center = (220,55)


#distance travelled, will have to repeat later in while loop to update
distance_font = pygame.font.Font("freesansbold.ttf", 18)
distance_text = distance_font.render("",True,WHITE, GREY)
distance_textRect = distance_text.get_rect()
distance_textRect.center = (rocketx-60,348)

#fuel indicator
fuel_text = distance_font.render(str(fuel), True, WHITE, BLACK)
fuel_textRect = fuel_text.get_rect()
fuel_textRect.center =(rocketx+60,rockety)

#defining a function for drawing menu/start screen things
def menu():
    screen.blit(menu_text1,menu_text1Rect)
    screen.blit(menu_text2, menu_text2Rect)



#function for drawing rocket
def rocket():
    screen.blit(rocketimg,(rocketx,rockety))

#function for suvat drawing on screen
def suvat():
    screen.blit(velocity_text,velocity_textRect)
    screen.blit(instruction_text,instruction_textRect)
    screen.blit(distance_text,distance_textRect)

#function for drawing the fuel percentage next to rocket
def drawfuel():
    screen.blit(fuel_text,fuel_textRect)

#function for determining the end game screen, whether the player wins or loses
def endgame(win):
    font = pygame.font.Font('8-BIT WONDER.ttf', 55)
    if win == True:
        win_text = font.render("Victory",True, GREEN,BLACK)
        win_textRect = win_text.get_rect()
        win_textRect.center = (940/2,100)
    if win == False: 
        win_text = font.render("DEFEAT",True, RED, BLACK)
        win_textRect = win_text.get_rect()
        win_textRect.center = (940/2,100)
        screen.blit(crashimg, (crashx,crashy))
    
    screen.blit(win_text,win_textRect)
        
        

while running == True: 
    
    #creating scren, and also game time/clock keeping that is consistent with the specified fps so that the physics may remain unchanged. Clock.tick computes how much time has passed in milliseconds per frame, so in this case 60fps should allow 0.001 milliseconds to pass, which allows for suvat/time equations. 
    
    screen.fill((0,0,0))
    
    
    
    
    
    
    #running for loop for events that happen in pygame to be able to close and quit the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
       
    
    
    
    #creates condition for if start is false, so menu is displayed, created clock.tick again so that the time of the game resets when entering the game, otherwise the rocket will jump locations from the beginning of the launch of programme rather than beginning of the game. 
    if start == False:
        menu()
        dt = 0
        clock.tick(TARGET_FPS)
    
        
    #start condition true, exits menu
    else:
        #calling the visible objects to game screen and clock to make suvat work in real time 1 second occurs every 60 frames, but is in milliseconds so multiplied by 0.001. Repeated the line in the loop to restart game timer again otherwise occurs from launch of programme (including menu time) not game. 
        screen.blit(background, [0, 0])
        dt = clock.tick(TARGET_FPS)*0.001
        
        #define keys, so button may be used to burn fuel and hence propel the rocket up
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and rockety > v:
            fly = True
        
        #Calling functions to draw and to update the display continuously 
        drawfuel()
        suvat()
        rocket()
        
        #starts loop which will ensure rocket will end at 295 pixels which is equivalent to 100m by multiplying the suvat below by 2.95 where distance applies
        if rockety < 295:
           
            # uses equations of motion to get the speed of the velocity with game time
            v += g*dt
            
            #the rocket's position is multiplied by 2.95 as we want 100m and there are 295 pixels.
            rockety += v*dt*2.95
            
            #creates conditions for using fuel, cannot go out of screen, and rate of fuel loss 
            if fly == True and rockety > 0-v and fuel > 0: 
                v += g*dt - fly_velocity
                fly = False
                fuel -= 0.1
            
            #creates condition for what happens if speed would exceed screen height at the top
            if fly == True and rockety < -v:
                v = 0
                fly = False
            
            #repeating the rectangles of the texts so the positions are constantly updated, and the variables tht are changing can be seen updating with the loop.
            instruction_textRect.center = (220,rockety+25)
            velocity_text = font.render(str(round(v,2))+" m/s", True, WHITE, BLACK)
            velocity_textRect.center = (220,rockety+55)
            distance_text = distance_font.render("Distance: "+str(round(100-rockety/2.95,0))+" m",True, BLACK, GREY)
            #"distance_textRect.center = (rocketx+150,rockety+20)"
            fuel_text = distance_font.render("Fuel: "+str(round(fuel,0))+"%", True, WHITE, BLACK)
            fuel_textRect.center =(rocketx+85,rockety+20)
        
            
            
        #condition for when rocket hits moon ground   
        else: 
            #if faster than required of 8m/s defeat
            if v > 8: 
                #slight sleep added as it feels more smooth 
                time.sleep(0.15)
                screen.blit(background, [0, 0])
                endgame(False)
                instruction_textRect.center = (280,rockety+25)
                instruction_text = font.render("CRASHED! CRASHED!", True, RED, BLACK)
                velocity_text = font.render(str(round(v,2))+" m/s", True, RED, BLACK)
                distance_text = distance_font.render("Distance: "+str(round(100-rockety/2.95,0))+" m",True, RED, GREY)
                fuel_text = distance_font.render("Fuel: "+str(round(fuel,0))+"%", True, RED, BLACK)
               
                
                drawfuel()
                suvat()
            
            #if slower than required of 8m/s victory 
            else:
                #slight sleep added as it feels more smooth
                time.sleep(0.15)
                instruction_text = font.render("SUCCESS! SUCCESS!", True, GREEN, BLACK)
                velocity_text = font.render(str(round(v,2))+" m/s", True, GREEN, BLACK)
                distance_text = distance_font.render("Distance: "+str(round(100-rockety/2.95,0))+" m",True, GREEN, GREY)
                fuel_text = distance_font.render("Fuel: "+str(round(fuel,0))+"%", True, GREEN, BLACK)
                endgame(True)
                drawfuel()
                suvat()
                
                
                
                    
    

        
    
        
        
        
      
    pygame.display.update()
        
   
    
         
    
else: 
    pygame.quit()
    
    
