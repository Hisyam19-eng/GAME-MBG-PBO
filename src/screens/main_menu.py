"""
Main menu screen with animations
Demonstrates: Inheritance (extends BaseScreen), Composition (contains Buttons)
"""
import pygame
import math
from screens.base import BaseScreen
from ui.button import Button
from core.audio_manager import AudioManager
from utils.load_image import get_assets_path, load_image_fit


class MainMenu(BaseScreen):
    """
    Main menu screen
    Inheritance: Extends BaseScreen
    Composition: Contains Background and Buttons
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # Load background image
        self._background = self._load_background('home.png')
        
        # Load logo image
        self._load_logo()
        
        # Get audio manager
        self._audio = AudioManager()
        
        # Create buttons with audio and images
        center_x = screen_width // 2
        self._play_button = Button(center_x, 310, 400, 125, "MAIN", audio_manager=self._audio, image_name='button-start.png')
        self._highscore_button = Button(center_x, 430, 250, 75, "HIGH SCORE", audio_manager=self._audio, image_name='button-score.png')
        self._quit_button = Button(center_x, 520, 250, 75, "KELUAR", audio_manager=self._audio, image_name='button-leave.png')
        
        # Play menu music
        self._audio.play_music('menu_music', loop=True)
        
        # Animation state
        self._title_offset = 0
        self._time = 0
    
    def _load_logo(self):
        """Load and prepare logo image"""
        try:
            logo_path = get_assets_path('images', 'logo.png')
            # Load logo with max dimensions to fit nicely above buttons
            self._logo, self._logo_width, self._logo_height = load_image_fit(
                logo_path, 
                max_width=400, 
                max_height=200, 
                convert_alpha=True
            )
        except Exception as e:
            print(f"Error loading logo: {e}")
            self._logo = None
    
    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            
            if self._play_button.is_clicked(mouse_pos, True):
                self.set_next_screen('GAME')
            elif self._highscore_button.is_clicked(mouse_pos, True):
                self.set_next_screen('HIGH_SCORE')
            elif self._quit_button.is_clicked(mouse_pos, True):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def update(self):
        """Update menu state"""
        self._time += 0.05
        
        # Floating animation for title
        self._title_offset = math.sin(self._time) * 10
        
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self._play_button.update(mouse_pos, mouse_pressed)
        self._highscore_button.update(mouse_pos, mouse_pressed)
        self._quit_button.update(mouse_pos, mouse_pressed)
    
    def draw(self, screen):
        """Draw menu"""
        # Draw background image
        screen.blit(self._background, (0, 0))
        
        # Draw logo with floating animation
        if self._logo:
            logo_y = 120 + self._title_offset
            logo_rect = self._logo.get_rect(center=(self._width // 2, logo_y))
            screen.blit(self._logo, logo_rect)
        
        # Draw buttons
        self._play_button.draw(screen)
        self._highscore_button.draw(screen)
        self._quit_button.draw(screen)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 28)
        instruction_text = instruction_font.render("Use ← → or A D to move", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(self._width // 2, self._height - 40))
        screen.blit(instruction_text, instruction_rect)
