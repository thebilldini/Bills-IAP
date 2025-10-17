#!/bin/bash
# Setup script for GPIO Sound Player

echo "=== GPIO Sound Player Setup ==="

# Create sounds directory
echo "Creating sounds directory..."
mkdir -p sounds

# Create example sound files list
echo "Creating example sound files..."
echo "Place your sound files (.wav, .mp3, .ogg) in the sounds directory:"
echo "  sounds/sound1.wav"
echo "  sounds/sound2.wav"
echo "  sounds/sound3.wav"
echo "  sounds/sound4.wav"
echo "  sounds/sound5.wav"

# Install Python dependencies (for Raspberry Pi)
echo ""
echo "Installing Python dependencies..."
echo "Note: Run this on your Raspberry Pi"

# Check if we're on a Raspberry Pi
if [[ $(uname -m) == "arm"* ]] || [[ $(uname -m) == "aarch64" ]]; then
    echo "Detected ARM architecture (likely Raspberry Pi)"
    
    # Special note for Pi Zero 2 W
    if grep -q "Pi Zero 2" /proc/device-tree/model 2>/dev/null; then
        echo "Raspberry Pi Zero 2 W detected - perfect for this project!"
    fi
    
    # Update package list
    sudo apt update
    
    # Install system dependencies
    sudo apt install -y python3-pygame python3-rpi.gpio python3-pip
    
    # Install via pip as backup
    pip3 install --user pygame RPi.GPIO
    
    echo "Dependencies installed successfully!"
else
    echo "Not running on Raspberry Pi - skipping GPIO library installation"
    echo "On Raspberry Pi, run: sudo apt install python3-pygame python3-rpi.gpio"
fi

echo ""
echo "Setup complete!"
echo "1. Add your sound files to the 'sounds' directory"
echo "2. Connect your buttons to GPIO pins 18, 19, 20, 21, 26"
echo "3. Run the script: python3 gpio_sound_player.py"
echo "   (or with sudo if needed: sudo python3 gpio_sound_player.py)"