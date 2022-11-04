from os import path

ROOT_DIR = path.dirname(path.realpath(__file__))

# Font
DEFAULT_FONT_LOC = path.join(ROOT_DIR, "milky_honey.ttf")
SMALL_FONT_SIZE = 24
LARGE_FONT_SIZE = 60
TITLE_FONT_SIZE = 80

# Buttons
SMALL_BUTTON_SIZE = 100,40
SMALL_BUTTON_BORDER = 5

LARGE_BUTTON_SIZE = 250,100
LARGE_BUTTON_BORDER = 10

# Images
IMG_DIR = path.join(ROOT_DIR, "img")
MENU_BG_FILE = "menuBG.png"
MENU_FG_FILE = "menuFG.png"
GAME_BG_FILE = "gameBG.png"
OPENED_BOTTLE_FILE = "opened_bottle.png"
CLOSED_BOTTLE_FILE = "closed_bottle.png"
MENU_BOTTLE_FILE = "menu_bottle.png"
BOTTLE_CAP_FILE = "bottle_cap.png"
BAR_FILE = "bar.png"

# Events
BEER_SPAWN_EVENT = 0
BEER_INC_EVENT = 1
TO_MENU_EVENT = 3
MENU_BEER_SPAWN_EVENT = 4

# Audio
AUDIO_MAIN_PATH = path.join(ROOT_DIR, "sounds")
AUDIO_LAND_PATH = path.join(AUDIO_MAIN_PATH, "land")
AUDIO_BOTTLE_SPAWN_PATH = path.join(AUDIO_MAIN_PATH, "bottle_spawn")
AUDIO_BUTTON_PATH = path.join(AUDIO_MAIN_PATH, "button")

# Other
TITLE = "PYNT"
WINDOW_CAPTION = "beer"
RANDOM_SEED = "beer"
FPS = 60    # Framerate and physics update rate are identical
HIGH_SCORE_PATH = path.join(ROOT_DIR, "high_score.txt")