
# PROTOTYPE 3 - MAIN MONOPOLY GAME

import random
import pygame
import prototype1

# BOARD SPACES
# Standard 40-space UK Monopoly board.

_BOARD = [
    ("GO", "go", None, 0, 0),
    ("Old Kent Road", "property", "brown", 60, 2),
    ("Community Chest", "chest", None, 0, 0),
    ("Whitechapel Road", "property", "brown", 60, 4),
    ("Income Tax", "tax", None, 0, 200),
    ("King's Cross Station", "railroad", "railroad", 200, 25),
    ("The Angel Islington", "property", "light blue", 100, 6),
    ("Chance", "chance", None, 0, 0),
    ("Euston Road", "property", "light blue", 100, 6),
    ("Pentonville Road", "property", "light blue", 120, 8),
    ("Jail / Just Visiting", "jail", None, 0, 0),
    ("Pall Mall", "property", "pink", 140, 10),
    ("Electric Company", "utility", "utility", 150, 0),
    ("Whitehall", "property", "pink", 140, 10),
    ("Northumberland Avenue", "property", "pink", 160, 12),
    ("Marylebone Station", "railroad", "railroad", 200, 25),
    ("Bow Street", "property", "orange", 180, 14),
    ("Community Chest", "chest", None, 0, 0),
    ("Marlborough Street", "property", "orange", 180, 14),
    ("Vine Street", "property", "orange", 200, 16),
    ("Free Parking", "free", None, 0, 0),
    ("The Strand", "property", "red", 220, 18),
    ("Chance", "chance", None, 0, 0),
    ("Fleet Street", "property", "red", 220, 18),
    ("Trafalgar Square", "property", "red", 240, 20),
    ("Fenchurch St Station", "railroad", "railroad", 200, 25),
    ("Leicester Square", "property", "yellow", 260, 22),
    ("Coventry Street", "property", "yellow", 260, 22),
    ("Water Works", "utility", "utility", 150, 0),
    ("Piccadilly", "property", "yellow", 280, 24),
    ("Go To Jail", "go_to_jail", None, 0, 0),
    ("Regent Street", "property", "green", 300, 26),
    ("Oxford Street", "property", "green", 300, 26),
    ("Community Chest", "chest", None, 0, 0),
    ("Bond Street", "property", "green", 320, 28),
    ("Liverpool Street Station", "railroad", "railroad", 200, 25),
    ("Chance", "chance", None, 0, 0),
    ("Park Lane", "property", "blue", 350, 35),
    ("Super Tax", "tax", None, 0, 100),
    ("Mayfair", "property", "blue", 400, 50),
]

# PROPERTY COLOURS

_GROUP_COLORS = {
    "brown": (145, 91, 55),
    "light blue": (120, 205, 230),
    "pink": (220, 115, 165),
    "orange": (235, 145, 55),
    "red": (220, 65, 65),
    "yellow": (240, 205, 70),
    "green": (55, 155, 90),
    "blue": (65, 105, 205),
    "railroad": (65, 65, 75),
    "utility": (90, 150, 155)
}

# PLAYER COLOURS

_PLAYER_COLORS = [
    (225, 75, 75),
    (65, 145, 230),
    (245, 190, 45),
    (80, 190, 120)
]


# PROPERTY NAME WRAPPING

def _wrapped_lines(text, font, width):
    """Split a property name into lines that fit inside a board tile."""

    words = text.split()
    lines = []
    current_line = ""

    for word in words:

        test_line = (current_line + " " + word).strip()

        if font.size(test_line)[0] <= width:
            current_line = test_line

        else:

            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# MAIN GAME FUNCTION

def run_game(screen, clock, username, piece="",
             mode="Original Monopoly", add_win=None):

    """Run a Monopoly game using the main application's display."""

    width, height = screen.get_size()

    background = (28, 48, 74)
    white = (245, 245, 245)
    muted = (205, 215, 218)

    panel = (19, 30, 49)
    accent = (220, 48, 58)

    # GAME MODES

    speed = mode == "Speed Monopoly"
    first_to_go = mode == "First to Get to Go"

    # PLAYER SETUP

    names = [
        username,
        "Alex (CPU)",
        "Sam (CPU)",
        "Taylor (CPU)"
    ]

    players = [
        {
            "name": n,
            "cash": 2000 if speed else 1500,
            "position": 0,
            "active": True,
            "color": _PLAYER_COLORS[i],
            "human": i == 0,
            "piece": piece if i == 0 else ""
        }
        for i, n in enumerate(names)
    ]

    # PROPERTY OWNERSHIP

    owner = [None] * 40

    # GAME VARIABLES

    current = 0
    rolled = False
    dice = (1, 1)

    message = "Roll the dice to begin your turn."

    game_over = False
    winner = None

    go_bonus = 300 if speed else 200

    # LARGER BOARD DIMENSIONS
    # The board uses the available screen space.

    cell = min(
        112,
        (height - 50) // 11,
        (width - 270) // 11
    )

    board_size = cell * 11

    board_x = max(
        235,
        (width - board_size) // 2 + 115
    )

    board_y = max(
        20,
        (height - board_size) // 2
    )

    # SIDEBAR

    sidebar = pygame.Rect(
        8, 8, 215, height - 16
    )

    menu_rect = pygame.Rect(
        20, height - 58, 190, 40
    )

    roll_rect = pygame.Rect(
        20, height - 220, 190, 42
    )

    buy_rect = pygame.Rect(
        20, height - 166, 190, 42
    )

    end_rect = pygame.Rect(
        20, height - 112, 190, 42
    )

    # FONTS

    title_font = pygame.font.SysFont(
        "arialblack", max(24, cell // 3)
    )

    heading_font = pygame.font.SysFont(
        "arialblack", max(16, cell // 6)
    )

    body_font = pygame.font.SysFont(
        "Arial", max(15, cell // 7)
    )

    tile_font = pygame.font.SysFont(
        "Arial", max(10, min(16, cell // 8)), bold=True
    )

    price_font = pygame.font.SysFont(
        "Arial", max(10, min(15, cell // 9))
    )

    button_font = pygame.font.SysFont(
        "Arial", 16, bold=True
    )

    # CPU TIMING

    cpu_deadline = pygame.time.get_ticks()

    # BUTTON DRAWING

    def draw_button(rect, label, enabled=True):

        color = (54, 105, 115) if enabled else (72, 78, 80)

        pygame.draw.rect(
            screen, color, rect, border_radius=6
        )

        pygame.draw.rect(
            screen, (185, 205, 207), rect, 2,
            border_radius=6
        )

        image = button_font.render(
            label, True,
            white if enabled else (150, 155, 155)
        )

        screen.blit(
            image, image.get_rect(center=rect.center)
        )

    # PROPERTY AND BOARD MECHANICS

    def resolve(index, total):

        nonlocal message, game_over, winner

        p = players[index]
        pos = p["position"]

        name, kind, group, price, rent = _BOARD[pos]

        # PROPERTY, RAILROAD AND UTILITY

        if kind in ("property", "railroad", "utility"):

            own = owner[pos]

            if own is None:

                if p["human"]:

                    message = f"{name} for £{price}: buy or end turn."

                elif p["cash"] >= price:

                    p["cash"] -= price
                    owner[pos] = index

                    message = f"{p['name']} bought {name}."

                else:

                    message = f"{p['name']} cannot afford {name}."

            elif own != index and players[own]["active"]:

                if kind == "utility":

                    count = sum(
                        o == own and _BOARD[i][1] == "utility"
                        for i, o in enumerate(owner)
                    )

                    due = total * (10 if count == 1 else 20)

                elif kind == "railroad":

                    count = sum(
                        o == own and _BOARD[i][1] == "railroad"
                        for i, o in enumerate(owner)
                    )

                    due = 25 * 2 ** max(0, count - 1)

                else:

                    due = rent

                    group_spaces = [
                        i for i, s in enumerate(_BOARD)
                        if s[1] == "property" and s[2] == group
                    ]

                    if all(owner[i] == own for i in group_spaces):
                        due *= 2

                paid = min(p["cash"], due)

                p["cash"] -= paid
                players[own]["cash"] += paid

                if paid < due:
                    p["active"] = False

                message = (
                    f"{p['name']} paid £{paid} rent "
                    f"to {players[own]['name']}."
                )

        # TAX

        elif kind == "tax":

            paid = min(p["cash"], rent)

            p["cash"] -= paid

            if paid < rent:
                p["active"] = False

            message = f"{p['name']} paid £{paid} tax."

        # CHANCE

        elif kind == "chance":

            text, amount = random.choice([
                ("Dividend", 100),
                ("Speeding fine", -50),
                ("Prize", 50),
                ("Repairs", -100)
            ])

            if amount < 0 and p["cash"] < -amount:

                p["active"] = False

            else:

                p["cash"] += amount

            message = f"Chance: {text} £{abs(amount)}."

        # COMMUNITY CHEST

        elif kind == "chest":

            amount = random.choice([
                50, 100, 150, -50, -100
            ])

            if amount < 0 and p["cash"] < -amount:

                p["active"] = False

            else:

                p["cash"] += amount

            message = (
                f"Community Chest: "
                f"{'collect' if amount >= 0 else 'pay'} "
                f"£{abs(amount)}."
            )

        # GO TO JAIL

        elif kind == "go_to_jail":

            p["position"] = 10

            message = f"{p['name']} was sent to Jail."

        elif kind == "jail":

            message = f"{p['name']} is just visiting Jail."

        # FREE PARKING

        elif kind == "free":

            message = f"{p['name']} landed on Free Parking."

    # CHECK FOR A WINNER

    def finish_check():

        nonlocal game_over, winner, message

        remaining = [
            i for i, p in enumerate(players)
            if p["active"]
        ]

        if len(remaining) <= 1:

            game_over = True

            winner = remaining[0] if remaining else None

            if winner is not None:

                message = players[winner]["name"] + " wins!"

            else:

                message = "Everyone is bankrupt."

            # Update Prototype 1's win records.

            if winner == 0 and add_win:

                add_win(username)

    # ROLL DICE

    def roll():

        nonlocal dice, rolled, message
        nonlocal game_over, winner

        if rolled or game_over:
            return

        dice = (
            random.randint(1, 6),
            random.randint(1, 6)
        )

        rolled = True

        p = players[current]

        total = sum(dice)

        old = p["position"]

        p["position"] = (old + total) % 40

        # PASSING GO

        if old + total >= 40:

            p["cash"] += go_bonus

            if first_to_go:

                game_over = True
                winner = current

                message = p["name"] + " passed GO and wins!"

                if current == 0 and add_win:
                    add_win(username)

                return

        message = (
            f"{p['name']} rolled "
            f"{dice[0]} + {dice[1]} = {total}."
        )

        resolve(current, total)

        finish_check()

    # END TURN AND ADVANCE PLAYER

    def advance():

        nonlocal current, rolled, message, cpu_deadline

        if game_over:
            return

        for _ in players:

            current = (current + 1) % len(players)

            if players[current]["active"]:
                break

        rolled = False

        message = f"{players[current]['name']}'s turn."

        cpu_deadline = pygame.time.get_ticks() + 700

        finish_check()

    # BOARD POSITIONS

    positions = []

    for i in range(40):

        if i <= 10:

            col, row = 10 - i, 10

        elif i <= 20:

            col, row = 0, 10 - (i - 10)

        elif i <= 30:

            col, row = i - 20, 0

        else:

            col, row = 10, i - 30

        positions.append((
            board_x + col * cell,
            board_y + row * cell
        ))

    # MAIN GAME LOOP

    running = True

    while running:

        now = pygame.time.get_ticks()

        screen.fill(background)

        # SIDEBAR

        pygame.draw.rect(
            screen, panel, sidebar, border_radius=8
        )

        screen.blit(
            heading_font.render("PLAYERS", True, accent),
            (20, 22)
        )

        for i, p in enumerate(players):

            y = 55 + i * 70

            pygame.draw.circle(
                screen, p["color"], (27, y + 10), 7
            )

            screen.blit(
                body_font.render(
                    p["name"][:16],
                    True,
                    white if p["active"] else (130, 130, 130)
                ),
                (40, y + 2)
            )

            balance = (
                f"£{p['cash']:,}"
                if p["active"]
                else "BANKRUPT"
            )

            screen.blit(
                body_font.render(balance, True, muted),
                (40, y + 23)
            )

            if p["human"] and p["piece"]:

                screen.blit(
                    price_font.render(
                        "Piece: " + p["piece"],
                        True, muted
                    ),
                    (40, y + 43)
                )

        human = current == 0 and players[0]["active"]

        # DRAW ALL 40 BOARD SPACES

        for i, (name, kind, group, price, rent) in enumerate(_BOARD):

            x, y = positions[i]

            rect = pygame.Rect(x, y, cell, cell)

            tile_colour = (
                (235, 220, 155)
                if kind == "go"
                else (232, 224, 194)
            )

            pygame.draw.rect(screen, tile_colour, rect)

            pygame.draw.rect(
                screen, (45, 50, 48), rect, 1
            )

            # PROPERTY COLOUR STRIP

            if group in _GROUP_COLORS:

                pygame.draw.rect(
                    screen,
                    _GROUP_COLORS[group],
                    (
                        x + 1,
                        y + 1,
                        cell - 2,
                        max(5, cell // 14)
                    )
                )

            # PROPERTY NAME WRAPPING

            max_width = cell - 10
            max_height = cell - 36

            current_tile_font = tile_font

            lines = _wrapped_lines(
                name,
                current_tile_font,
                max_width
            )

            # Reduce font size only for this individual tile.

            while (
                max(
                    [current_tile_font.size(line)[0] for line in lines],
                    default=0
                ) > max_width
                or len(lines) * current_tile_font.get_linesize() > max_height
            ) and current_tile_font.get_height() > 9:

                current_tile_font = pygame.font.SysFont(
                    "Arial",
                    current_tile_font.get_height() - 1,
                    bold=True
                )

                lines = _wrapped_lines(
                    name,
                    current_tile_font,
                    max_width
                )

            # Centre all lines inside the tile.

            block_height = (
                len(lines) * current_tile_font.get_linesize()
            )

            start_y = y + max(
                cell // 14 + 3,
                (cell - 28 - block_height) // 2
            )

            for line_no, line in enumerate(lines):

                label = current_tile_font.render(
                    line, True, (25, 30, 30)
                )

                screen.blit(
                    label,
                    label.get_rect(
                        center=(
                            x + cell // 2,
                            start_y
                            + line_no * current_tile_font.get_linesize()
                            + current_tile_font.get_linesize() // 2
                        )
                    )
                )

            # PROPERTY PRICE

            if price:

                cost = price_font.render(
                    f"£{price}", True, (45, 50, 48)
                )

                screen.blit(
                    cost,
                    cost.get_rect(
                        center=(x + cell // 2, y + cell - 20)
                    )
                )

            # PROPERTY OWNER MARKER

            if owner[i] is not None:

                pygame.draw.circle(
                    screen,
                    players[owner[i]]["color"],
                    (x + cell - 8, y + 10),
                    5
                )

            # PLAYER TOKENS

            occupants = [
                p for p in players
                if p["active"] and p["position"] == i
            ]

            for j, p in enumerate(occupants):

                tx = int(
                    x + cell // 2
                    + (j - (len(occupants) - 1) / 2) * 13
                )

                ty = y + cell - 8

                pygame.draw.circle(
                    screen, p["color"], (tx, ty), 6
                )

                pygame.draw.circle(
                    screen, (25, 25, 25), (tx, ty), 6, 1
                )

        # BOARD CENTRE

        center = pygame.Rect(
            board_x + cell,
            board_y + cell,
            cell * 9,
            cell * 9
        )

        pygame.draw.rect(
            screen, (35, 54, 82), center
        )

        pygame.draw.rect(
            screen, (170, 190, 190), center, 2
        )

        centre_text = [

            (
                "LONDON MONOPOLY",
                title_font,
                white,
                center.y + 48
            ),

            (
                mode,
                body_font,
                accent,
                center.y + 80
            ),

            (
                f"DICE: {dice[0]} + {dice[1]} = {sum(dice)}",
                heading_font,
                white,
                center.centery - 10
            ),

            (
                "Turn: " + players[current]["name"],
                body_font,
                players[current]["color"],
                center.centery + 20
            ),

            (
                message[:70],
                price_font,
                muted,
                center.centery + 48
            )
        ]

        for text, font, color, cy in centre_text:

            img = font.render(text, True, color)

            screen.blit(
                img,
                img.get_rect(
                    center=(center.centerx, cy)
                )
            )


        # GAME BUTTONS

        if game_over:

            draw_button(menu_rect, "Menu")

        else:

            property_here = (
                _BOARD[players[0]["position"]][1]
                in ("property", "railroad", "utility")
            )

            can_buy = (
                human
                and rolled
                and property_here
                and owner[players[0]["position"]] is None
            )

            draw_button(
                roll_rect,
                "Roll Dice",
                human and not rolled
            )

            draw_button(
                buy_rect,
                "Buy Property",
                can_buy and players[0]["cash"] >=
                _BOARD[players[0]["position"]][3]
            )

            draw_button(
                end_rect,
                "End Turn",
                human and rolled
            )

            draw_button(menu_rect, "Menu")

        pygame.display.flip()

        # CPU PLAYER TURNS

        if (
            not game_over
            and current != 0
            and players[current]["active"]
            and now >= cpu_deadline
        ):

            if not rolled:

                roll()

                cpu_deadline = now + 900

            else:

                advance()

        # HANDLE PLAYER INPUT

        for event in pygame.event.get():

            # CLOSE GAME

            if event.type == pygame.QUIT:

                running = False

            # ESCAPE KEY

            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):

                running = False

            # MOUSE BUTTONS

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                # RETURN TO MENU

                if menu_rect.collidepoint(event.pos):

                    running = False

                # HUMAN PLAYER CONTROLS

                elif not game_over and current == 0:

                    # ROLL DICE

                    if (
                        roll_rect.collidepoint(event.pos)
                        and not rolled
                    ):

                        roll()

                    # BUY PROPERTY

                    elif (
                        buy_rect.collidepoint(event.pos)
                        and rolled
                    ):

                        pos = players[0]["position"]

                        space = _BOARD[pos]

                        if (
                            space[1] in (
                                "property",
                                "railroad",
                                "utility"
                            )
                            and owner[pos] is None
                            and players[0]["cash"] >= space[3]
                        ):

                            players[0]["cash"] -= space[3]

                            owner[pos] = 0

                            message = (
                                f"You bought {space[0]} "
                                f"for £{space[3]}!"
                            )

                    # END TURN

                    elif (
                        end_rect.collidepoint(event.pos)
                        and rolled
                    ):

                        advance()

        # FRAME RATE

        clock.tick(30)

    # RETURN GAME RESULT TO PROTOTYPE 2

    return winner == 0
