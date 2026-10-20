import pygame
import sys
import json
import csv
import random
from constants import *

def load_beatmap():
    """Загрузка нот из JSON (ЛР 2)"""
    try:
        with open(BEATMAP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"bpm": 120, "notes": [1.0, 2.0, 3.0, 4.0, 5.0]}

def save_score(name: str, score: int, max_combo: int):
    """Сохранение результатов в CSV (ЛР 2)"""
    file_exists = CSV_FILE.exists() and CSV_FILE.stat().st_size > 0
    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Имя", "Очки", "Макс. Комбо"])
            writer.writerow([name, score, max_combo])
    except OSError as e:
        print(f"Ошибка записи CSV: {e}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ритм-Автомат (Beat Clicker) - Вариант 4")
    clock = pygame.time.Clock()

    beatmap = load_beatmap()
    note_times = beatmap.get("notes", [])

    score = 0
    combo = 0
    max_combo = 0
    
    active_notes = []
    start_time = pygame.time.get_ticks()
    note_index = 0

    font = pygame.font.SysFont(None, 28)
    game_over = False

    running = True
    while running:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                hit_success = False
                
                for note in active_notes[:]:
                    dist = ((note["x"] - mouse_pos[0])**2 + (note["y"] - mouse_pos[1])**2)**0.5
                    if dist <= 35:
                        delta = abs(note["ring_radius"] - 30)
                        if delta < 15:
                            score += 100 * (1 + combo // 5)
                            combo += 1
                            max_combo = max(max_combo, combo)
                            hit_success = True
                        else:
                            combo = 0
                        active_notes.remove(note)
                        break
                if not hit_success and active_notes:
                    combo = 0

        # Спавн нот по таймингам из JSON (ЛР 2)
        if note_index < len(note_times):
            if current_time >= note_times[note_index]:
                active_notes.append({
                    "x": random.randint(100, SCREEN_WIDTH - 100),
                    "y": random.randint(100, SCREEN_HEIGHT - 100),
                    "spawn_time": current_time,
                    "ring_radius": 100
                })
                note_index += 1
        elif not active_notes and not game_over and note_index >= len(note_times):
            game_over = True
            save_score("Polina", score, max_combo)

        # Сужение колец (ЛР 1)
        for note in active_notes[:]:
            elapsed = current_time - note["spawn_time"]
            progress = elapsed / 1.0
            note["ring_radius"] = max(30, int(100 - 70 * progress))
            
            if progress > 1.2:
                active_notes.remove(note)
                combo = 0

        # Отрисовка
        screen.fill(BLACK)

        for note in active_notes:
            pygame.draw.circle(screen, BLUE, (note["x"], note["y"]), 30)
            pygame.draw.circle(screen, YELLOW, (note["x"], note["y"]), note["ring_radius"], 3)

        score_text = font.render(f"Score: {score}  |  Combo: {combo} (Max: {max_combo})", True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            end_text = font.render("Track Finished! Score saved to CSV.", True, GREEN)
            screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()