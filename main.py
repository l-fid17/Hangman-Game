import math, random
import pygame
import pygame_menu
import nltk
nltk.download('words')
from nltk.corpus import words

pygame.init()

# setup display
WIDTH, HEIGHT = 720, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hangman Game")

menu = pygame_menu.Menu(
    HEIGHT, WIDTH, "Play Hangman", theme=pygame_menu.themes.THEME_GREEN)

# load images
images = []
for i in range(7):
    images.append(pygame.image.load("images/hangman" + str(i) + ".png"))

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# colors
BG_GREEN = (0, 255, 0, 1)
BG_WHITE = (255, 255, 255, 1)

B_BLACK = (0, 0, 0, 1)

# button variables
RADIUS = 20
GAP = 10
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 375
A = 65
letters = []
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# game variables
hangman_status = 0
# words = ["DEVELOPER", "CODING", "PYGAME", "PYTHON", "ENVIRONMENT"]
words = words.words()
word = random.choice(words).upper()
guessed = []


def draw():
    win.fill(BG_GREEN)

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, B_BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, B_BLACK)
    win.blit(text, (300, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, B_BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, B_BLACK)
            win.blit(text,
                     (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (WIDTH / 8, HEIGHT / 6))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(BG_GREEN)
    text = WORD_FONT.render(message, 1, B_BLACK)
    win.blit(
        text,
        (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def play_again():
    B_WIDTH = 100
    B_HEIGHT = 40

    win.fill(BG_WHITE)

    text = TITLE_FONT.render("Play Again?", 1, B_BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    pygame.draw.rect(win, B_BLACK, (100, 100, B_WIDTH, B_HEIGHT))

    pygame.display.update()


def reset_fields():
    global hangman_status, word, guessed, letters
    hangman_status = 0
    word = random.choice(words).upper()
    guessed = []
    letters = []
    for i in range(26):
        x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = start_y + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


# Game Loop
def start_game():
    global hangman_status

    # set game loop
    FPS = 60  # max framerate
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You Won!")
            reset_fields()
            break

        if hangman_status == 6:
            display_message("You Lost :(")
            display_message(word)
            reset_fields()
            break


menu.add_button('Play', start_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(win)
pygame.quit()
