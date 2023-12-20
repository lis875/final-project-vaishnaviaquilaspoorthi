import pygame
import sys
import textwrap
import pygame.mixer
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/intro_music.mp3")

# Get the screen size
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Raiders of the Lost Artifact")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (150, 150, 150)
blue = (33, 116, 115)  # New color for the button
green = (0, 255, 0)
orange = (255, 165, 0)
red = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Game variables
current_screen = "intro"
current_chapter = 1

health = 100  # Initial health

# Mini-game functions
# Load map image
# Load map image
map_image = pygame.transform.scale(
    pygame.image.load("assets/images/map_screen.jpg"),
    (screen_width, screen_height)
)

# Create a rect for the map button
map_button_rect = pygame.Rect(screen_width - 70, screen_height - 70, 50, 50)
map_button_text = font.render("MAP", True, white)

close_button_width, close_button_height = 50, 50
close_button_rect = pygame.Rect(screen_width - close_button_width - 20, 20, close_button_width, close_button_height)
close_button_text = font.render("X", True, white)

def handle_health(health_change):
    global health
    health += health_change
    # Ensure health stays within [0, 100] range
    health = max(0, min(health, 100))

# Function to handle health changes
# Function to handle health changes
def handle_choice(chapter_data, choice_number):
    choice_function = chapter_data.get("choice_functions", {}).get(choice_number)

    if choice_function:
        choice_function()  # Call the specified function for the chosen choice
        display_health_bar()  # Update the health bar after the choice is made


# Function to handle choices
def handle_choice_function(health_change):
    handle_health(health_change)


# Chapter data

chapters = {
    "intro": {
        "text": "Welcome to Raiders of the Lost Artifact! Your goal is to find the ancient Scepter of Eternity hidden deep within the Amazon rainforest. Make choices to navigate through the challenges and uncover the mysteries.",
        "button_text": "  Start  ",
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/intro_background.jpg"),
            (screen_width, screen_height),
        ),
        "next_screen": "chapter1",
    },
    "chapter1": {
        "text": "You find a cryptic message that will lead you to the hidden temple. Select your path:",
        "choices": [" Take the winding river route.", " Repel down the cliff."],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/river_background.jpg"),
            (screen_width, screen_height),
        ),
        "next_chapters": [2,4],
        "choice_functions": {
            1: lambda: handle_choice_function(0),
            2: lambda: handle_choice_function(-10),
        },
    },
    "chapter2": {
        "text": "As Pavitra continues, the sound of a distant waterfall reaches his ears. A mystical aura surrounds the area, and a shimmering waterfall reveals a hidden cave. Choose your next move:",
        "choices": [
            " Investigate the cave behind the waterfall, hoping it holds clues to the artifact's location ",
            " Stay on course, wary of potential traps near the enchanting waterfall. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [3,3],
        "choice_functions": {
            1: lambda: handle_choice_function(-5),
            2: lambda: handle_choice_function(-10), 
        },
    },
    "chapter3": {
        "text": "In the depths of the cave, Pavitra encounters ethereal guardian spirit. They offer guidance but pose a challenge to those seeking the artifact. Choose your next move:",
        "choices": [
            " Seek the spirits' guidance, accepting the challenges they present. ",
            " Avoid the spirits and proceed cautiously, relying on your instincts. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [6,6],
        "choice_functions": {
            1: lambda: handle_choice_function(-5),
            2: lambda: handle_choice_function(0),  # Placeholder for the second choice
        },
    },
    "chapter4": {
        "text": "While exploring further, Pavitra discovers a concealed path veiled by overgrown vegetation. The path seems to lead deeper into the heart of the forest. Choose your next move:",
        "choices": [
            " Follow the hidden path, intrigued by the possibility of finding secrets unknown. ",
            " Stick to the original route, cautious of potential dangers. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [5,5],
        "choice_functions": {
            1: lambda: handle_choice_function(-5),
            2: lambda: handle_choice_function(-20),  # Placeholder for the second choice
        },
    },
    "chapter5": {
        "text": "Pavitra stumbles upon the journal of a lost explorer who had ventured into the jungle in search of the same artifact. The journal contains valuable insights .Choose your next move:",
        "choices": [
            " Study the journal for clues that might aid your quest. ",
            " Continue without delving into the journal, relying on your instincts. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [6,6],
        "choice_functions": {
            1: lambda: handle_choice_function(-10),
            2: lambda: handle_choice_function(-15),  # Placeholder for the second choice
        },
    },
    "chapter6": {
        "text": "Inside the temple, Pavitra encounters a vast chamber filled with shadows. In the center, a pedestal holds the artifact. However, a series of deadly traps guard the way. Choose your next move:",
        "choices": [
            " Brave the hidden spikes on the floor and make a run for the artifact. ",
            " Examine the walls for clues to disarm the traps safely. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [7,7],
        "choice_functions": {
            1: lambda: handle_choice_function(-10),
            2: lambda: handle_choice_function(-5),  # Placeholder for the second choice
        },
    },
    "chapter7": {
        "text": "As Pavitra finds the Stone embedded in the wall, he notices the cracks on the ancient painted walls that are held together by the stone. A question is written below the stone. Only if you give the right answer will you be allowed to take the stone. \n 'Eternal, yet fleeting, it marches with might, Leaving its mark, conquering all fears.' What am I?" ,
        "choices": [
            "  'Time' ",
            " 'Power' ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [8,8],
        "choice_functions": {
            1: lambda: handle_choice_function(0),
            2: lambda: handle_choice_function(-30),
        },
    },
    "chapter8": {
        "text": "As Pavitra secures the artifact, a collapsing mechanism is triggered within the temple. The exit is blocked, and time is running out.",
        "choices": [
            " Navigate through a series of secret passages to find an alternative exit.",
            " Use your whip to create a makeshift bridge and cross a dangerous gap. ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [9,9],
        "choice_functions": {
            1: lambda: handle_choice_function(0),
            2: lambda: handle_choice_function(-5),
        },
    },
    "chapter9": {
        "text": "With the artifact in hand, Pavi dodges an attack that his arch-rival initiates as he tries to snatch the stone.",
        "choices": [
            " Use the power of the stone on Dr. Gunda ",
            " Engage in hand-to-hand combat ",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [10,10],
        "choice_functions": {
            1: lambda: handle_choice_function(-10),
            2: lambda: handle_choice_function(-10),
        },
    },
    "chapter10": {
        "text": "Pavitra Prabhakar successfully escapes the collapsing temple and Dr. Gunda. The artifact is secured, and Pavitra reflects on the thrilling adventure.",
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
    }
}



def wrap_text(text, font, max_width):
    words = text.split()
    wrapped_lines = []
    current_line = []

    for word in words:
        test_line = current_line + [word]
        test_text = ' '.join(test_line)
        text_width, _ = font.size(test_text)

        if text_width <= max_width:
            current_line.append(word)
        else:
            wrapped_lines.append(' '.join(current_line))
            current_line = [word]

    wrapped_lines.append(' '.join(current_line))
    return wrapped_lines

def display_health_bar():
    # Calculate health bar dimensions
    health_bar_width = int((health / 100) * (screen_width - 40))
    health_bar_height = 20
    health_bar_x = 20
    health_bar_y = 20

    # Calculate color based on health value
    if health > 60:
        color = green
        text_color = black  # Set text color to white for green health
    elif 20 <= health <= 60:
        color = orange
        text_color = white  # Set text color to black for orange health
    else:
        color = red
        text_color = white  # Set text color to white for red health

    # Draw health bar background
    pygame.draw.rect(screen, black, (health_bar_x, health_bar_y, screen_width - 40, health_bar_height))
    # Draw health bar
    pygame.draw.rect(screen, color, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

    # Display health value with the specified text color
    health_text = font.render(f"Health: {health}", True, text_color)
    
    # Adjust the x-coordinate to place the text within the health bar
    text_x = health_bar_x + (health_bar_width - health_text.get_width()) / 2
    screen.blit(health_text, (text_x, health_bar_y))


def display_text(text, y_offset=0):
    wrapped_text = wrap_text(text, font, screen_width - 400)
    text_surface = pygame.Surface((screen_width - 200, screen_height - 700), pygame.SRCALPHA)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))

    line_height = font.get_linesize()
    total_lines = len(wrapped_text)
    for i, line in enumerate(wrapped_text):
        line_surface = font.render(line, True, white)
        line_rect = line_surface.get_rect(center=(text_rect.width // 2, text_rect.height // 2 + i * line_height - (total_lines-1) * line_height // 2))
        text_surface.blit(line_surface, line_rect)

    black_rect = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(black_rect, (0, 0, 0, 150), black_rect.get_rect())
    screen.blit(black_rect, text_rect.topleft)

    screen.blit(text_surface, text_rect.topleft)


# Inside display_choices function
def display_choices(choices, choice_rects):
    padding_x = 10  # Adjust the padding value as needed
    padding_y = 5  # Adjust the padding value as needed

    total_width = len(choices) * 300 + (len(choices) - 1) * 10
    start_x = (screen_width - total_width) // 2

    for i, (choice, rect) in enumerate(zip(choices, choice_rects)):
        choice_text = font.render(choice, True, white)

        # Adjust the choice_rect to include padding
        choice_rect = pygame.Rect(
            start_x + i * 310 - padding_x,
            rect.y - padding_y,
            choice_text.get_width() + 2 * padding_x,
            choice_text.get_height() + 2 * padding_y
        )

        button_surface = pygame.Surface((400, 50), pygame.SRCALPHA)
        highlight = choice_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(button_surface, highlight_color if highlight else black, button_surface.get_rect())
        screen.blit(button_surface, (start_x + i * 310, rect.y))

        screen.blit(choice_text, (choice_rect.x + padding_x, choice_rect.y + padding_y))


# Inside the main function
def main():
    global current_screen, current_chapter, health, map_displayed, previous_screen
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the map button is clicked
                if map_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if current_screen == "map":
                        # Close the map screen
                        map_displayed = False
                        current_screen = previous_screen
                    else:
                        # Open the map screen
                        map_displayed = True
                        previous_screen = current_screen
                        current_screen = "map"

                elif current_screen == "map":
                    # Check if the close button on the map screen is clicked
                    if close_button_rect.collidepoint(pygame.mouse.get_pos()):
                        # Close the map screen
                        map_displayed = False
                        current_screen = previous_screen

                elif current_screen in chapters:
                    chapter_data = chapters[current_screen]

                    if "button_rect" in chapter_data and chapter_data["button_rect"].collidepoint(pygame.mouse.get_pos()):
                        current_screen = chapter_data["next_screen"]

                    elif "choice_rects" in chapter_data:
                        for i, rect in enumerate(chapter_data["choice_rects"]):
                            if rect.collidepoint(pygame.mouse.get_pos()):
                                current_chapter = chapter_data["next_chapters"][i]
                                current_screen = f"chapter{current_chapter}"

                                # Add the following line to handle the choice and update the health bar
                                handle_choice(chapter_data, i + 1)


                    elif "choices" in chapter_data and "button_rect" not in chapter_data:
                        # Handle case where choices are displayed without a button
                        for i, rect in enumerate(chapter_data["choice_rects"]):
                            if rect.collidepoint(pygame.mouse.get_pos()):
                                current_chapter = chapter_data["next_chapters"][i]
                                current_screen = f"chapter{current_chapter}"

                                # Add the following line to handle the choice and update the health bar
                                handle_choice(chapter_data, i + 1)

        if current_screen in chapters:
            chapter_data = chapters[current_screen]

            screen.blit(chapter_data["background"], (0, 0))
            display_text(chapter_data["text"], -50)

            display_health_bar()  # Add this line to display the health bar

            # Draw the map button
            pygame.draw.rect(screen, blue, map_button_rect, 0)
            pygame.draw.rect(screen, (255, 255, 255), map_button_rect, 2)
            screen.blit(map_button_text, (map_button_rect.x + (map_button_rect.width - map_button_text.get_width()) // 2, map_button_rect.y + (map_button_rect.height - map_button_text.get_height()) // 2))

            if "choices" in chapter_data:
                chapter_data["choice_rects"] = []
                for i, choice in enumerate(chapter_data["choices"]):
                    choice_text = font.render(choice, True, white)
                    choice_rect = pygame.Rect(
                        screen_width // 2 - choice_text.get_width() // 2,
                        screen_height - 100 + i * (choice_text.get_height() + 10),
                        choice_text.get_width(),
                        choice_text.get_height()
                    )
                    chapter_data["choice_rects"].append(choice_rect)

                for i, rect in enumerate(chapter_data["choice_rects"]):
                    highlight = rect.collidepoint(pygame.mouse.get_pos())
                    pygame.draw.rect(screen, blue if highlight else (0, 0, 0), rect, 0)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
                    screen.blit(font.render(chapter_data["choices"][i], True, white), (rect.x, rect.y))

            elif "button_text" in chapter_data:
                button_text = font.render(chapter_data["button_text"], True, white)
                button_rect = pygame.Rect(screen_width // 2 - button_text.get_width() // 2,
                                          screen_height - 100,
                                          button_text.get_width(),
                                          button_text.get_height())
                chapter_data["button_rect"] = button_rect

                # Check if the mouse is over the button
                highlight = button_rect.collidepoint(pygame.mouse.get_pos())

                # Change the button color when hovering
                pygame.draw.rect(screen, blue if highlight else (0, 0, 0), button_rect, 0)
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
                screen.blit(button_text, (button_rect.x, button_rect.y))

            pygame.display.flip()

        elif current_screen == "map":
            # Display the map image
            screen.blit(map_image, (0, 0))

            # Draw the close button on the map screen
            pygame.draw.rect(screen, red, close_button_rect, 0)
            pygame.draw.rect(screen, (255, 255, 255), close_button_rect, 2)
            screen.blit(close_button_text, (close_button_rect.x + (close_button_rect.width - close_button_text.get_width()) // 2, close_button_rect.y + (close_button_rect.height - close_button_text.get_height()) // 2))

            pygame.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    main()
