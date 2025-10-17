# Example sound files for testing
# Place actual sound files in this directory

# Supported formats:
# - .wav (recommended for best compatibility)
# - .mp3
# - .ogg

# Expected files:
# sound1.wav - Button 1 sound
# sound2.wav - Button 2 sound  
# sound3.wav - Button 3 sound
# sound4.wav - Button 4 sound
# sound5.wav - Button 5 sound

# You can download free sound effects from:
# - freesound.org
# - zapsplat.com
# - Adobe Audition (built-in sounds)
# - Or record your own!

# For testing, you can use system sounds:
# On Raspberry Pi OS: /usr/share/sounds/alsa/



🧭 Guide: Auto-Start a Python Audio Player on Raspberry Pi (with Auto-Login + systemd Service)

System:
Raspberry Pi 3 B+ running Raspberry Pi OS or Debian-based distro
User: profbill
Project path: /home/profbill/Desktop/player/audio_player.py

------------------------------------------------------------
1️⃣ Enable Automatic Login

1. Open configuration tool:
   sudo raspi-config

2. Navigate:
   System Options → Boot / Auto Login → Console Autologin
   (or “Desktop Autologin” if using the GUI)

3. Finish and reboot:
   sudo reboot

After reboot, the Pi logs directly into profbill without asking for a password.

------------------------------------------------------------
2️⃣ Create a systemd Service

1. Create a new service file:
   sudo nano /etc/systemd/system/audioplayer.service

2. Paste the following configuration:

   [Unit]
   Description=GPIO Audio Player
   After=network.target sound.target

   [Service]
   ExecStart=/usr/bin/python3 /home/profbill/Desktop/player/audio_player.py
   WorkingDirectory=/home/profbill/Desktop/player
   User=profbill
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target

3. Save and exit (Ctrl + O, Enter, Ctrl + X).

------------------------------------------------------------
3️⃣ Enable and Start the Service

sudo systemctl daemon-reload
sudo systemctl enable audioplayer.service
sudo systemctl start audioplayer.service

Check it’s active:
systemctl status audioplayer.service

Tail the live log (optional):
journalctl -u audioplayer.service -f

------------------------------------------------------------
4️⃣ Test the Setup

Reboot the Pi:
sudo reboot

After boot:
- The Pi auto-logs in as profbill.
- The audio_player.py script launches automatically.
- If the script crashes, systemd restarts it.

------------------------------------------------------------
✅ Optional Enhancements

Delay start until sound card ready:
Add ExecStartPre=/bin/sleep 5 before ExecStart

Log output to file:
ExecStart=/usr/bin/python3 /home/profbill/Desktop/player/audio_player.py >> /home/profbill/Desktop/player/log.txt 2>&1

Manually restart:
sudo systemctl restart audioplayer.service

Disable autostart:
sudo systemctl disable audioplayer.service

------------------------------------------------------------
You now have a hands-free, auto-booting Raspberry Pi audio player configured for your user and project.
