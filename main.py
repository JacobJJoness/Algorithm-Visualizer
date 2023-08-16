import pygame
import random
import time

pygame.init()

# Set up display
width, height = 900, 700
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Insertion Sort Visualizer")

# Colors
background_color = (25, 25, 25)
bar_color = (255, 0, 0)
active_color = (0, 255, 0)

# Calculate number of bars and their width dynamically
num_bars = 200  # Change this to your desired number of bars
bar_width = width // num_bars


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

play_pause_button = Button("Play/Pause", (50, height - 150), lambda: global_play_pause())
restart_button = Button("Restart", (50, height - 80), lambda: restart())

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
            time.sleep(0.01)
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
    
    # Define the gradient colors
    start_color = (0, 0, 255)  # Blue
    end_color = (255, 0, 0)    # Red
    
    for i, height in enumerate(arr):
        # Calculate the interpolation factor based on the height
        interp_factor = (height - min(arr)) / (max(arr) - min(arr))
        
        # Interpolate between start_color and end_color
        color = (
            int(start_color[0] + interp_factor * (end_color[0] - start_color[0])),
            int(start_color[1] + interp_factor * (end_color[1] - start_color[1])),
            int(start_color[2] + interp_factor * (end_color[2] - start_color[2]))
        )
        
        if i in active_indices:
            color = active_color
        x_pos = i * bar_width
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





