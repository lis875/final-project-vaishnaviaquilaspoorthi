import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
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
        "text": "Welcome to Raiders of the Lost Artifact!\n\nYour goal is to find the ancient Scepter of Eternity hidden deep within the Amazon rainforest.\n\nMake choices to navigate through the challenges and uncover the mysteries.",
        "button_text": "Start",
        "background": pygame.image.load("intro_background.jpg"),
        "next_screen": "chapter1"
    },
    "chapter1": {
        "text": "You find a cryptic message leading you to the hidden temple.\n\nSelect your path:",
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

def display_button(text, button_rect):
    button_text = font.render(text, True, white)
    
    # Draw a background rectangle and check if the mouse is over it
    highlight = button_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, highlight_color if highlight else black, button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

def main():
    global current_screen, current_chapter

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
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

            # Display background image
            screen.blit(chapter_data["background"], (0, 0))

            # Display chapter text with an offset
            display_text(chapter_data["text"], -50)

            if "choices" in chapter_data:
                # Display choices as clickable buttons
                chapter_data["choice_rects"] = [pygame.Rect(50, 150 + i * 50, 300, 50) for i in range(len(chapter_data["choices"]))]
                display_choices(chapter_data["choices"], chapter_data["choice_rects"])

            elif "button_text" in chapter_data:
                # Display a button
                chapter_data["button_rect"] = pygame.Rect(50, 400, 300, 50)
                display_button(chapter_data["button_text"], chapter_data["button_rect"])

        pygame.display.flip()
        clock.tick(30)

def display_choices(choices, choice_rects):
    for i, (choice, rect) in enumerate(zip(choices, choice_rects)):
        choice_text = font.render(choice, True, white)
        
        # Draw a background rectangle and check if the mouse is over it
        highlight = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, highlight_color if highlight else black, rect)
        screen.blit(choice_text, (rect.x + 10, rect.y + 10))

if __name__ == "__main__":
    main()
