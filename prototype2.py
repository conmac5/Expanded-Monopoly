#Prototype 2 Code of NEA. This includes game-mode selection, checking wins and piece selection, as well as moving on to the actual main board.
import pygame
import prototype1.py
pygame.init()

if __name__ == "__main__":
    main()

success, message = prototype1.register(username, password, password2)
logged_in = prototype1.login(username, password)
players = prototype1.get_wins()
prototype1.add_win(username)
prototype1.getwins()
#WINDOW SETUP

screen_width = 1000
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monopoly")

clock = pygame.time.Clock()

#COLOURS

dark_bg = (30, 30, 30)
background_colour = (52, 78, 91)

white_text = (240, 240, 240)
grey_border = (180, 180, 180)

black = (0, 0, 0)
white = (255, 255, 255)

red = (255, 80, 80)
green = (80, 255, 80)

yellow = (245, 205, 60)
blue = (60, 130, 230)
light_blue = (100, 190, 240)

brown = (120, 70, 35)
pink = (240, 130, 180)

light_grey = (220, 220, 220)
dark_grey = (80, 80, 80)
silver = (192,192,192)
# FONTS

font = pygame.font.SysFont("arialblack", 40)
title_font = pygame.font.SysFont("arialblack", 50)

small_font = pygame.font.SysFont("Arial", 25)
tiny_font = pygame.font.SysFont("Arial", 19)

#TEXT FUNCTIONS

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))


def draw_centered_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


# BUTTON CLASS

def create_button_image(text,width,height,bg_colour,text_colour,border_colour):

    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    pygame.draw.rect(surface,bg_colour,(0, 0, width, height))

    pygame.draw.rect(surface,border_colour,(0, 0, width, height),4)

    button_font = pygame.font.SysFont("Arial",25,bold=True)

    text_surface = button_font.render(text.upper(),True,text_colour)

    text_rect = text_surface.get_rect(center=(width // 2, height // 2))

    surface.blit(text_surface, text_rect)

    return surface


class Button:

    def __init__(self, x, y, image, scale=1):

        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self, surface):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1:

                if self.clicked is False:

                    self.clicked = True
                    action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image,(self.rect.x, self.rect.y))

        return action


# INPUT BOX

class InputBox:

    def __init__(self, x, y, width, height):

        self.rect = pygame.Rect(x,y,width,height)

        self.text = ""
        self.active = False

    def draw(self, screen, password=False):

        if self.active:
            colour = white
        else:
            colour = (190, 190, 190)

        pygame.draw.rect(screen,colour,self.rect)

        pygame.draw.rect(screen,black,self.rect,2)

        if password:
            display_text = "*" * len(self.text)
        else:
            display_text = self.text

        text_surface = small_font.render(display_text,True,black)
        screen.blit(text_surface,(self.rect.x + 10,self.rect.y + 8))

    #handle_event is now inside InputBox

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:

            if self.active:

                if event.key == pygame.K_BACKSPACE:

                    self.text = self.text[:-1]

                elif event.key == pygame.K_RETURN:

                    pass

                elif len(self.text) < 25:

                    self.text += event.unicode


#BUTTON IMAGES
instruction_btn_img = create_button_image("Instructions",220,70,dark_bg,white_text,grey_border)
back_btn_img = create_button_image("Back",150,50,dark_bg,white_text,grey_border)

wins_btn_img = create_button_image(
    "Check Wins",
    220,
    60,
    dark_bg,
    white_text,
    grey_border
)

logout_btn_img = create_button_image(
    "Logout",
    150,
    50,
    dark_bg,
    white_text,
    grey_border
)


# BUTTON OBJECTS

instruction_button = Button(
    390,
    350,
    instruction_btn_img
)

back_button = Button(
    20,
    20,
    back_btn_img
)

wins_button = Button(
    390,
    470,
    wins_btn_img
)

logout_button = Button(
    820,
    20,
    logout_btn_img
)

# MONOPOLY PIECES

pieces = [
    "Scottie Dog",
    "Top Hat",
    "Battleship",
    "Boot",
    "Thimble",
    "Iron",
    "Racing Car",
    "Wheelbarrow"
]

selected_piece = None


# DRAW MONOPOLY PIECES

def draw_piece(piece, x, y, scale=1):

    colour = (70, 70, 70)

    # Scottie Dog

    if piece == "Scottie Dog":

        pygame.draw.ellipse(
            screen,
            silver,
            (
                x - 25 * scale,
                y - 5 * scale,
                45 * scale,
                25 * scale
            )
        )

        pygame.draw.circle(
            screen,
            silver,
            (
                int(x + 18 * scale),
                int(y - 5 * scale)
            ),
            int(13 * scale)
        )

        pygame.draw.polygon(
            screen,
            silver,
            [
                (
                    x + 25 * scale,
                    y - 10 * scale
                ),
                (
                    x + 35 * scale,
                    y - 18 * scale
                ),
                (
                    x + 28 * scale,
                    y
                )
            ]
        )

        pygame.draw.line(
            screen,
            silver,
            (
                x - 15 * scale,
                y + 15 * scale
            ),
            (
                x - 15 * scale,
                y + 30 * scale
            ),
            max(2, int(5 * scale))
        )

        pygame.draw.line(
            screen,
            silver,
            (
                x + 5 * scale,
                y + 15 * scale
            ),
            (
                x + 5 * scale,
                y + 30 * scale
            ),
            max(2, int(5 * scale))
        )

    # Top Hat

    elif piece == "Top Hat":

        pygame.draw.ellipse(
            screen,
            colour,
            (
                x - 35 * scale,
                y + 20 * scale,
                70 * scale,
                20 * scale
            )
        )

        pygame.draw.rect(
            screen,
            colour,
            (
                x - 25 * scale,
                y - 35 * scale,
                50 * scale,
                60 * scale
            )
        )

        pygame.draw.rect(
            screen,
            dark_grey,
            (
                x - 25 * scale,
                y + 5 * scale,
                50 * scale,
                8 * scale
            )
        )

    # Battleship

    elif piece == "Battleship":

        pygame.draw.polygon(
            screen,
            colour,
            [
                (
                    x - 45 * scale,
                    y + 20 * scale
                ),
                (
                    x + 35 * scale,
                    y + 20 * scale
                ),
                (
                    x + 50 * scale,
                    y
                ),
                (
                    x - 30 * scale,
                    y
                )
            ]
        )

        pygame.draw.rect(
            screen,
            colour,
            (
                x - 20 * scale,
                y - 20 * scale,
                40 * scale,
                20 * scale
            )
        )

        pygame.draw.line(
            screen,
            colour,
            (
                x,
                y - 20 * scale
            ),
            (
                x,
                y - 40 * scale
            ),
            max(2, int(5 * scale))
        )

    # Boot

    elif piece == "Boot":

        pygame.draw.ellipse(
            screen,
            colour,
            (
                x - 25 * scale,
                y + 15 * scale,
                65 * scale,
                25 * scale
            )
        )

        pygame.draw.polygon(
            screen,
            colour,
            [
                (
                    x - 20 * scale,
                    y + 20 * scale
                ),
                (
                    x - 10 * scale,
                    y - 45 * scale
                ),
                (
                    x + 15 * scale,
                    y - 45 * scale
                ),
                (
                    x + 15 * scale,
                    y + 20 * scale
                )
            ]
        )

    # Thimble

    elif piece == "Thimble":

        pygame.draw.ellipse(
            screen,
            colour,
            (
                x - 30 * scale,
                y - 35 * scale,
                60 * scale,
                20 * scale
            )
        )

        pygame.draw.polygon(
            screen,
            colour,
            [
                (
                    x - 30 * scale,
                    y - 25 * scale
                ),
                (
                    x + 30 * scale,
                    y - 25 * scale
                ),
                (
                    x + 20 * scale,
                    y + 35 * scale
                ),
                (
                    x - 20 * scale,
                    y + 35 * scale
                )
            ]
        )

    # Iron

    elif piece == "Iron":

        pygame.draw.polygon(
            screen,
            colour,
            [
                (
                    x - 40 * scale,
                    y + 25 * scale
                ),
                (
                    x + 40 * scale,
                    y + 25 * scale
                ),
                (
                    x + 15 * scale,
                    y - 15 * scale
                ),
                (
                    x - 15 * scale,
                    y - 15 * scale
                )
            ]
        )

        pygame.draw.arc(
            screen,
            colour,
            (
                x - 25 * scale,
                y - 40 * scale,
                50 * scale,
                50 * scale
            ),
            0,
            3.14,
            max(2, int(6 * scale))
        )

    # Racing Car

    elif piece == "Racing Car":

        pygame.draw.rect(
            screen,
            red,
            (
                x - 40 * scale,
                y - 10 * scale,
                80 * scale,
                30 * scale
            )
        )

        pygame.draw.polygon(
            screen,
            red,
            [
                (
                    x - 20 * scale,
                    y - 10 * scale
                ),
                (
                    x - 5 * scale,
                    y - 30 * scale
                ),
                (
                    x + 25 * scale,
                    y - 30 * scale
                ),
                (
                    x + 35 * scale,
                    y - 10 * scale
                )
            ]
        )

        pygame.draw.circle(
            screen,
            black,
            (
                int(x - 25 * scale),
                int(y + 20 * scale)
            ),
            int(10 * scale)
        )

        pygame.draw.circle(
            screen,
            black,
            (
                int(x + 25 * scale),
                int(y + 20 * scale)
            ),
            int(10 * scale)
        )

    # Wheelbarrow

    elif piece == "Wheelbarrow":

        pygame.draw.polygon(
            screen,
            red,
            [
                (
                    x - 35 * scale,
                    y - 10 * scale
                ),
                (
                    x + 35 * scale,
                    y - 10 * scale
                ),
                (
                    x + 15 * scale,
                    y + 25 * scale
                ),
                (
                    x - 20 * scale,
                    y + 25 * scale
                )
            ]
        )

        pygame.draw.line(
            screen,
            black,
            (
                x + 15 * scale,
                y + 25 * scale
            ),
            (
                x + 40 * scale,
                y + 45 * scale
            ),
            max(2, int(5 * scale))
        )

        pygame.draw.circle(
            screen,
            black,
            (
                int(x - 25 * scale),
                int(y + 30 * scale)
            ),
            int(9 * scale)
        )


# PIECE BUTTON RECTANGLES

piece_rects = []

for i in range(len(pieces)):

    column = i % 4
    row = i // 4

    x = 60 + column * 230
    y = 160 + row * 220

    piece_rects.append(
        pygame.Rect(
            x,
            y,
            190,
            180
        )
    )


# DRAW PIECE SELECTION SCREEN

def draw_piece_selection():

    draw_centered_text(
        "CHOOSE YOUR MONOPOLY PIECE",
        title_font,
        white_text,
        screen_width // 2,
        65
    )

    draw_centered_text(
        "Click a piece to select it",
        small_font,
        white_text,
        screen_width // 2,
        115
    )

    mouse_pos = pygame.mouse.get_pos()

    for i, piece in enumerate(pieces):

        rect = piece_rects[i]

        border_colour = grey_border

        if selected_piece == piece:
            border_colour = yellow

        elif rect.collidepoint(mouse_pos):
            border_colour = white

        pygame.draw.rect(
            screen,
            (45, 45, 45),
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            border_colour,
            rect,
            4,
            border_radius=10
        )

        draw_piece(
            piece,
            rect.centerx,
            rect.centery - 15,
            1
        )

        draw_centered_text(
            piece,
            tiny_font,
            white_text,
            rect.centerx,
            rect.bottom - 25
        )

    if selected_piece is not None:

        draw_centered_text(
            "Selected: " + selected_piece,
            small_font,
            yellow,
            screen_width // 2,
            625
        )


# GAME MODE SELECTION

game_modes = [
    "Speed Monopoly",
    "Original Monopoly",
    "First to Get to Go"
]

selected_mode = None

mode_rects = []

for i in range(3):

    mode_rects.append(
        pygame.Rect(
            150 + i * 270,
            230,
            230,
            180
        )
    )


def draw_mode_selection():

    draw_centered_text(
        "CHOOSE GAME MODE",
        title_font,
        white_text,
        screen_width // 2,
        80
    )

    draw_centered_text(
        "Select how you want to play",
        small_font,
        white_text,
        screen_width // 2,
        135
    )

    mouse_pos = pygame.mouse.get_pos()

    for i, mode in enumerate(game_modes):

        rect = mode_rects[i]

        if selected_mode == mode:
            border_colour = yellow

        elif rect.collidepoint(mouse_pos):
            border_colour = white

        else:
            border_colour = grey_border

        pygame.draw.rect(
            screen,
            dark_bg,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            border_colour,
            rect,
            4,
            border_radius=10
        )

        draw_centered_text(
            mode,
            small_font,
            white_text,
            rect.centerx,
            rect.centery - 15
        )

        if mode == "Speed Monopoly":

            description = "A faster version of Monopoly"

        elif mode == "Original Monopoly":

            description = "Classic Monopoly rules"

        else:

            description = "First player to pass GO wins"

        draw_centered_text(
            description,
            tiny_font,
            light_grey,
            rect.centerx,
            rect.centery + 35
        )

    if selected_mode is not None:

        draw_centered_text(
            "Selected: " + selected_mode,
            small_font,
            yellow,
            screen_width // 2,
            500
        )


# GAME START SCREEN

def draw_game_start():

    draw_centered_text(
        "GAME READY",
        title_font,
        white_text,
        screen_width // 2,
        100
    )

    draw_centered_text(
        "Player: " + logged_in_username,
        small_font,
        white_text,
        screen_width // 2,
        190
    )

    draw_centered_text(
        "Mode: " + selected_mode,
        small_font,
        white_text,
        screen_width // 2,
        240
    )

    draw_centered_text(
        "Piece: " + selected_piece,
        small_font,
        white_text,
        screen_width // 2,
        290
    )

    draw_piece(
        selected_piece,
        screen_width // 2,
        390,
        1.5
    )

    draw_centered_text(
        "The actual Monopoly board can now be started.",
        tiny_font,
        light_grey,
        screen_width // 2,
        500
    )


# GAME BUTTONS

start_game_img = create_button_image(
    "Start Game",
    220,
    60,
    dark_bg,
    white_text,
    grey_border
)

continue_img = create_button_image(
    "Continue",
    220,
    60,
    dark_bg,
    white_text,
    grey_border
)

start_game_button = Button(
    390,
    550,
    start_game_img
)

continue_button = Button(
    390,
    550,
    continue_img
)


# WIN SCREEN

def draw_wins_screen():

    draw_centered_text(
        "MONOPOLY WIN RECORDS",
        title_font,
        white_text,
        screen_width // 2,
        70
    )

    draw_centered_text(
        "Wins are read from users.csv",
        small_font,
        light_grey,
        screen_width // 2,
        125
    )

    table_x = 250
    table_y = 180
    table_width = 500

    pygame.draw.rect(
        screen,
        dark_bg,
        (
            table_x,
            table_y,
            table_width,
            60
        )
    )

    pygame.draw.rect(
        screen,
        grey_border,
        (
            table_x,
            table_y,
            table_width,
            60
        ),
        2
    )

    draw_text(
        "PLAYER",
        small_font,
        white_text,
        table_x + 40,
        table_y + 15
    )

    draw_text(
        "WINS",
        small_font,
        white_text,
        table_x + 360,
        table_y + 15
    )

    players = get_wins()

    y = table_y + 60

    if len(players) == 0:

        draw_centered_text(
            "No players found.",
            small_font,
            red,
            screen_width // 2,
            y + 40
        )

    else:

        for username, wins in players:

            pygame.draw.rect(
                screen,
                (45, 45, 45),
                (
                    table_x,
                    y,
                    table_width,
                    55
                )
            )

            pygame.draw.rect(
                screen,
                grey_border,
                (
                    table_x,
                    y,
                    table_width,
                    55
                ),
                1
            )

            text_colour = (
                yellow
                if username == logged_in_username
                else white_text
            )

            draw_text(
                username,
                small_font,
                text_colour,
                table_x + 40,
                y + 12
            )

            draw_text(
                str(wins),
                small_font,
                text_colour,
                table_x + 365,
                y + 12
            )

            y += 55

            if y > 600:
                break


# VARIABLES

run = True

# Possible screens:
# menu
# game_menu
# mode_selection
# piece_selection
# game_ready
# wins
# instructions

screen_state = "menu"

message = ""
message_colour = white

logged_in_username = ""



# MAIN GAME LOOP


while run:


    # EVENT HANDLING


    for event in pygame.event.get():

        # QUIT GAME

        if event.type == pygame.QUIT:

            run = False

        # MODE SELECTION

        if (
            screen_state == "mode_selection"
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            for i, rect in enumerate(mode_rects):

                if rect.collidepoint(event.pos):

                    selected_mode = game_modes[i]

        # PIECE SELECTION

        if (
            screen_state == "piece_selection"
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            for i, rect in enumerate(piece_rects):

                if rect.collidepoint(event.pos):

                    selected_piece = pieces[i]



    # DRAW SCREEN


    screen.fill(background_colour)


    # MAIN MENU

    if screen_state == "menu":

        draw_centered_text(
            "MONOPOLY",
            title_font,
            white_text,
            screen_width // 2,
            80
        )


        if back_button.draw(screen):

            screen_state = "menu"
            message = ""


    # GAME MENU

    elif screen_state == "game_menu":

        draw_centered_text(
            "MONOPOLY GAME",
            title_font,
            white_text,
            screen_width // 2,
            80
        )

        draw_centered_text(
            "Logged in as: " + logged_in_username,
            small_font,
            white_text,
            screen_width // 2,
            145
        )

        if start_game_button.draw(screen):

            selected_mode = None
            selected_piece = None

            screen_state = "mode_selection"

        if wins_button.draw(screen):

            screen_state = "wins"

        if logout_button.draw(screen):

            logged_in_username = ""
            selected_mode = None
            selected_piece = None

            screen_state = "menu"


    # MODE SELECTION

    elif screen_state == "mode_selection":

        draw_mode_selection()

        if back_button.draw(screen):

            screen_state = "game_menu"

        if selected_mode is not None:

            if continue_button.draw(screen):

                selected_piece = None
                screen_state = "piece_selection"


    # PIECE SELECTION
    elif screen_state == "piece_selection":
        draw_piece_selection()
        if back_button.draw(screen):
            screen_state = "mode_selection"
        if selected_piece is not None:
            if continue_button.draw(screen):
                screen_state = "game_ready"

    # GAME READY
    elif screen_state == "game_ready":
        draw_game_start()
        if back_button.draw(screen):
            screen_state = "piece_selection"
        if start_game_button.draw(screen):
            # The actual Monopoly board will eventually
            # be launched here.
            screen_state = "game_menu"


    # WINS
    elif screen_state == "wins":
        draw_wins_screen()
        if back_button.draw(screen):
            screen_state = "game_menu"
    # INSTRUCTIONS
    elif screen_state == "instructions":
        draw_centered_text(
            "INSTRUCTIONS",
            title_font,
            white_text,
            screen_width // 2,
            70
        )

        instructions = [
            "1. Create an account or login.",
            "2. Select a Monopoly game mode.",
            "3. Select your Monopoly playing piece.",
            "4. Start the game.",
            "5. Your wins are stored in users.csv.",
            "6. Check Wins displays the current win records."
        ]

        y = 170

        for instruction in instructions:

            draw_text(
                instruction,
                small_font,
                white_text,
                180,
                y
            )

            y += 55

        if back_button.draw(screen):

            screen_state = "menu"

    # UPDATE DISPLAY

    pygame.display.flip()

    # Limit game to 60 FPS

    clock.tick(60)

# CLOSE PYGAME


pygame.quit()
