# YouTube to MP3 Converter

A simple web application that converts YouTube videos to MP3 format.

## Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system

### Installing FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
Download FFmpeg from the official website: https://ffmpeg.org/download.html

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd ytmp3
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Paste a YouTube URL into the input field
2. Click "Convert to MP3"
3. Wait for the conversion to complete
4. Click the "Download MP3" button to download the converted file

## Features

- Simple and modern user interface
- Real-time conversion status updates
- Error handling and user feedback
- Automatic file naming based on video title
- High-quality MP3 conversion (192kbps)

## Note

This application is for personal use only. Please respect YouTube's terms of service and copyright laws when using this tool. 