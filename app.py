import os
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import ffmpeg
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the downloads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),
        'extract_flat': False,
        'force_generic_extractor': True,
        'no_check_certificates': True,
        'ignoreerrors': True,
        'quiet': True,
        'nocheckcertificate': True,
        'legacyserverconnect': True,
        'prefer_insecure': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'file_access_retries': 10,
        'extractor_retries': 10,
        'retry_sleep': 5,
        'retry_sleep_functions': {'fragment': lambda n: 5 * (n + 1)},
        'sleep_interval': 5,
        'max_sleep_interval': 30,
        'sleep_interval_requests': 3,
        'throttledratelimit': 100000,
        'ratelimit': 100000,
        'no_warnings': False,
        'verbose': True,
        'update': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return {
                'title': info['title'],
                'filename': f"{info['title']}.mp3",
                'filepath': os.path.join(app.config['UPLOAD_FOLDER'], f"{info['title']}.mp3")
            }
        except Exception as e:
            return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result = download_youtube_audio(url)
    if 'error' in result:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'filename': result['filename'],
        'title': result['title']
    })

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False) 