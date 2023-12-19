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
        "background": pygame.transform.scale(pygame.image.load("assets/images/intro_background.jpg"), (screen_width, screen_height)),
        "next_screen": "chapter1"
    },
    "chapter1": {
        "text": "You find a cryptic message leading you to the hidden temple. Select your path:",
        "choices": ["Take the winding river route.", "Repel down the cliff."],
        "background": pygame.transform.scale(pygame.image.load("assets/images/river_background.jpg"), (screen_width, screen_height)),
        "next_chapters": [2, 3]  # Corresponding to the choices
    },
    # Add more chapters as needed
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
                              button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))

def display_choices(choices):
    choice_rects = []
    total_width = len(choices) * 300 + (len(choices) - 1) * 10
    start_x = (screen_width - total_width) // 2

    for i, choice in enumerate(choices):
        choice_text = font.render(choice, True, white)
        rect = pygame.Rect(start_x + i * 310, screen_height - 70, 300, 50)

        pygame.draw.rect(screen, black, rect)
        screen.blit(choice_text, (rect.x + (300 - choice_text.get_width()) // 2, rect.y + (50 - choice_text.get_height()) // 2))

        choice_rects.append(rect)

    return choice_rects

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
                                current_screen = "chapter1"  # Set the screen back to chapter1

        if current_screen in chapters:
            chapter_data = chapters[current_screen]

            screen.blit(chapter_data["background"], (0, 0))
            display_text(chapter_data["text"], -50)

            if "choices" in chapter_data:
                chapter_data["choice_rects"] = display_choices(chapter_data["choices"])

            elif "button_text" in chapter_data:
                chapter_data["button_rect"] = pygame.Rect(screen_width // 2 - 150, screen_height - 100, 300, 50)
                display_button(chapter_data["button_text"], chapter_data["button_rect"])

            pygame.display.flip()

        clock.tick(30)


if __name__ == "__main__":
    main()
