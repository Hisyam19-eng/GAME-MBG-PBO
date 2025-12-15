"""
Game screen with particle effects and floating score text
Demonstrates: Inheritance, Composition, Exception Handling
"""
import pygame
import random
from screens.base import BaseScreen
from core.game import Game
from core.audio_manager import AudioManager


class Particle:
    """
    Particle for visual effects
    Simple composition component
    """
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.life = 30
        self.max_life = 30
        self.color = color
        self.size = random.randint(3, 6)
    
    def update(self):
        """Update particle position and life"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.life -= 1
    
    def draw(self, screen):
        """Draw particle with fade effect"""
        alpha_ratio = self.life / self.max_life
        size = int(self.size * alpha_ratio)
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
    
    @property
    def is_dead(self):
        return self.life <= 0


class FloatingText:
    """Floating score text when catching items"""
    
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 60
        self.max_life = 60
        self.vy = -2
    
    def update(self):
        """Update floating text"""
        self.y += self.vy
        self.life -= 1
    
    def draw(self, screen):
        """Draw floating text with fade"""
        alpha_ratio = self.life / self.max_life
        font = pygame.font.Font(None, 48)
        
        # Create text with color
        text_surface = font.render(self.text, True, self.color)
        
        # Apply alpha (fade out)
        text_surface.set_alpha(int(255 * alpha_ratio))
        
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)
    
    @property
    def is_dead(self):
        return self.life <= 0


class GameScreen(BaseScreen):
    """
    Active gameplay screen
    Inheritance: Extends BaseScreen
    Composition: Contains Game, Particles, FloatingTexts
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # Load background image
        self._background = self._load_background('play.png')
        
        # Composition: GameScreen contains Game
        self._game = Game(screen_width, screen_height)
        
        # Get audio manager
        self._audio = AudioManager()
        
        # Play game music
        self._audio.stop_music()  # Stop menu music
        self._audio.play_music('game_music', loop=True)
        
        # Visual effects (composition)
        self._particles = []
        self._floating_texts = []
        
        # Track previous item count to detect catches
        self._prev_item_count = 0
        self._last_score = 0
        self._last_hp = 3
        self._game_over_sound_played = False
        
        # Game over background
        self._game_over_background = None
        self._game_over_background_loaded = False
    
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Pause or return to menu
                self._audio.stop_music()
                self.set_next_screen('MAIN_MENU')
            elif event.key == pygame.K_r and self._game.is_game_over:
                # Restart game
                self._game = Game(self._width, self._height)
                self._particles.clear()
                self._floating_texts.clear()
                self._last_score = 0
                self._last_hp = 3
                self._game_over_sound_played = False
                self._game_over_background = None
                self._game_over_background_loaded = False
    
    def update(self):
        """Update game screen"""
        if not self._game.is_game_over:
            # Get keyboard state
            keys = pygame.key.get_pressed()
            self._game.handle_input(keys)
            self._game.update()
            
            # Check for score/hp changes to create effects
            self._check_for_catches()
        
        # Update particles
        for particle in self._particles[:]:
            particle.update()
            if particle.is_dead:
                self._particles.remove(particle)
        
        # Update floating texts
        for text in self._floating_texts[:]:
            text.update()
            if text.is_dead:
                self._floating_texts.remove(text)
        
        # Check if game is over
        if self._game.is_game_over:
            # Play game over sound once
            if not self._game_over_sound_played:
                self._audio.stop_music()
                self._audio.play_sound('game_over')
                self._game_over_sound_played = True
            
            # Load appropriate game over background
            if not self._game_over_background_loaded:
                self._load_game_over_background()
                self._game_over_background_loaded = True
    
    def _check_for_catches(self):
        """Check if item was caught and create effects"""
        current_score = self._game.score
        current_hp = self._game.hp
        
        # Score increased - good item caught
        if current_score > self._last_score:
            score_diff = current_score - self._last_score
            self._create_catch_effect(
                self._game._player.x,
                self._game._player.y,
                f"+{score_diff}",
                (34, 197, 94),
                (34, 197, 94)
            )
            self._last_score = current_score
            # Play good catch sound
            self._audio.play_sound('good_catch')
        
        # HP decreased - bad item caught
        if current_hp < self._last_hp:
            self._create_catch_effect(
                self._game._player.x,
                self._game._player.y,
                "-1",
                (239, 68, 68),
                (239, 68, 68)
            )
            self._last_hp = current_hp
            # Play bad catch sound
            self._audio.play_sound('bad_catch')
    
    def _create_catch_effect(self, x, y, text, text_color, particle_color):
        """
        Create particle effect and floating text
        
        Args:
            x, y: Position
            text: Text to show
            text_color: Color of text
            particle_color: Color of particles
        """
        try:
            # Create floating text
            floating_text = FloatingText(x, y - 30, text, text_color)
            self._floating_texts.append(floating_text)
            
            # Create particles
            for _ in range(15):
                particle = Particle(x, y, particle_color)
                self._particles.append(particle)
        except Exception as e:
            print(f"Error creating catch effect: {e}")
    
    def _get_stars_from_score(self, score):
        """
        Calculate number of stars based on score
        
        Args:
            score: Player's final score
            
        Returns:
            int: Number of stars (1-3)
        """
        if score >= 100:
            return 3
        elif score >= 50:
            return 2
        else:
            return 1
    
    def _load_game_over_background(self):
        """Load appropriate game over background based on score"""
        results = self._game.get_results()
        score = results['score']
        
        # Get number of stars
        stars = self._get_stars_from_score(score)
        
        # Load win.png if 2+ stars, else lose.png
        if stars >= 2:
            background_name = 'win.png'
        else:
            background_name = 'lose.png'
        
        self._game_over_background = self._load_background(background_name)
    
    def draw(self, screen):
        """Draw game screen"""
        # Draw appropriate background
        if self._game.is_game_over and self._game_over_background:
            # Draw game over background (win or lose)
            screen.blit(self._game_over_background, (0, 0))
        else:
            # Draw normal game background
            screen.blit(self._background, (0, 0))
        
        # Draw game (without its own background)
        self._game.draw(screen, draw_background=False)
        
        # Draw particles
        for particle in self._particles:
            particle.draw(screen)
        
        # Draw floating texts
        for text in self._floating_texts:
            text.draw(screen)
        
        # Draw game over screen if game is over
        if self._game.is_game_over:
            self._draw_game_over(screen)
    
    def _draw_game_over(self, screen):
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self._width, self._height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        font = pygame.font.Font(None, 84)
        game_over_text = font.render("GAME OVER", True, (251, 191, 36))
        game_over_rect = game_over_text.get_rect(center=(self._width // 2, self._height // 2 - 80))
        screen.blit(game_over_text, game_over_rect)
        
        # Results
        results_font = pygame.font.Font(None, 48)
        results = self._game.get_results()
        
        score_text = results_font.render(f"Score: {results['score']}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self._width // 2, self._height // 2))
        screen.blit(score_text, score_rect)
        
        caught_text = results_font.render(
            f"Caught: {results['good_caught']}/{results['total_caught']}",
            True, (255, 255, 255)
        )
        caught_rect = caught_text.get_rect(center=(self._width // 2, self._height // 2 + 50))
        screen.blit(caught_text, caught_rect)
        
        accuracy_text = results_font.render(
            f"Accuracy: {results['accuracy']:.1f}%",
            True, (255, 255, 255)
        )
        accuracy_rect = accuracy_text.get_rect(center=(self._width // 2, self._height // 2 + 100))
        screen.blit(accuracy_text, accuracy_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render(
            "Press R to restart or ESC for menu",
            True, (200, 200, 200)
        )
        instruction_rect = instruction_text.get_rect(center=(self._width // 2, self._height - 60))
        screen.blit(instruction_text, instruction_rect)
        
        # Draw stars based on score
        self._draw_stars(screen, results['score'])
    
    def _draw_stars(self, screen, score):
        """Draw star rating based on score"""
        # Get number of stars using shared logic
        stars = self._get_stars_from_score(score)
        
        # Draw stars
        star_y = self._height // 2 - 30
        star_spacing = 60
        start_x = self._width // 2 - (stars - 1) * star_spacing // 2
        
        for i in range(stars):
            star_x = start_x + i * star_spacing
            self._draw_star(screen, star_x, star_y, 20, (251, 191, 36))
    
    def _draw_star(self, screen, x, y, size, color):
        """Draw a star shape"""
        import math
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
