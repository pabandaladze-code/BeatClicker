from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BEATMAP_FILE = BASE_DIR / "beatmap.json"
CSV_FILE = BASE_DIR / "beat_scores.csv"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
GRAY = (50, 50, 70)
RED = (255, 70, 70)
GREEN = (70, 255, 70)
BLUE = (70, 130, 255)
YELLOW = (255, 220, 50)