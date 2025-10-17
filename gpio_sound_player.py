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
        
        # Track-specific playback configuration
        self.track_config = {
            0: {'mode': 'interrupt', 'self': 'ignore', 'priority': 3},    # Button 1
            1: {'mode': 'interrupt', 'self': 'ignore', 'priority': 1},       # Button 2
            2: {'mode': 'overlay', 'self': 'restart', 'priority': 2},    # Button 3
            3: {'mode': 'overlay', 'self': 'queue', 'priority': 1},        # Button 4
            4: {'mode': 'exclusive', 'self': 'ignore', 'priority': 5}      # Button 5
        }
        
        # Initialize pygame mixer for sound playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Setup GPIO
        self.setup_gpio()
        
        # Load sound files
        self.load_sounds()
        
        # Track button states to prevent multiple triggers
        self.button_states = [True] * 5  # True = not pressed (pull-up)
        
        # Track currently playing sounds
        self.currently_playing = {}  # {button_index: pygame.mixer.Channel}
        self.sound_channels = []     # List to store pygame channels
        
        print("GPIO Sound Player initialized!")
        print("Button GPIO pins:", self.button_pins)
        print("Track configurations loaded")
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
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        pygame.mixer.stop()
        self.currently_playing.clear()
        print("Stopped all sounds")
    
    def stop_lower_priority_sounds(self, priority):
        """Stop sounds with lower priority than the given priority"""
        to_remove = []
        for btn_idx, channel in self.currently_playing.items():
            if channel.get_busy():  # Still playing
                btn_priority = self.track_config[btn_idx].get('priority', 1)
                if btn_priority < priority:
                    channel.stop()
                    to_remove.append(btn_idx)
        
        for btn_idx in to_remove:
            del self.currently_playing[btn_idx]
            print(f"Stopped lower priority sound {btn_idx + 1}")
    
    def is_anything_playing(self):
        """Check if any sounds are currently playing"""
        # Clean up finished sounds
        to_remove = []
        for btn_idx, channel in self.currently_playing.items():
            if not channel.get_busy():
                to_remove.append(btn_idx)
        
        for btn_idx in to_remove:
            del self.currently_playing[btn_idx]
        
        return len(self.currently_playing) > 0
    
    def play_sound(self, button_index):
        """Play sound for the specified button with configuration rules"""
        if button_index >= len(self.sounds) or not self.sounds[button_index]:
            print(f"No sound available for button {button_index + 1}")
            return
        
        config = self.track_config.get(button_index, {'mode': 'overlay', 'self': 'restart', 'priority': 1})
        mode = config.get('mode', 'overlay')
        self_behavior = config.get('self', 'restart')
        priority = config.get('priority', 1)
        
        print(f"Button {button_index + 1} pressed - Mode: {mode}, Priority: {priority}")
        
        # Check if this same button is already playing
        if button_index in self.currently_playing:
            channel = self.currently_playing[button_index]
            if channel.get_busy():  # Still playing
                if self_behavior == 'ignore':
                    print(f"Button {button_index + 1} already playing, ignoring")
                    return
                elif self_behavior == 'restart':
                    channel.stop()
                    print(f"Restarting sound {button_index + 1}")
                # queue behavior would be handled here (more complex)
        
        # Handle interaction with other sounds
        if mode == 'interrupt':
            self.stop_all_sounds()
            print(f"Button {button_index + 1} interrupting all sounds")
        elif mode == 'exclusive':
            if self.is_anything_playing():
                print(f"Button {button_index + 1} blocked - other sounds playing")
                return
        elif mode == 'overlay':
            # Stop lower priority sounds only
            self.stop_lower_priority_sounds(priority)
        
        # Play the sound
        channel = self.sounds[button_index].play()
        if channel:
            self.currently_playing[button_index] = channel
            print(f"Playing sound {button_index + 1}: {self.sound_files[button_index]}")
        else:
            print(f"Failed to play sound {button_index + 1} - no available channels")
    
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