import arcade as arc
import time as t
import random as r

#const
width = 626
height = 434
title = "Game"
jump = 10
gravity = -0.3

#main_character
class Bird(arc.Sprite):
    def __init__(self,window):
        super().__init__("Main1.png",1.3)
        self.center_x = 100
        self.center_y = 400
        self.cooldown_time = 0.4
        self.timer = t.time()
        self.cooldown = False
        self.change_angle = 0
        self.window = window
        for i in range(3):
            self.append_texture(arc.load_texture(f"Main{i}.png"))
    def update(self):
        self.angle+=self.change_angle
        self.center_y+=self.change_y
        self.change_y+=gravity
        if t.time()-self.timer > self.cooldown_time:
            self.cooldown = False
        if self.top <= -10 or self.bottom>=height+10:
            self.window.game = False
            self.window.lose = True
            
#obstacles
class Obstacles(arc.Sprite):
    def __init__(self,image,scale,change_angle):
        super().__init__(image,scale)
        self.change_x = -10
        self.left = width
        self.center_y = r.randint(0,height)
        self.change_angle = change_angle
    def update(self):
        self.center_x+=self.change_x
        self.angle+=self.change_angle
        if self.left <= 0:
            self.left = width
            self.center_y = r.randint(0+10,height-10)
            self.change_x-=0.5 
            self.change_angle+=1

class Rock(Obstacles):
    def __init__(self):
        super().__init__("Rock.png",1.2,1.5)
        
class Branch(Obstacles):
    def __init__(self):
        super().__init__("Leaves.png",2,2)

class Paber(Obstacles):  
   def __init__(self):
       super().__init__("Paber.png",2.5,5)

#Main_game
class Game(arc.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        #Objects
        self.character = Bird(self)
        self.rock = Rock()                    
        self.branch = Branch()
        self.paber = Paber()
        #background
        self.bg=arc.load_texture("Forest.png")
        #for_conditions
        self.branch_timer = t.time()
        self.paber_timer = t.time()
        self.randint_branch = r.randint(1,3)
        self.randint_paber = r.randint(2,4)
        self.counter = 0 
        self.texture_timer = 0
        self.time = 0
        self.game_time = 10
        self.seconds = self.game_time
        self.global_timer = t.time()
        self.lose = False
        self.win = False
        self.game=True
    def update(self,delta_time):
        if self.game:
            self.time+=delta_time
            if self.time>=1:
                self.seconds-=1
                self.time = 0
            self.rock.update()
            if t.time()-self.branch_timer>=self.randint_branch:
                self.branch.update()
            if t.time()-self.paber_timer>=self.randint_paber:
                self.paber.update()
            if arc.check_for_collision(self.character,self.rock) or arc.check_for_collision(self.character,self.branch) or arc.check_for_collision(self.character,self.paber):     
                    self.game = False
                    self.lose = True
                    self.character.change_angle-=1.5
                    self.character.center_y+=25
            if t.time()-self.texture_timer>=0.2:
                self.texture_timer=0
                self.character.set_texture(2) 
            if t.time()-self.global_timer>=self.game_time:
                self.win = True
                self.game = False
        if not self.game and self.lose:
            self.character.set_texture(3)
        if not self.win:
            if self.character.bottom>-500:
                self.character.update()
    def on_draw(self):
        arc.draw_texture_rectangle(width/2,height/2,width,height,self.bg)
        self.character.draw()
        self.rock.draw()
        if self.game:
            arc.draw_text(f"Try to survive {self.seconds} sec",width/2+135,height/2+200,arc.color.RED,font_size=14)
        if t.time()-self.branch_timer>=self.randint_branch:
            self.branch.draw()
        if t.time()-self.paber_timer>=self.randint_paber:
                self.paber.draw()
        if self.lose == True:
            arc.draw_text("You lost!",width/2-60,height/2,arc.color.RED,font_size=20)
        if self.win == True:
            arc.draw_text("You won!",width/2-60,height/2,arc.color.RED,font_size=20)
    def on_key_press(self,symbol,modifiers):
       if self.game:
        if symbol == arc.key.SPACE and self.character.cooldown==False:
            self.character.change_y = jump
            self.character.cooldown = True
            self.character.timer = t.time()
            self.character.set_texture(1)
            self.texture_timer = t.time()                       
window = Game(width,height,title)   
arc.run()
