# GPIO Sound Player

A Python script that plays sound files when GPIO buttons are pressed on a Raspberry Pi.

## Features

- 5 GPIO buttons trigger 5 different sound files
- Debounced button input to prevent multiple triggers
- Support for various audio formats (WAV, MP3, OGG)
- Clean shutdown with Ctrl+C
- Automatic GPIO cleanup

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- 5 push buttons
- Jumper wires
- Optional: breadboard for easier connections

## Wiring Diagram

Connect each button between a GPIO pin and GND:

```
Button 1: GPIO 18 ──┤ Button ├── GND
Button 2: GPIO 19 ──┤ Button ├── GND  
Button 3: GPIO 20 ──┤ Button ├── GND
Button 4: GPIO 21 ──┤ Button ├── GND
Button 5: GPIO 26 ──┤ Button ├── GND
```

The script uses internal pull-up resistors, so no external resistors are needed.

## Software Setup

### 1. Run Setup Script (on Raspberry Pi)

```bash
chmod +x setup.sh
bash setup.sh
```

### 2. Manual Installation

```bash
# Create sounds directory
mkdir sounds

# Install dependencies
sudo apt update
sudo apt install python3-pygame python3-rpi.gpio

# Or use pip
pip3 install pygame RPi.GPIO
```

### 3. Add Sound Files

Place your sound files in the `sounds` directory:

```
sounds/
├── sound1.wav
├── sound2.wav
├── sound3.wav
├── sound4.wav
└── sound5.wav
```

Supported formats: WAV, MP3, OGG

## Usage

### Run the Script

```bash
python3 gpio_sound_player.py
```

If you get permission errors:

```bash
sudo python3 gpio_sound_player.py
```

### Controls

- Press any connected button to play its corresponding sound
- Press Ctrl+C to exit cleanly

## Configuration

### Change GPIO Pins

Edit the `button_pins` list in `gpio_sound_player.py`:

```python
self.button_pins = [18, 19, 20, 21, 26]  # Change these pin numbers
```

### Change Sound Files

Edit the `sound_files` list in `gpio_sound_player.py`:

```python
self.sound_files = [
    'sounds/your_sound1.wav',
    'sounds/your_sound2.wav',
    # ... add more files
]
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Run with `sudo`
2. **GPIO Already in Use**: Make sure no other GPIO programs are running
3. **No Sound**: Check audio output settings and file paths
4. **Module Not Found**: Install missing dependencies

### Test Audio

```bash
# Test audio output
speaker-test -t sine -f 1000 -l 1

# Test pygame audio
python3 -c "import pygame; pygame.mixer.init(); print('Audio initialized successfully')"
```

### Debug Mode

Add debug prints to see button states:

```python
# In the check_buttons method, add:
print(f"Button {i+1} state: {current_state}")
```

## GPIO Pin Reference

| Button | GPIO Pin | Physical Pin |
|--------|----------|--------------|
| 1      | 18       | 12           |
| 2      | 19       | 35           |
| 3      | 20       | 38           |
| 4      | 21       | 40           |
| 5      | 26       | 37           |

## License

This project is open source. Feel free to modify and use as needed.

## Future Enhancements

- Volume control per button
- LED indicators for button presses
- Web interface for remote control
- MIDI support
- Looping sounds
- Multiple sound banks