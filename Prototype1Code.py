#Prototype 1 code for my NEA. This includes registration and logging into a account.

import pygame
from pathlib import Path
import csv
import os
USERS_FILE = Path(__file__).with_name("users.csv")
import hashlib

pygame.init() 

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, mode="r", newline="") as f:

#Window screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monopoly - Login/Registration") 

#Colours
dark_bg = (30, 30, 30)
background_colour = (52, 78, 91)
white_text = (240, 240, 240)
grey_border = (180, 180, 180)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 80, 80)
green = (80, 255, 80) 

#Fonts
font = pygame.font.SysFont("arialblack", 40)
small_font = pygame.font.SysFont("Arial", 25) 

#Drawing texts
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y)) 

#CSV functions 

#Register a new account 
def register(username, password, password2): 

    #Make sure all boxes have something in them 
    if username == "" or password == "" or password2 == "": 
       return False, "Please fill in all boxes!" 
 
    #Check that both passwords are the same 
    if password != password2: 
       return False, "Passwords do not match!" 
    #Password strength test
    if len(password) < 8 or len(password2) < 8:
        return False, "Password length is too short"
    
    #Check whether the username already exists 
    if os.path.exists("users.csv"): 
       with open("users.csv", mode="r", newline="") as f: 
           reader = csv.reader(f) 
           for row in reader: 
               if len(row) >= 1: 
                    if row[0] == username: 
                       return False, "Username already exists!" 
 
    #Add the new account to the CSV
                    
    with open("users.csv", mode="a", newline="") as f:
        writer = csv.writer(f)
        #Hashing the password
        salt = '5gz'
        pwd_salt = salt + password
        hashed = hashlib.sha256(pwd_salt.encode())
        print(hashed.hexdigest())
    
        #Username, password, number of wins 
        writer.writerow([username, password, 0]) 
    return True, "Account created! Please login." 
 

#Login to an existing account
def login(username, password): 

    # Check if the CSV file exists 
    if not os.path.exists("users.csv"): 
       return False 
     
    #Open the CSV file 
    with open("users.csv", mode="r", newline="") as f: 
           reader = csv.reader(f) 
         
           #Check every row 
           for row in reader: 
         
               if len(row) >= 2: 
                   #Check username and password 
                   if row[0] == username and row[1] == password: 
                       return True 
         
    return False
 

#Create button images
def create_button_image(text,width,height,bg_colour,text_colour,border_colour): 
    #Create transparent surface
    surface = pygame.Surface((width, height),pygame.SRCALPHA)
    #Draw background
    pygame.draw.rect(surface,bg_colour,(0, 0, width, height))
    #Draw border
    pygame.draw.rect(surface,border_colour,(0, 0, width, height),4)
    #Create button font
    button_font = pygame.font.SysFont("Arial",28,bold=True)
    #Render button text
    text_surface = button_font.render(text.upper(),True,text_colour)
    #Centre text
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface,text_rect)
    return surface 

#Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False 

        #Get mouse position 
        pos = pygame.mouse.get_pos() 
         
        #Check if mouse is over button 
        if self.rect.collidepoint(pos): 
            #Check if left mouse button has been pressed 
            if pygame.mouse.get_pressed()[0] == 1: 
                if self.clicked == False: 
                    self.clicked = True 
                    action = True 
         
           #Reset clicked when mouse is released 
        if pygame.mouse.get_pressed()[0] == 0: 
            self.clicked = False 
         
        #Draw button 
        surface.blit(self.image,(self.rect.x,self.rect.y)) 
        return action
     

#Input box class
class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = ""
        self.active = False 

    def draw(self, screen, password=False): 
       #Change colour when box is selected 
       if self.active: 
           colour = white 
       else: 
           colour = (190, 190, 190) 
     
       #Draw box 
       pygame.draw.rect(screen,colour,self.rect) 
     
       #Draw black border 
       pygame.draw.rect(screen,black,self.rect,2) 
     
       #Hide password 
       if password: 
           display_text = "*" * len(self.text) 
       else: 
           display_text = self.text 
     
       #Render text 
       text_surface = small_font.render(display_text,True,black) 
     
       #Draw text inside box 
       screen.blit(text_surface,(self.rect.x + 10,self.rect.y + 10)) 
 
    def handle_event(self, event): 
       #Mouse clicked 
       if event.type == pygame.MOUSEBUTTONDOWN: 
           #Activate the box if clicked 
           if self.rect.collidepoint(event.pos): 
               self.active = True 
           else: 
               self.active = False 
     
       #Keyboard input 
       if event.type == pygame.KEYDOWN: 
           if self.active: 
               #Backspace 
               if event.key == pygame.K_BACKSPACE: 
                   self.text = self.text[:-1] 
               #Add typed character 
               else: 
                   #Prevent extremely long usernames/passwords 
                   if len(self.text) < 25: 
                       self.text += event.unicode 
 

#Create button images
register_btn_img = create_button_image("Register",220,80,dark_bg,white_text,grey_border)
login_btn_img = create_button_image("Login",220,80,dark_bg,white_text,grey_border)
instruction_btn_img = create_button_image("Instruction",220,80,dark_bg,white_text,grey_border)
create_account_btn_img = create_button_image("Create Account",220,60,dark_bg,white_text,grey_border)
login_submit_btn_img = create_button_image("Login",220,60,dark_bg,white_text,grey_border)
back_btn_img = create_button_image("Back",150,50,dark_bg,white_text,grey_border) 

#Create button objects
register_button = Button(290,150,register_btn_img,1)
login_button = Button(290,250,login_btn_img,1)
instruction_button = Button(290,350,instruction_btn_img,1)
create_account_button = Button(290,430,create_account_btn_img,1)
login_submit_button = Button(290,330,login_submit_btn_img,1)
back_button = Button(20,20,back_btn_img,1) 

#Create input boxes

#Registration boxes
register_username_box = InputBox(300,140,220,45)
register_password_box = InputBox(300,220,220,45)
register_password2_box = InputBox(300,300,220,45) 

#Login boxes
login_username_box = InputBox(300,170,220,45) 
login_password_box = InputBox(300,250,220,45)

#Instructions box
instruction_box = InputBox(300,170,220,45)

#Variables
run = True 

#Which screen are we currently on? 
#Options:"menu", "register", "login", "game" 

screen_state = "menu" 

#Message displayed on register/login screen
message = "" 
message_colour = white 

#Store the username of the person who logged in
logged_in_username = "" 

#Game Loop
while run:
    #Fill background
    screen.fill(background_colour)
    #Options menu
    if screen_state == "menu":
        draw_text("Monopoly Expanded",font,white_text,200,50)
        #Register button
        if register_button.draw(screen):
            screen_state = "register"
            message = "" 

        #Login button 
        if login_button.draw(screen): 
            screen_state = "login" 
            message = "" 
         
         
        #Instructions button 
        if instruction_button.draw(screen): 
            #I will add my instructions screen here when done
            screen_state = "Instructions"
            message = ""
            print("Instructions clicked!") 
     
    #Register screen 
    elif screen_state == "register": 
       draw_text("REGISTER",font,white_text,300,50) 
       #Labels         
       draw_text("Username:",small_font,white_text,130,150) 
       draw_text("Password:",small_font,white_text,130,230) 
       draw_text("Confirm:",small_font,white_text,130,310) 
     
       #Draw input boxes 
       register_username_box.draw(screen) 
       register_password_box.draw(screen,password=True) 
       register_password2_box.draw(screen,password=True) 
     
       #Display message 
       if message != "": 
           draw_text(message,small_font,message_colour,150,380) 
     
       #Create account button 
       if create_account_button.draw(screen): 
           success, result = register(register_username_box.text,register_password_box.text,register_password2_box.text) 
           message = result 
           if success: 
               message_colour = green 
     
               #Clear boxes 
               register_username_box.text = "" 
               register_password_box.text = "" 
               register_password2_box.text = "" 
     
               #Go to login screen 
               screen_state = "login" 
           else: 
               message_colour = red 
     
       #Back button 
       if back_button.draw(screen): 
           screen_state = "menu" 
           message = "" 
     
    #Login screen 
    elif screen_state == "login": 
       draw_text("LOGIN",font,white_text,320,70) 
       #Labels 
       draw_text("Username:",small_font,white_text,130,180) 
       draw_text("Password:",small_font,white_text,130,260) 
     
       #Draw input boxes 
       login_username_box.draw(screen) 
       login_password_box.draw(screen,password=True) 
     
     
       #Display message 
       if message != "": 
           draw_text(message,small_font,message_colour,180,410) 
     
       #Login button 
       if login_submit_button.draw(screen): 
           username = login_username_box.text 
           password = login_password_box.text 
           #Check CSV 
           if login(username, password): 
               logged_in_username = username 
               message = "Login successful!" 
               message_colour = green 
               #Clear login boxes 
               login_username_box.text = "" 
               login_password_box.text = "" 
               #Go to game 
               screen_state = "game" 
           else: 
               message = "Incorrect username or password!" 
               message_colour = red 
     
       #Back button 
       if back_button.draw(screen): 
           screen_state = "menu" 
           message = "" 

       #Instructions screen
       elif screen_state == "Instructions":
           #Instructions screen will go here
           print("Insturction clicked")
           
           #Display message
           draw_text(message,small_font,message_colour,180,410) 
    #Game screen 
    elif screen_state == "game": 
       draw_text("Options screen",font,white_text,180,200) 
       draw_text("Logged in as: " + logged_in_username,small_font,white_text,270,270)
        
     
     
    #Event handler 
    for event in pygame.event.get(): 
       #Close window 
       if event.type == pygame.QUIT: 
           run = False 
     
       #Registration input 
       if screen_state == "register": 
           register_username_box.handle_event(event) 
           register_password_box.handle_event(event) 
           register_password2_box.handle_event(event) 
     
       #Login input 
       if screen_state == "login": 
           login_username_box.handle_event(event) 
           login_password_box.handle_event(event)

            
     
    #Update display 
    pygame.display.update() 


#Close pygame
pygame.quit() 

