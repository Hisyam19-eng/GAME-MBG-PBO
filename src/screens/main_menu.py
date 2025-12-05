"""
Main menu screen with animations
Demonstrates: Inheritance (extends BaseScreen), Composition (contains Buttons)
"""
import pygame
import math
from screens.base import BaseScreen
from ui.button import Button
from core.background import Background
from core.audio_manager import AudioManager


class MainMenu(BaseScreen):
    """
    Main menu screen
    Inheritance: Extends BaseScreen
    Composition: Contains Background and Buttons
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # Composition: Menu contains these components
        self._background = Background(screen_width, screen_height)
        
        # Get audio manager
        self._audio = AudioManager()
        
        # Create buttons with audio
        center_x = screen_width // 2
        self._play_button = Button(center_x, 280, 200, 60, "MAIN", audio_manager=self._audio)
        self._highscore_button = Button(center_x, 360, 200, 60, "HIGH SCORE", audio_manager=self._audio)
        self._quit_button = Button(center_x, 440, 200, 60, "KELUAR", audio_manager=self._audio)
        
        # Play menu music
        self._audio.play_music('menu_music', loop=True)
        
        # Animation state
        self._title_offset = 0
        self._time = 0
    
    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            
            if self._play_button.is_clicked(mouse_pos, True):
                self.set_next_screen('GAME')
            elif self._highscore_button.is_clicked(mouse_pos, True):
                # For now, show a placeholder message
                print("High Score screen - akan diimplementasikan di game screen")
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
        # Draw background
        self._background.draw(screen)
        
        # Draw title with shadow
        title_font = pygame.font.Font(None, 84)
        subtitle_font = pygame.font.Font(None, 42)
        
        # Title shadow
        title_shadow = title_font.render("NUSANTARA", True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(self._width // 2 + 4, 120 + self._title_offset + 4))
        screen.blit(title_shadow, shadow_rect)
        
        # Title
        title_text = title_font.render("NUSANTARA", True, (251, 191, 36))
        title_rect = title_text.get_rect(center=(self._width // 2, 120 + self._title_offset))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = subtitle_font.render("Food Catcher", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self._width // 2, 180 + self._title_offset))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw decorative elements
        self._draw_decorations(screen)
        
        # Draw buttons
        self._play_button.draw(screen)
        self._highscore_button.draw(screen)
        self._quit_button.draw(screen)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 28)
        instruction_text = instruction_font.render("Use ← → or A D to move", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(self._width // 2, self._height - 40))
        screen.blit(instruction_text, instruction_rect)
    
    def _draw_decorations(self, screen):
        """Draw decorative elements on menu"""
        # Draw some floating food icons
        time_offset = self._time * 2
        
        for i in range(6):
            angle = (i / 6) * 2 * math.pi + time_offset
            x = self._width // 2 + math.cos(angle) * 220
            y = 150 + math.sin(angle) * 80
            
            # Alternating good and bad items
            if i % 2 == 0:
                color = (34, 197, 94)  # Green
            else:
                color = (239, 68, 68)  # Red
            
            pygame.draw.circle(screen, color, (int(x), int(y)), 12)
            pygame.draw.circle(screen, (255, 255, 255), (int(x - 3), int(y - 3)), 4)
