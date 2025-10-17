#!/usr/bin/env python3
"""
GPIO Sound Player Script
Plays different sound files when GPIO buttons are pressed.
Designed for Raspberry Pi with 5 buttons connected to GPIO pins.

Required libraries:
- RPi.GPIO (for Raspberry Pi GPIO control)
- pygame (for sound playback)

Install with:
pip install RPi.GPIO pygame

Hardware Setup:
- Connect 5 push buttons between GPIO pins and GND
- Use internal pull-up resistors (configured in code)
- Button press = LOW signal (button connects GPIO to GND)
"""

import RPi.GPIO as GPIO
import pygame
import time
import os
import sys
from threading import Thread

class SoundPlayer:
    def __init__(self):
        # GPIO pin configuration for buttons (BCM numbering)
        self.button_pins = [18, 19, 20, 21, 26]  # GPIO pins for 5 buttons
        
        # Sound file paths - place your sound files in a 'sounds' directory
        self.sound_files = [
            'sounds/sound1.wav',
            'sounds/sound2.wav', 
            'sounds/sound3.wav',
            'sounds/sound4.wav',
            'sounds/sound5.wav'
        ]
        
        # Initialize pygame mixer for sound playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Setup GPIO
        self.setup_gpio()
        
        # Load sound files
        self.load_sounds()
        
        # Track button states to prevent multiple triggers
        self.button_states = [True] * 5  # True = not pressed (pull-up)
        
        print("GPIO Sound Player initialized!")
        print("Button GPIO pins:", self.button_pins)
        print("Press Ctrl+C to exit")
    
    def setup_gpio(self):
        """Configure GPIO pins for button input"""
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        
        for pin in self.button_pins:
            # Setup as input with internal pull-up resistor
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print(f"Configured GPIO {pin} as input with pull-up")
    
    def load_sounds(self):
        """Load sound files and verify they exist"""
        self.sounds = []
        
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            print("Created 'sounds' directory. Please add your sound files:")
            for i, sound_file in enumerate(self.sound_files):
                print(f"  {i+1}. {sound_file}")
        
        for i, sound_file in enumerate(self.sound_files):
            if os.path.exists(sound_file):
                try:
                    sound = pygame.mixer.Sound(sound_file)
                    self.sounds.append(sound)
                    print(f"Loaded: {sound_file}")
                except pygame.error as e:
                    print(f"Error loading {sound_file}: {e}")
                    self.sounds.append(None)
            else:
                print(f"Warning: {sound_file} not found")
                self.sounds.append(None)
    
    def play_sound(self, button_index):
        """Play sound for the specified button"""
        if button_index < len(self.sounds) and self.sounds[button_index]:
            print(f"Playing sound {button_index + 1}: {self.sound_files[button_index]}")
            self.sounds[button_index].play()
        else:
            print(f"No sound available for button {button_index + 1}")
    
    def check_buttons(self):
        """Check button states and play sounds when pressed"""
        for i, pin in enumerate(self.button_pins):
            current_state = GPIO.input(pin)
            
            # Button pressed = LOW (False), Released = HIGH (True)
            if not current_state and self.button_states[i]:
                # Button just pressed (was released, now pressed)
                print(f"Button {i + 1} pressed (GPIO {pin})")
                self.play_sound(i)
                self.button_states[i] = False
            elif current_state and not self.button_states[i]:
                # Button just released (was pressed, now released)
                self.button_states[i] = True
    
    def run(self):
        """Main loop to monitor buttons"""
        try:
            while True:
                self.check_buttons()
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO and pygame resources"""
        print("Cleaning up GPIO...")
        GPIO.cleanup()
        pygame.mixer.quit()
        print("Cleanup complete")

def main():
    """Main function to run the sound player"""
    print("=== GPIO Sound Player ===")
    print("Make sure you're running this on a Raspberry Pi with GPIO access")
    print("Connect buttons between GPIO pins and GND")
    
    try:
        player = SoundPlayer()
        player.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're running on a Raspberry Pi")
        print("2. Run with sudo if you get permission errors: sudo python3 gpio_sound_player.py")
        print("3. Install required libraries: pip install RPi.GPIO pygame")
        print("4. Check GPIO connections and sound files")

if __name__ == "__main__":
    main()