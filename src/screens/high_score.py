"""
High score/results screen with star rating
Demonstrates: Inheritance, Composition
"""
import pygame
import math
from screens.base import BaseScreen
from ui.button import Button
from core.background import Background
from core.audio_manager import AudioManager
from utils.load_image import get_assets_path, load_image_fit

class HighScore(BaseScreen):
    """
    Results and high score screen
    Inheritance: Extends BaseScreen
    Composition: Contains Background and Button
    """
    
    def __init__(self, screen_width, screen_height, game_results=None):
        super().__init__(screen_width, screen_height)
        
        self._background = self._load_background('score.png')
        
        # Get audio manager
        self._audio = AudioManager()
        
        # Create button with audio
        self._back_button = Button(100, screen_height - 80, 150, 100, "Back", audio_manager=self._audio, image_name='button-back.png')
        
        # Play victory sound
        self._audio.play_sound('victory')
        
        # Game results
        self._results = game_results or {
            'score': 0,
            'total_caught': 0,
            'good_caught': 0,
            'bad_caught': 0,
            'accuracy': 0,
            'time_played': 0
        }
        
        # Animation state
        self._time = 0
        self._star_scale = [0, 0, 0]
        self._target_stars = self._calculate_stars()
    
    def _calculate_stars(self):
        """Calculate star rating based on score"""
        score = self._results['score']
        if score >= 100:
            return 3
        elif score >= 50:
            return 2
        elif score >= 20:
            return 1
        return 0
    
    def handle_event(self, event):
        """Handle high score screen events"""
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self._back_button.is_clicked(mouse_pos, True):
                self.set_next_screen('MAIN_MENU')
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.set_next_screen('MAIN_MENU')
    
    def update(self):
        """Update high score screen"""
        self._time += 0.05
        
        # Animate stars appearing
        for i in range(self._target_stars):
            if self._star_scale[i] < 1.0:
                self._star_scale[i] += 0.05
                if self._star_scale[i] > 1.0:
                    self._star_scale[i] = 1.0
        
        # Update button
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        self._back_button.update(mouse_pos, mouse_pressed)
    
    def draw(self, screen):
        """Draw high score screen"""
        # Draw background
        screen.blit(self._background, (0, 0))
        
        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("HASIL PERMAINAN", True, (251, 191, 36))
        title_rect = title_text.get_rect(center=(self._width // 2, 60))
        screen.blit(title_text, title_rect)
        
        # Draw stars with animation
        self._draw_animated_stars(screen)
        
        # Draw statistics
        self._draw_statistics(screen)
        
        # Draw rating message
        self._draw_rating_message(screen)
        
        # Draw button
        self._back_button.draw(screen)
    
    def _draw_animated_stars(self, screen):
        """Draw stars with scale animation"""
        star_y = 150
        star_spacing = 80
        start_x = self._width // 2 - star_spacing
        
        for i in range(3):
            star_x = start_x + i * star_spacing
            
            # Determine if this star should be filled
            if i < self._target_stars:
                color = (251, 191, 36)
                scale = self._star_scale[i]
            else:
                color = (100, 100, 100)
                scale = 1.0
            
            # Draw star with scale
            size = int(30 * scale)
            if size > 0:
                self._draw_star(screen, star_x, star_y, size, color)
    
    def _draw_star(self, screen, x, y, size, color):
        """Draw a star shape"""
        points = []
        for i in range(5):
            angle = math.pi / 2 + (2 * math.pi * i) / 5
            point_x = x + size * math.cos(angle)
            point_y = y - size * math.sin(angle)
            points.append((point_x, point_y))
            
            # Inner point
            angle = math.pi / 2 + (2 * math.pi * i) / 5 + math.pi / 5
            point_x = x + (size * 0.4) * math.cos(angle)
            point_y = y - (size * 0.4) * math.sin(angle)
            points.append((point_x, point_y))
        
        pygame.draw.polygon(screen, color, points)
    
    def _draw_star_glow(self, screen, x, y, size, color, alpha):
        """Draw star glow effect"""
        glow_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        
        for i in range(5):
            angle = math.pi / 2 + (2 * math.pi * i) / 5
            point_x = size * 1.5 + size * math.cos(angle)
            point_y = size * 1.5 - size * math.sin(angle)
            
            # Draw fading circles for glow
            for j in range(3):
                glow_radius = int(size * 0.3 * (3 - j))
                glow_alpha = alpha // (j + 1)
                glow_color = (*color, glow_alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (int(point_x), int(point_y)), glow_radius)
        
        screen.blit(glow_surface, (x - size * 1.5, y - size * 1.5))
    
    def _draw_statistics(self, screen):
        """Draw game statistics"""
        stats_font = pygame.font.Font(None, 42)
        y_start = 240
        line_height = 50
        
        stats = [
            f"Score Akhir: {self._results['score']}",
            f"Total Tangkapan: {self._results['total_caught']}",
            f"Makanan Segar: {self._results['good_caught']}",
            f"Makanan Busuk: {self._results['bad_caught']}",
            f"Akurasi: {self._results['accuracy']:.1f}%",
            f"Waktu Bermain: {self._results['time_played']:.1f}s"
        ]
        
        for i, stat in enumerate(stats):
            # Alternating colors for readability
            color = (255, 255, 255)
            stat_text = stats_font.render(stat, True, color)
            stat_rect = stat_text.get_rect(center=(self._width // 2, y_start + i * line_height))
            screen.blit(stat_text, stat_rect)
    
    def _draw_rating_message(self, screen):
        """Draw rating message based on performance"""
        messages = [
            "Ayo coba lagi!",
            "Lumayan!",
            "Bagus sekali!",
            "Sempurna!"
        ]
        
        message = messages[self._target_stars]
        message_font = pygame.font.Font(None, 48)
        message_text = message_font.render(message, True, (251, 191, 36))
        message_rect = message_text.get_rect(center=(self._width // 2, 520))
        screen.blit(message_text, message_rect)
