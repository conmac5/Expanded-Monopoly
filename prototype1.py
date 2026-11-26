
#Prototype 1 code for my NEA. This includes registration and logging into a account.

import pygame
from pathlib import Path
import csv
import os
import hashlib
import secrets

USERS_FILE = Path(__file__).with_name("users.csv")

pygame.init()

clock = pygame.time.Clock()
screen = None

#Window screen setup
screen_width = 1400
screen_height = 950

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

#Create a salted hash for storing and checking passwords
def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

#Register a new account
def register(username, password, password2):
    #Make sure all boxes have something in them
    if not username or not password or not password2:
        return False, "Please fill in all boxes!"

    #Check that both passwords are the same
    if password != password2:
        return False, "Passwords do not match!"

    #Password strength test
    if len(password) < 8:
        return False, "Password length is too short"

    #Check whether the username already exists
    if USERS_FILE.exists():
        with open(USERS_FILE, mode="r", newline="") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) >= 1 and row[0] == username:
                    return False, "Username already exists!"

    #Add the new account to the CSV
    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    with open(USERS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        #Username, password hash, salt, number of wins
        writer.writerow([username, password_hash, salt, 0])

    return True, "Account created! Please login."

#Login to an existing account
def login(username, password):
    # Check if the CSV file exists
    if not USERS_FILE.exists():
        return False

    #Open the CSV file
    with open(USERS_FILE, mode="r", newline="") as f:
        reader = csv.reader(f)

        #Check every row
        for row in reader:
            if not row or row[0] != username:
                continue

            #Support the existing username,password,wins format
            if len(row) == 3:
                #Older Prototype 1 files stored the password as plain text.
                if row[1] == password:
                    return True

                #Also allow the fixed-salt hash used in an earlier version.
                if row[1] == hash_password(password, "5gz"):
                    return True

            #Check username and password using the secure format
            if len(row) >= 4:
                salt = row[2]
                entered_hash = hash_password(password, salt)
                return secrets.compare_digest(entered_hash, row[1])

    return False

#Get the usernames and win totals from the CSV
#Supports both the older username,password,wins and the newer hashed-password format
def get_wins():
    players = []

    if not USERS_FILE.exists():
        return players

    with open(USERS_FILE, mode="r", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) >= 4:
                username = row[0]
                wins_value = row[3]
            elif len(row) >= 3:
                username = row[0]
                wins_value = row[2]
            else:
                continue

            try:
                wins = int(wins_value)
            except ValueError:
                wins = 0

            players.append((username, wins))

    return players

#Add one win to the account's win total
def add_win(username):
    if not USERS_FILE.exists():
        return

    rows = []

    with open(USERS_FILE, mode="r", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            if row and row[0] == username:
                if len(row) >= 4:
                    wins_index = 3
                elif len(row) >= 3:
                    wins_index = 2
                else:
                    rows.append(row)
                    continue

                try:
                    row[wins_index] = str(int(row[wins_index]) + 1)
                except ValueError:
                    row[wins_index] = "1"

            rows.append(row)

    with open(USERS_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

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
register_button = Button(590,300,register_btn_img,1)
login_button = Button(590,410,login_btn_img,1)
instruction_button = Button(590,520,instruction_btn_img,1)
create_account_button = Button(590,660,create_account_btn_img,1)
login_submit_button = Button(590,610,login_submit_btn_img,1)
back_button = Button(20,20,back_btn_img,1)

#Create input boxes

#Registration boxes
register_username_box = InputBox(570,340,300,50)
register_password_box = InputBox(570,440,300,50)
register_password2_box = InputBox(570,540,300,50)

#Login boxes
login_username_box = InputBox(570,380,300,50)
login_password_box = InputBox(570,480,300,50)


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
def main(login_only=False):
    global run, screen, screen_state, message, message_colour, logged_in_username

    run = True
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Monopoly - Login/Registration")

    while run:
        #When Prototype 2 is using this login UI, return the authenticated player to it.
        if login_only and screen_state == "game":
            return logged_in_username

        #Fill background
        screen.fill(background_colour)

        #Options menu
        if screen_state == "menu":
            draw_text("Monopoly Expanded",font,white_text,500,180)

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
            draw_text("REGISTER",font,white_text,580,210)

            #Labels
            draw_text("Username:",small_font,white_text,430,350)
            draw_text("Password:",small_font,white_text,430,450)
            draw_text("Confirm:",small_font,white_text,430,550)

            #Draw input boxes
            register_username_box.draw(screen)
            register_password_box.draw(screen,password=True)
            register_password2_box.draw(screen,password=True)

            #Display message
            if message != "":
                draw_text(message,small_font,message_colour,430,620)

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
            draw_text("LOGIN",font,white_text,610,270)

            #Labels
            draw_text("Username:",small_font,white_text,430,400)
            draw_text("Password:",small_font,white_text,430,500)

            #Draw input boxes
            login_username_box.draw(screen)
            login_password_box.draw(screen,password=True)

            #Display message
            if message != "":
                draw_text(message,small_font,message_colour,430,570)

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
            draw_text("INSTRUCTIONS",font,white_text,530,210)
            #Instructions screen will go here

            #Back button
            if back_button.draw(screen):
                screen_state = "menu"
                message = ""

        #Game screen
        elif screen_state == "game":
            draw_text("Options screen",font,white_text,550,400)
            draw_text("Logged in as: " + logged_in_username,small_font,white_text,550,470)

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
        clock.tick(60)
        pygame.display.update()

    return None

# Run the login screens and return the username when login succeeds.
def authenticate():
    global run, screen_state, message, message_colour, logged_in_username

    run = True
    screen_state = "menu"
    message = ""
    message_colour = white
    logged_in_username = ""

    register_username_box.text = ""
    register_password_box.text = ""
    register_password2_box.text = ""
    login_username_box.text = ""
    login_password_box.text = ""

    return main(login_only=True)

#Close pygame
if __name__ == "__main__":
    main()
    pygame.quit()
