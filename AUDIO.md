# 🎵 Audio System Documentation

## Overview

Game Nusantara Food Catcher menggunakan sistem audio lengkap dengan:
- **Procedural Sound Generation** - Suara dibuat real-time menggunakan waveform
- **Background Music Support** - Optional music files (MP3/OGG)
- **Sound Effects** - Berbagai sound untuk gameplay events
- **Volume Control** - Separate controls untuk music dan SFX

---

## 🔊 Sound Effects

### 1. **Click Sound** (Beep)
- **Trigger**: Saat tombol diklik
- **Frequency**: 440Hz (Note A4)
- **Duration**: 50ms
- **Waveform**: Sine wave dengan envelope

### 2. **Good Catch** (Rising Tone)
- **Trigger**: Saat tangkap makanan segar (+5 score)
- **Frequency**: 440Hz → 880Hz (A4 → A5)
- **Duration**: 150ms
- **Waveform**: Frequency sweep (chirp)
- **Effect**: Suara naik memberi feedback positif

### 3. **Bad Catch** (Falling Tone)
- **Trigger**: Saat tangkap makanan busuk (-1 HP)
- **Frequency**: 440Hz → 220Hz (A4 → A3)
- **Duration**: 150ms
- **Waveform**: Frequency sweep descending
- **Effect**: Suara turun memberi feedback negatif

### 4. **Game Over** (Descending Tones)
- **Trigger**: Saat game berakhir
- **Notes**: A (440Hz) → F (349Hz) → D (294Hz)
- **Duration**: 200ms per tone
- **Effect**: Sequence menurun memberi rasa selesai

### 5. **Victory** (Fanfare)
- **Trigger**: Saat masuk high score screen
- **Notes**: C (523Hz) → E (659Hz) → G (784Hz) → C (1047Hz)
- **Duration**: 120ms per tone
- **Effect**: Arpeggio naik memberi rasa pencapaian

---

## 🎵 Background Music (Optional)

Game supports optional background music files. Jika tidak ada file, game tetap berjalan normal tanpa musik.

### Folder Structure:
```
assets/
└─ sounds/
   ├─ menu_music.mp3     # Menu utama (optional)
   └─ game_music.mp3     # Gameplay (optional)
```

### Supported Formats:
- **MP3** - Most common, good compression
- **OGG** - Open format, good quality
- **WAV** - Uncompressed, largest file size

### Music Transitions:
- **Main Menu** → Play menu_music.mp3 (loop)
- **Game Start** → Stop menu music, play game_music.mp3 (loop)
- **Game Over** → Stop game music
- **Back to Menu** → Restart menu music

---

## 🎚️ Technical Implementation

### AudioManager Class
Singleton pattern untuk centralized audio management:

```python
class AudioManager:
    _instance = None  # Singleton
    
    Methods:
    - play_sound(name)           # Play SFX
    - play_music(name, loop)     # Play background music
    - stop_music()               # Stop music
    - set_music_volume(vol)      # 0.0 to 1.0
    - set_sfx_volume(vol)        # 0.0 to 1.0
```

### Sound Generation
Uses **numpy** for waveform generation:

```python
# Simple beep
frequency = 440  # Hz
duration = 0.05  # seconds
samples = int(sample_rate * duration)
wave = np.sin(2 * np.pi * frequency * t)

# Apply envelope (fade in/out)
envelope = create_fade_envelope(samples)
wave *= envelope

# Convert to pygame Sound
sound = pygame.sndarray.make_sound(stereo_wave)
```

### Advantages:
- ✅ **No External Files Needed** - Works out of the box
- ✅ **Lightweight** - Small memory footprint
- ✅ **Customizable** - Easy to modify frequencies/durations
- ✅ **Instant Playback** - No loading delays

---

## 🔧 Customization Guide

### Mengubah Volume Default

Edit `core/audio_manager.py`:
```python
def __init__(self):
    self._music_volume = 0.5  # Default: 0.5 (50%)
    self._sfx_volume = 0.7    # Default: 0.7 (70%)
```

### Mengubah Sound Frequencies

Edit `core/audio_manager.py`:

```python
# Click sound - ubah frequency
self._sounds['click'] = self._generate_beep(550, 50)  # Was 440

# Good catch - ubah range
self._sounds['good_catch'] = self._generate_sweep(500, 1000, 150)

# Bad catch - ubah range  
self._sounds['bad_catch'] = self._generate_sweep(500, 250, 150)
```

### Menambahkan Music Files

1. Buat folder:
```bash
mkdir -p assets/sounds
```

2. Copy music files:
```bash
# Download atau copy file MP3/OGG
cp your_menu_music.mp3 assets/sounds/menu_music.mp3
cp your_game_music.mp3 assets/sounds/game_music.mp3
```

3. Game will auto-detect dan play!

### Disable Audio Completely

Edit `core/audio_manager.py`:
```python
def __init__(self):
    self._audio_available = False  # Force disable
    return
```

---

## 📊 Performance Notes

### CPU Usage:
- **Procedural sound generation**: ~1-2ms per sound (on init)
- **Playback**: Minimal CPU usage
- **Music streaming**: Handled by pygame.mixer

### Memory Usage:
- Each sound effect: ~10-50KB
- Total audio system: ~200KB in memory
- Music files: Streamed from disk (not loaded to RAM)

### Optimization:
- Sounds generated once on init, cached
- Singleton pattern prevents multiple AudioManager instances
- Graceful fallback if audio unavailable

---

## 🐛 Troubleshooting

### No Sound?

**Check 1**: Audio device available?
```python
# Game will print if audio fails:
"Audio not available: [error message]"
```

**Check 2**: System volume not muted?
- Check OS volume mixer
- Check game process volume

**Check 3**: Numpy installed?
```bash
pip install numpy
```

### Sound Crackling/Distorted?

**Solution 1**: Adjust buffer size
```python
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
# Try buffer=1024 or buffer=2048
```

**Solution 2**: Lower sample rate
```python
pygame.mixer.init(frequency=22050, ...)  # Try 11025 or 44100
```

### Music Not Playing?

**Check 1**: File exists?
```bash
ls assets/sounds/menu_music.mp3
```

**Check 2**: File format supported?
- MP3, OGG, WAV are supported
- Other formats may not work

**Check 3**: Volume not zero?
```python
self._music_volume = 0.5  # Make sure > 0
```

---

## 🎓 Learning Resources

### Audio Programming Concepts:
- **Sample Rate**: 22050 Hz (samples per second)
- **Bit Depth**: 16-bit signed integer
- **Channels**: 2 (stereo)
- **Waveforms**: Sine, sawtooth, square, noise
- **Envelope**: ADSR (Attack, Decay, Sustain, Release)
- **Frequency**: Hz (cycles per second), musical notes

### Musical Notes Reference:
```
C4  = 261.63 Hz
D4  = 293.66 Hz
E4  = 329.63 Hz
F4  = 349.23 Hz
G4  = 392.00 Hz
A4  = 440.00 Hz (standard tuning)
B4  = 493.88 Hz
C5  = 523.25 Hz
```

### Further Reading:
- [Pygame Mixer Documentation](https://www.pygame.org/docs/ref/mixer.html)
- [NumPy Audio Processing](https://numpy.org/doc/stable/reference/generated/numpy.sin.html)
- [Digital Audio Fundamentals](https://en.wikipedia.org/wiki/Digital_audio)

---

## 🎮 Audio in Gameplay

### Feedback Loop:
```
Player Action → Audio Feedback → Emotional Response

Good catch:
  Click basket → Rising tone → "Yay! Good job!"
  
Bad catch:
  Click basket → Falling tone → "Oops, avoid that!"
  
Button click:
  Click → Beep → "Action confirmed"
```

### Audio Design Principles:
1. **Immediate Feedback** - Sound plays instantly on action
2. **Clear Distinction** - Good vs bad sounds are obviously different
3. **Not Annoying** - Short duration, pleasant tones
4. **Optional** - Game works without audio
5. **Performance** - No lag or stuttering

---

## 🔮 Future Enhancements

### Possible Additions:
- [ ] Volume sliders in settings menu
- [ ] More sound variations
- [ ] Combo catch sounds (when catching multiple rapidly)
- [ ] Warning sound when HP low
- [ ] Timer countdown beeps
- [ ] Achievement unlock sounds
- [ ] Music fade in/out transitions

### Advanced Features:
- [ ] Dynamic music based on score
- [ ] 3D positional audio (items from left/right)
- [ ] Sound mixing (multiple sounds simultaneously)
- [ ] Audio visualization (waveform display)

---

**Enjoy the audio experience! 🎵🎮**
