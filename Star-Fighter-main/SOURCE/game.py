
import pygame, os, random, math, time, pickle
from pygame.locals import *
from pygame._sdl2.video import Window
from data.scripts.scenes import *
from data.scripts.defines import FPS, WIN_RES, TITLE
from data.scripts.muda import (
    load_img, 
    load_sound, 
    read_savedata,
    write_savedata,
    SceneManager
)
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
pygame.mixer.init()

# Player Preferences class =====================================================
class PlayerPrefs:
    def __init__(self):
        self.is_fullscreen = False
        self.is_frameless = False
        self.music_vol = 0.40
        self.sfx_vol = 0.30
        self.game_difficulty = 0
        self.hp_pref = 0
        self.can_pause = False

        # Controls
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT 
        self.key_fire = pygame.K_z
        self.key_back = pygame.K_x

        self.score = 0
        self.title_selected = 0
        self.options_scene_selected = 0

# Game loop ====================================================================

def main():
    # Load / create PlayerPrefs object
    P_Prefs = None
    try:
        with open(USERDAT_FILE, 'rb') as f:
            P_Prefs = pickle.load(f)

            # Reset these variables
            P_Prefs.title_selected = 0
            P_Prefs.options_scene_selected = 0
    except:
        P_Prefs = PlayerPrefs()

    # Play music
    pygame.mixer.music.load("SOURCE\data\sfx\ost_fighter.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(P_Prefs.music_vol)
    
    # Set window flags
    window_flags = HWACCEL | DOUBLEBUF
    if P_Prefs.is_fullscreen:
        window_flags = window_flags | FULLSCREEN
    if P_Prefs.is_frameless:
        window_flags = window_flags | NOFRAME

    # Initialize the window
    window = None
    if P_Prefs.is_fullscreen:
        window = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), window_flags)
    else:
        w = int(WIN_RES["w"]) * SCALE
        h = int(WIN_RES["h"]) * SCALE
        window = pygame.display.set_mode((w,h), window_flags)
    
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_img("icon.png", IMG_DIR, 1))
    pygame.mouse.set_visible(False)

    # Create a scene manager
    manager = SceneManager(TitleScene(P_Prefs))

    # Create Render target
    render_target = pygame.Surface((WIN_RES["w"], WIN_RES["h"]))

    # Loop variables
    clock = pygame.time.Clock()
    running = True
    prev_time = time.time()
    dt = 0

    while running:
        # Fill window
        window.fill("BLACK")

        # Lock FPS
        clock.tick(FPS)
        #pygame.display.set_caption(f"{TITLE} (FPS: {round(clock.get_fps(),2)})")

        # Calculate delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        # Check for QUIT event
        if pygame.event.get(QUIT) or \
           (type(manager.scene) == TitleScene and manager.scene.exit): # This is a dumb hack but it will work for now.
            # Save player preferences
            try:
                with open(USERDAT_FILE, 'wb') as f:
                    pickle.dump(P_Prefs, f)
            except:
                print("ERROR: Failed to save.")
            
            # Exit loop and function
            running = False
            return

        # Call scene methods    
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update(dt)
        manager.scene.draw(render_target)   

        # Draw screen
        
        if (window_flags & FULLSCREEN) != 0:
            xscale = window.get_width() / WIN_RES["w"] / 2
            yscale = window.get_height() / WIN_RES["h"]
            targetx = int(WIN_RES["w"] * xscale)
            targety = int(WIN_RES["h"] * yscale)

            #window.blit(pygame.transform.scale(render_target, (round(WIN_RES["w"]*2.25), targety)), (window.get_rect().width / 2 - WIN_RES["w"]*1.125, 0))
            window.blit(
                pygame.transform.scale(
                    render_target,
                    (targetx, targety)
                ), 
                (window.get_width() / 2 - targetx / 2,0)
            )
        else:
            window.blit(pygame.transform.scale(render_target,(window.get_width(), window.get_height())),(0,0))

        pygame.display.flip()

if __name__ == "__main__":
    # Run main
    main()

    # Quit pygame
    pygame.quit()