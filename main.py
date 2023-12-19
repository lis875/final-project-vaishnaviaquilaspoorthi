import pygame
import sys
import textwrap
import pygame.mixer

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

# Fonts
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Game variables
current_screen = "intro"
current_chapter = 1

# Chapter data

chapters = {
    "intro": {
        "text": "Welcome to Raiders of the Lost Artifact! \n Your goal is to find the ancient Scepter of Eternity hidden deep within the Amazon rainforest. \n Make choices to navigate through the challenges and uncover the mysteries.",
        "button_text": "Start",
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/intro_background.jpg"),
            (screen_width, screen_height),
        ),
        "next_screen": "chapter1",
    },
    "chapter1": {
        "text": "You find a cryptic message leading you to the hidden temple. Select your path:",
        "choices": ["Take the winding river route.", "Repel down the cliff."],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/river_background.jpg"),
            (screen_width, screen_height),
        ),
        "next_chapters": [2, 3],  # Corresponding to the choices
    },
    "chapter2": {
        "text": "He finds himself standing in front of an ancient temple hidden within the jungle. The entrance is adorned with strange symbols. A faint whispering sound echoes through the air. Choose your next move:",
        "choices": [
            "Decipher the symbols and enter through the main entrance.",
            "Consult the book which you brought with you",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter2.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [4, 5],  # Corresponding to the choices
    },
    "chapter3": {
        "text": "Inside the temple, Pavitra encounters a vast chamber filled with shadows. In the center, a pedestal holds the artifact. However, a series of deadly traps guard the way. Make your decision:",
        "choices": [
            "Brave the hidden spikes on the floor and make a run for the artifact.",
            "Examine the walls for clues to disarm the traps safely.",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter3.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [6, 7],  # Corresponding to the choices
    },
    "chapter4": {
        "text": "As Indiana secures the artifact, a rival archaeologist, Dr. Renegade, appears. He demands the artifact for himself and challenges Indiana to a duel. How will you confront Dr. Renegade?",
        "choices": [
            "Engage in a traditional fistfight to settle the dispute.",
            "Outsmart him with your knowledge of ancient artifacts.",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter4.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [8, 9],  # Corresponding to the choices
    },
    "chapter5": {
        "text": "With the artifact in hand, Pavi and Dr. Renegade trigger a collapsing mechanism within the temple. The exit is blocked, and time is running out. Select your escape route:",
        "choices": [
            "Navigate through a series of secret passages to find an alternative exit.",
            "Use your whip to create a makeshift bridge and cross a dangerous gap.",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter5.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [10, 11],  # Corresponding to the choices
    },
    "epilogue": {
        "text": "Indiana Jones successfully escapes the collapsing temple, leaving Dr. Renegade behind. The artifact is secured, and Indiana reflects on the thrilling adventure. How will you conclude this tale?",
        "choices": [
            "Return the artifact to a museum to share its history with the world.",
            "Keep the artifact for yourself, unlocking its mysterious powers.",
        ],
        "background": pygame.transform.scale(
            pygame.image.load("assets/images/chapter6.png"),
            (screen_width, screen_height),
        ),
        "next_chapters": [12, 13],  # Corresponding to the choices
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

def display_button(text, button_rect):
    button_text = font.render(text, True, white)
    
    highlight = button_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, highlight_color if highlight else black, button_rect)
    screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                              button_rect.y + button_rect.height // 2 -
    button_text.get_height() // 2))

def display_choices(choices, choice_rects):
    total_width = len(choices) * 300 + (len(choices) - 1) * 10
    start_x = (screen_width - total_width) // 2

    for i, (choice, rect) in enumerate(zip(choices, choice_rects)):
        choice_text = font.render(choice, True, white)

        text_x = start_x + i * 310 + (300 - choice_text.get_width()) // 2
        text_y = rect.y + (50 - choice_text.get_height()) // 2

        button_surface = pygame.Surface((400, 50), pygame.SRCALPHA)
        highlight = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(button_surface, highlight_color if highlight else black, button_surface.get_rect())
        screen.blit(button_surface, (start_x + i * 310, rect.y))

        screen.blit(choice_text, (text_x, text_y))


def main():
    global current_screen, current_chapter
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

        if current_screen in chapters:
            chapter_data = chapters[current_screen]

            screen.blit(chapter_data["background"], (0, 0))
            display_text(chapter_data["text"], -50)

            if "choices" in chapter_data:
                chapter_data["choice_rects"] = [pygame.Rect(screen_width // 2 - 150, screen_height - 100 + i * 60, 300, 50) for i in range(len(chapter_data["choices"]))]
                display_choices(chapter_data["choices"], chapter_data["choice_rects"])


            elif "button_text" in chapter_data:
                chapter_data["button_rect"] = pygame.Rect(screen_width // 2 - 150, screen_height - 100, 300, 50)
                display_button(chapter_data["button_text"], chapter_data["button_rect"])

            pygame.display.flip()

        clock.tick(30)


if __name__ == "__main__":
    main()
