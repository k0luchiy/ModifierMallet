import os
import sys
import pygame

# Add the project root directory to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.controllers.game_controller import GameController

def main():
    # Initialize pygame before creating the game controller
    pygame.init()
    
    try:
        game = GameController()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()