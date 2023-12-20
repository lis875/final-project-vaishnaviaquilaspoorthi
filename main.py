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
def mini_deciphering_game():
    # Implement the mini deciphering game logic here
    pass

def mini_guess_the_pattern_game():
    # Implement the mini guess the pattern game logic here
    pass

def mini_trivia_game():
    # Implement the mini trivia game logic here
    pass

def mini_math_game():
    # Implement the mini math game logic here
    pass

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
        "text": "You find a cryptic message leading you to the hidden temple. Select your path:",
        "choices": [" Take the winding river route. (Lose 5 health) ", " Repel down the cliff. (Lose 10 health) "],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/river_background.jpg"),
            (screen_width, screen_height),
        ),
        "next_chapters": [2, 3],
        "choice_functions": {
            1: lambda: handle_choice_function(-5),
            2: lambda: handle_choice_function(-10)
        }
    },
    "chapter2": {
        "text": "He finds himself standing in front of an ancient temple hidden within the jungle. The entrance is adorned with strange symbols. A faint whispering sound echoes through the air. Choose your next move:",
        "choices": [
            " Decipher the symbols and enter through the main entrance. (Mini deciphering game) ",
            " Consult the book which you brought with you "
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [4, 5],
        "choice_functions": {
            1: mini_deciphering_game,
            2: lambda: None  # Placeholder for the second choice
        }
    },
    "chapter3": {
        "text": "Inside the temple, Pavitra encounters a vast chamber filled with shadows. In the center, a pedestal holds the artifact. However, a series of deadly traps guard the way. Make your decision:",
        "choices": [
            " Brave the hidden spikes on the floor and make a run for the artifact. (Lose 10 health) ",
            " Examine the walls for clues to disarm the traps safely. (Mini guess the pattern game) "
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter3.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [6, 7],
        "choice_functions": {
            1: lambda: handle_choice_function(-10),
            2: mini_guess_the_pattern_game
        }
    },
    "chapter4": {
        "text": "As Indiana secures the artifact, a rival archaeologist, Dr. Renegade, appears. He demands the artifact for himself and challenges Indiana to a duel. How will you confront Dr. Renegade?",
        "choices": [
            " Engage in a traditional fistfight to settle the dispute. (Lose 20 health) ",
            " Outsmart him with your knowledge of ancient artifacts. (Mini trivia game) "
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter4.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [8, 9],
        "choice_functions": {
            1: lambda: handle_choice_function(-20),
            2: mini_trivia_game
        }
    },
    "chapter5": {
        "text": "With the artifact in hand, Pavi and Dr. Renegade trigger a collapsing mechanism within the temple. The exit is blocked, and time is running out. Select your escape route:",
        "choices": [
            " Navigate through a series of secret passages to find an alternative exit. (Mini math game) ",
            " Use your whip to create a makeshift bridge and cross a dangerous gap. (Lose 10 health) "
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter5.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [10, 11],
        "choice_functions": {
            1: mini_math_game,
            2: lambda: handle_choice_function(-10)
        }
    },
    "epilogue": {
        "text": "Indiana Jones successfully escapes the collapsing temple, leaving Dr. Renegade behind. The artifact is secured, and Indiana reflects on the thrilling adventure. How will you conclude this tale?",
        "choices": [
            " Return the artifact to a museum to share its history with the world. ",
            " Keep the artifact for yourself, unlocking its mysterious powers. "
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter6.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [12, 13],
        "choice_functions": {
            1: lambda: None,  # Placeholder for the first choice
            2: lambda: None   # Placeholder for the second choice
        }
    },
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


# ... (remaining code)

def display_health_bar():
    # Calculate health bar dimensions
    health_bar_width = int((health / 100) * (screen_width - 40))
    health_bar_height = 20
    health_bar_x = 20
    health_bar_y = 20

    # Calculate color based on health value
    if health > 60:
        color = green
        text_color = white  # Set text color to white for green health
    elif 20 <= health <= 60:
        color = orange
        text_color = black  # Set text color to black for orange health
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


def main():
    global current_screen, current_chapter, health
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
                if current_screen in chapters:
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


        if current_screen in chapters:
            chapter_data = chapters[current_screen]

            screen.blit(chapter_data["background"], (0, 0))
            display_text(chapter_data["text"], -50)

            display_health_bar()  # Add this line to display the health bar

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

        clock.tick(30)

if __name__ == "__main__":
    main()