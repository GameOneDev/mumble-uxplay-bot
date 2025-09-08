# Mumble UxPlay Bot

A Python bot that streams audio from Apple devices (iPhone/iPad) to a Mumble VoIP server using UxPlay for AirPlay mirroring.

## 🚀 One-Command Installation

Get everything set up with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/GameOneDev/mumble-uxplay-bot/main/setup.sh | bash
```

This will:
- Download the repository
- Install all system dependencies
- Build and install UxPlay
- Set up the Python environment
- Configure everything automatically

> **Requirements**: git, curl, python3.8+, and sudo access are required. The script has been tested on Debian/Ubuntu-based systems.

## Prerequisites

- Linux system
- Python 3.8+
- Mumble server
- iOS device (iPhone/iPad) with AirPlay

## Installation

### 1. Install System Dependencies (Debian/Ubuntu)

```bash
# Update package list
sudo apt update

# Install UxPlay dependencies
sudo apt install -y cmake libavahi-compat-libdnssd-dev libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav \
    libplist-dev alsa-utils
```

### 2. Install and Build UxPlay

```bash
# Clone UxPlay repository
git clone https://github.com/FDH2/UxPlay.git
cd UxPlay

# Build UxPlay
mkdir build && cd build
cmake ..
make
sudo make install

# Clean up (optional)
cd ../..
rm -rf UxPlay
```

### 3. Set up Python Environment

```bash
# Clone this repository
git clone https://github.com/GameOneDev/mumble-uxplay-bot.git
cd mumble-uxplay-bot

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install pymumble_py3
```

## Configuration

Edit the constants at the top of `main.py`:

### Mumble server settings

```python
# Mumble server settings
MUMBLE_HOST = 'your.mumble.server.com'  # Your Mumble server IP/hostname
MUMBLE_PORT = 64738                    # Default Mumble port
MUMBLE_USER = 'UxPlayBot'              # Bot username
MUMBLE_PASSWORD = ''                   # Password (if required)
```

### Audio Quality Settings

You can adjust audio quality by modifying the constants:

```python
AUDIO_CHANNELS = 2  # 2 channels for stereo, 1 for mono
MUMBLE_BANDWIDTH = 96000  # Higher bandwidth for better quality (bps)
```

## Usage

### Running the Bot

1. **Run the bot:**
   ```bash
   python main.py
   ```
   (The script automatically uses the virtual environment)

2. **On your Apple device:**
   - Open Control Center
   - Tap "Screen Mirroring"
   - Select "UxPlayBot" from the list

3. **Play music on your Apple device** - it will stream to Mumble!

### Stopping the Bot

Press `Ctrl+C` in the terminal to stop the bot gracefully.

## Troubleshooting

### Audio Capture Issues
- **"arecord failed"**: Check ALSA devices with `arecord -l`
- **No audio devices**: Ensure ALSA is properly configured
- **Permission denied**: Run with proper audio permissions or as audio group member

### Mumble Connection Issues
- **Connection refused**: Check server IP, port, and firewall settings
- **Authentication failed**: Verify username/password

### UxPlay Issues
- **Build fails**: Ensure all dependencies are installed
- **No AirPlay device**: Check that UxPlay is running and accessible on the same network as your Apple device

### ModuleNotFoundError
If you get `ModuleNotFoundError: No module named 'pymumble_py3'`, the virtual environment is not being used correctly. The script should automatically detect and use the virtual environment. If it doesn't work:

1. Activate the virtual environment manually:
   ```bash
   source .venv/bin/activate
   ```
2. Run the bot:
   ```bash
   python main.py
   ```

## Acknowledgments

- [UxPlay](https://github.com/FDH2/UxPlay) - AirPlay mirroring server
- [pymumble](https://github.com/azlux/pymumble) - Python Mumble library
- [Mumble](https://www.mumble.info/) - VoIP communication platform
