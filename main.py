import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Raiders of the Lost Artifact")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Game variables
current_chapter = 1

# Chapter data
chapters = {
    1: {
        "text": "Welcome to Raiders of the Lost Artifact!",
        "choices": ["Take the winding river route.", "Repel down the cliff."],
        "background": pygame.image.load("temple_background.jpg"),
        "next_chapters": [2, 3]  # Corresponding to the choices
    },
    # Add more chapters as needed
}

def display_text(text, y_offset=0):
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    
    # Create a background rectangle behind the text
    pygame.draw.rect(screen, black, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    screen.blit(text_surface, text_rect.topleft)

def display_choices(choices):
    for i, choice in enumerate(choices):
        choice_text = font.render(choice, True, white)
        choice_rect = choice_text.get_rect(topleft=(50, 150 + i * 50))
        
        # Create a background rectangle behind each choice
        pygame.draw.rect(screen, black, (choice_rect.x - 10, choice_rect.y - 10, choice_rect.width + 20, choice_rect.height + 20))
        screen.blit(choice_text, choice_rect.topleft)

def main():
    global current_chapter

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_chapter in chapters:
                    chapter_data = chapters[current_chapter]
                    choices = chapter_data["choices"]

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, _ in enumerate(choices):
                        if 50 <= mouse_x <= 300 and 150 + i * 50 <= mouse_y <= 200 + i * 50:
                            current_chapter = chapter_data["next_chapters"][i]

        if current_chapter in chapters:
            chapter_data = chapters[current_chapter]

            # Display background image
            screen.blit(chapter_data["background"], (0, 0))

            # Display chapter text with an offset
            display_text(chapter_data["text"], -50)

            # Display choices
            display_choices(chapter_data["choices"])

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
