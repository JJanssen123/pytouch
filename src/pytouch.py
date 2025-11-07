#!/usr/bin/env python3
import pygame, os, sys
from touch.touch import TouchHandler # Importeer de bijgewerkte klasse

# === Constanten & Instellingen ===
EVENT_DEV = "/dev/input/event0"
SCREEN_W = 320
SCREEN_H = 480
SWIPE_TRESHOLD = 10 # Vereiste swipe afstand in pixels

# === init display drivers ===
os.environ["SDL_VIDEODRIVER"] = "kmsdrm"
os.environ["SDL_RENDER_DRIVER"] = "software"

# === Main Programma ===
if __name__ == '__main__':
    # Geef de drempelwaarde mee bij initialisatie
    touch = TouchHandler(EVENT_DEV, SCREEN_W, SCREEN_H, swipe_threshold=SWIPE_TRESHOLD)
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN) 
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    running = True

    screen.fill((255, 255, 255)) 
    prev_x, prev_y = 0, 0 

    # Hoofd game-lus
    while running:
        # --- 1. PYGAME EVENT AFHANDELING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- 2. TOUCH EVENT AFHANDELING ---
        touch.process_events()

        # --- 3. SWIPE DETECTIE IN MAIN LOOP ---
        # Controleer of er een swipe heeft plaatsgevonden in deze frame
        if touch.swipe_direction:
            print(f"Swipe gedetecteerd: {touch.swipe_direction}")
            # Hier kun je code toevoegen om iets anders te doen bij een swipe
            if touch.swipe_direction == 'left':
                #print("Ga naar vorig menu!")
                pass

        # --- 4. TEKENLOGICA IN DE MAIN LOOP (Blijft intact) ---
        if touch.is_touching:
            print(f"Tap ({touch.current_x}, {touch.current_y})")
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = touch.current_x, touch.current_y
                
            pygame.draw.line(screen, (255, 0, 0), (prev_x, prev_y), (touch.current_x, touch.current_y), 5)
            prev_x, prev_y = touch.current_x, touch.current_y
        else:
            prev_x, prev_y = 0, 0

        # --- 5. RENDEREN EN FRAMERATE BEHEER ---
        dirty_rect = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
        pygame.display.update(dirty_rect)
        
        clock.tick(60)

    pygame.quit()
