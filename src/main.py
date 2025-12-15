"""
Main entry point for Cooking Rhythm MBG game
Demonstrates: Composition (contains screens), Exception Handling
"""
import pygame
import sys
from screens.main_menu import MainMenu
from screens.game_screen import GameScreen
from screens.high_score import HighScore
from core.audio_manager import AudioManager


class GameManager:
    """
    Main game manager with screen system
    Composition: Manages different screens
    Exception Handling: Graceful error recovery
    """
    
    def __init__(self):
        """Initialize game manager"""
        # Initialize Pygame
        try:
            pygame.init()
            pygame.font.init()
        except Exception as e:
            print(f"Failed to initialize Pygame: {e}")
            sys.exit(1)
        
        # Screen settings
        self._width = 1000
        self._height = 600
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Cooking Rhythm MBG")
        
        # Clock for FPS management
        self._clock = pygame.time.Clock()
        self._fps = 60
        
        # Screen management
        self._current_screen_name = 'MAIN_MENU'
        self._screens = {}
        self._current_screen = None
        
        # Initialize audio
        self._audio = AudioManager()
        
        # Initialize screens
        self._initialize_screens()
        
        # Running flag
        self._running = True
    
    def _initialize_screens(self):
        """Initialize all game screens"""
        try:
            self._screens['MAIN_MENU'] = MainMenu(self._width, self._height)
            self._screens['GAME'] = GameScreen(self._width, self._height)
            self._screens['HIGH_SCORE'] = HighScore(self._width, self._height)
            # High score screen will be created dynamically with results
            
            self._current_screen = self._screens['MAIN_MENU']
        except Exception as e:
            print(f"Error initializing screens: {e}")
            sys.exit(1)
    
    def _switch_screen(self, screen_name):
        """
        Switch to a different screen
        
        Args:
            screen_name: Name of screen to switch to
        """
        try:
            if screen_name == 'GAME':
                # Create new game screen for fresh game
                self._screens['GAME'] = GameScreen(self._width, self._height)
                self._current_screen = self._screens['GAME']
                self._current_screen_name = 'GAME'
            
            elif screen_name == 'HIGH_SCORE':
                # Create high score screen with game results
                game_screen = self._screens.get('GAME')
                if game_screen and hasattr(game_screen, '_game'):
                    results = game_screen._game.get_results()
                else:
                    results = None
                
                self._screens['HIGH_SCORE'] = HighScore(
                    self._width, self._height, results
                )
                self._current_screen = self._screens['HIGH_SCORE']
                self._current_screen_name = 'HIGH_SCORE'
            
            elif screen_name == 'MAIN_MENU':
                # Return to main menu
                self._screens['MAIN_MENU'] = MainMenu(self._width, self._height)
                self._current_screen = self._screens['MAIN_MENU']
                self._current_screen_name = 'MAIN_MENU'
            
            else:
                print(f"Unknown screen: {screen_name}")
        
        except Exception as e:
            print(f"Error switching to screen {screen_name}: {e}")
            # Fallback to main menu on error
            self._current_screen = self._screens['MAIN_MENU']
            self._current_screen_name = 'MAIN_MENU'
    
    def run(self):
        """Main game loop"""
        while self._running:
            try:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    else:
                        # Pass event to current screen
                        if self._current_screen:
                            self._current_screen.safe_handle_event(event)
                
                # Update current screen
                if self._current_screen:
                    self._current_screen.safe_update()
                    
                    # Check for screen transition
                    next_screen = self._current_screen.get_next_screen()
                    if next_screen:
                        self._switch_screen(next_screen)
                
                # Draw
                self._screen.fill((0, 0, 0))
                if self._current_screen:
                    self._current_screen.safe_draw(self._screen)
                
                pygame.display.flip()
                
                # Maintain FPS
                self._clock.tick(self._fps)
            
            except Exception as e:
                print(f"Error in main loop: {e}")
                # Try to continue running
                continue
        
        # Cleanup
        self._cleanup()
    
    def _cleanup(self):
        """Clean up resources"""
        try:
            # Cleanup audio
            self._audio.cleanup()
            pygame.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        sys.exit(0)


def main():
    """Main entry point"""
    try:
        game_manager = GameManager()
        game_manager.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
