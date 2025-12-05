"""
Audio Manager for game sounds and music
Singleton pattern for centralized audio management
"""
import pygame
import numpy as np
import os


class AudioManager:
    """
    Singleton audio manager
    Handles music and sound effects with procedural generation
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._audio_available = False
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._audio_available = True
        except Exception as e:
            print(f"Audio not available: {e}")
            return
        
        # Volume settings
        self._music_volume = 0.5
        self._sfx_volume = 0.7
        
        # Sound cache
        self._sounds = {}
        
        # Generate procedural sounds
        self._generate_sounds()
        
        # Music state
        self._current_music = None
    
    def _generate_sounds(self):
        """Generate procedural sound effects"""
        if not self._audio_available:
            return
        
        try:
            # Click sound - short beep
            self._sounds['click'] = self._generate_beep(440, 50)
            
            # Good catch - rising tone
            self._sounds['good_catch'] = self._generate_sweep(440, 880, 150)
            
            # Bad catch - falling tone  
            self._sounds['bad_catch'] = self._generate_sweep(440, 220, 150)
            
            # Game over - descending tones
            self._sounds['game_over'] = self._generate_game_over()
            
            # Victory - ascending fanfare
            self._sounds['victory'] = self._generate_victory()
            
        except Exception as e:
            print(f"Error generating sounds: {e}")
    
    def _generate_beep(self, frequency, duration_ms):
        """Generate a simple beep sound"""
        try:
            sample_rate = 22050
            duration = duration_ms / 1000.0
            samples = int(sample_rate * duration)
            
            # Generate sine wave
            t = np.linspace(0, duration, samples, False)
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Apply envelope (fade in/out)
            envelope = np.ones(samples)
            fade_samples = int(samples * 0.1)
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            wave *= envelope
            
            # Convert to 16-bit
            wave = (wave * 32767).astype(np.int16)
            
            # Make stereo
            stereo_wave = np.column_stack((wave, wave))
            
            return pygame.sndarray.make_sound(stereo_wave)
        except Exception as e:
            print(f"Error generating beep: {e}")
            return None
    
    def _generate_sweep(self, start_freq, end_freq, duration_ms):
        """Generate a frequency sweep (chirp)"""
        try:
            sample_rate = 22050
            duration = duration_ms / 1000.0
            samples = int(sample_rate * duration)
            
            # Generate frequency sweep
            t = np.linspace(0, duration, samples, False)
            freq = np.linspace(start_freq, end_freq, samples)
            phase = 2 * np.pi * np.cumsum(freq) / sample_rate
            wave = np.sin(phase)
            
            # Apply envelope
            envelope = np.ones(samples)
            fade_samples = int(samples * 0.1)
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            wave *= envelope * 0.3  # Lower volume
            
            # Convert to 16-bit
            wave = (wave * 32767).astype(np.int16)
            
            # Make stereo
            stereo_wave = np.column_stack((wave, wave))
            
            return pygame.sndarray.make_sound(stereo_wave)
        except Exception as e:
            print(f"Error generating sweep: {e}")
            return None
    
    def _generate_game_over(self):
        """Generate game over sound effect"""
        try:
            # Three descending tones
            frequencies = [440, 349, 294]  # A, F, D
            duration_each = 200
            
            sounds = []
            for freq in frequencies:
                sound = self._generate_beep(freq, duration_each)
                if sound:
                    sounds.append(sound)
            
            # Combine sounds (play first one, others will queue)
            return sounds[0] if sounds else None
        except Exception as e:
            print(f"Error generating game over sound: {e}")
            return None
    
    def _generate_victory(self):
        """Generate victory fanfare"""
        try:
            # Ascending arpeggio
            frequencies = [523, 659, 784, 1047]  # C, E, G, C
            duration_each = 120
            
            sounds = []
            for freq in frequencies:
                sound = self._generate_beep(freq, duration_each)
                if sound:
                    sounds.append(sound)
            
            return sounds[0] if sounds else None
        except Exception as e:
            print(f"Error generating victory sound: {e}")
            return None
    
    def play_sound(self, sound_name):
        """
        Play a sound effect
        
        Args:
            sound_name: Name of sound ('click', 'good_catch', 'bad_catch', etc.)
        """
        if not self._audio_available:
            return
        
        try:
            sound = self._sounds.get(sound_name)
            if sound:
                sound.set_volume(self._sfx_volume)
                sound.play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def play_music(self, music_name, loop=True):
        """
        Play background music
        
        Args:
            music_name: Name of music file (without extension)
            loop: Whether to loop the music
        """
        if not self._audio_available:
            return
        
        try:
            # Check if music file exists
            music_path = None
            for ext in ['.mp3', '.ogg', '.wav']:
                path = f"assets/sounds/{music_name}{ext}"
                if os.path.exists(path):
                    music_path = path
                    break
            
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self._music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self._current_music = music_name
            else:
                # No music file - silent is okay
                pass
        except Exception as e:
            print(f"Error playing music {music_name}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if not self._audio_available:
            return
        
        try:
            pygame.mixer.music.stop()
            self._current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def set_music_volume(self, volume):
        """
        Set music volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._music_volume = max(0.0, min(1.0, volume))
        if self._audio_available:
            try:
                pygame.mixer.music.set_volume(self._music_volume)
            except Exception as e:
                print(f"Error setting music volume: {e}")
    
    def set_sfx_volume(self, volume):
        """
        Set sound effects volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._sfx_volume = max(0.0, min(1.0, volume))
    
    def cleanup(self):
        """Cleanup audio resources"""
        if not self._audio_available:
            return
        
        try:
            self.stop_music()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error cleaning up audio: {e}")
    
    @property
    def is_available(self):
        """Check if audio is available"""
        return self._audio_available
