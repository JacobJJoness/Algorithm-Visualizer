import pygame
import random
import time


pygame.init()

# Set up display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Insertion Sort Visualizer")

# Colors
background_color = (25, 25, 25)
bar_color = (255, 0, 0)
active_color = (0, 255, 0)



# Number of bars and their width
num_bars = 200
bar_width = width // num_bars
gap = 2

# Generate random heights for bars
bar_heights = [random.randint(50, 500) for _ in range(num_bars)]

paused = True
sorting = False

# Button class
class Button:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 150, 60)
        self.color = (150, 150, 150)
        self.action = action

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        display.blit(text, text_rect)

    def check_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

play_pause_button = Button("Play/Pause", (50, 50), lambda: global_play_pause())
restart_button = Button("Restart", (50, 120), lambda: restart())

def global_play_pause():
    global paused
    paused = not paused

def insertion_sort(arr):
    global paused, sorting
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            draw_bars(arr, [i, j + 1])
            pygame.display.update()
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_pause_button.check_clicked(event.pos)
                    restart_button.check_clicked(event.pos)

        arr[j + 1] = key

def draw_bars(arr, active_indices=[]):
    display.fill(background_color)
    for i, height in enumerate(arr):
        color = bar_color
        if i in active_indices:
            color = active_color
        x_pos = i * (bar_width + gap)
        y_pos = height
        pygame.draw.rect(display, color, (x_pos, 0, bar_width, height))
    play_pause_button.draw()
    restart_button.draw()
    pygame.display.update()

def restart():
    global bar_heights, paused
    bar_heights = [random.randint(50, 500) for _ in range(num_bars)]
    paused = True
    draw_bars(bar_heights)

def main():
    global paused, sorting
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_pause_button.check_clicked(event.pos)
                restart_button.check_clicked(event.pos)

        if not paused and not sorting:
            sorting = True
            insertion_sort(bar_heights)
            sorting = False

        draw_bars(bar_heights)

    pygame.quit()

if __name__ == "__main__":
    main()