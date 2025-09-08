#!/usr/bin/env python3

import subprocess
import sys
import os
import time

# Check if virtual environment exists
venv_path = os.path.join(os.path.dirname(__file__), '.venv', 'bin', 'python')
if not os.path.exists(venv_path):
    print("Error: Virtual environment not found!")
    print("Please run the setup script first:")
    print("  ./setup.sh")
    print("Or create the virtual environment manually:")
    print("  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt")
    sys.exit(1)


if sys.executable != venv_path:
    print("Switching to virtual environment Python...")
    os.execv(venv_path, [venv_path] + sys.argv)

import pymumble_py3


# Mumble server details - replace with your own
MUMBLE_HOST = 'your.mumble.server.com'
MUMBLE_PORT = 64738
MUMBLE_USER = 'UxPlayBot'
MUMBLE_PASSWORD = ''  # if required

# Audio settings
AUDIO_CHANNELS = 2  # 2 channels for stereo, 1 for mono
MUMBLE_BANDWIDTH = 96000  # Higher bandwidth for better quality (bps)
AUDIO_FORMAT = 's16le'  # 16-bit signed little-endian for parec
AUDIO_FORMAT_ARECORD = 'S16_LE'  # Format for arecord
AUDIO_SAMPLE_RATE = 48000  # Should not be changed, Mumble expects 48000 Hz


# UxPlay options
UXPLAY_NAME = 'MumbleBot'

def start_uxplay():
    """Start UxPlay in background"""
    env = os.environ.copy()
    env['GSTREAMER_AUDIO_SINK'] = 'alsasink'
    cmd = ['uxplay', '-n', UXPLAY_NAME]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    return proc

def start_parec():
    """Start audio capture using ALSA (arecord)"""
    print(f"Starting ALSA audio capture...")
    cmd = ['arecord', '-D', 'default', '-f', AUDIO_FORMAT_ARECORD, '-r', str(AUDIO_SAMPLE_RATE), '-c', str(AUDIO_CHANNELS)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc

def main():
    # Start UxPlay
    print("Starting UxPlay...")
    uxplay_proc = start_uxplay()
    time.sleep(5)

    if uxplay_proc.poll() is not None:
        print("UxPlay failed to start or crashed.")
        return


    print("Connecting to Mumble...")
    try:
        mumble = pymumble_py3.Mumble(MUMBLE_HOST, MUMBLE_USER, port=MUMBLE_PORT, password=MUMBLE_PASSWORD, reconnect=True, stereo=True)
        mumble.start()
        mumble.is_ready()
        mumble.set_bandwidth(MUMBLE_BANDWIDTH)
        print("Connected to Mumble successfully.")
    except Exception as e:
        print(f"Failed to connect to Mumble: {e}")
        uxplay_proc.terminate()
        return

    # Start audio capture
    parec_proc = start_parec()

    if parec_proc is None:
        print("Failed to start audio capture.")
        uxplay_proc.terminate()
        mumble.stop()
        return


    time.sleep(1)
    if parec_proc.poll() is not None:
        stderr_output = parec_proc.stderr.read().decode()
        print(f"Audio capture failed to start. Error: {stderr_output}")
        uxplay_proc.terminate()
        mumble.stop()
        return

    print("Streaming audio to Mumble. Press Ctrl+C to stop.")

    try:
        while True:
            data = parec_proc.stdout.read(1024)
            if not data:
                print("No more data from audio capture, exiting.")
                break
            mumble.sound_output.add_sound(data)
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        parec_proc.terminate()
        uxplay_proc.terminate()
        mumble.stop()

if __name__ == '__main__':
    main()
