import os
from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube
import ffmpeg
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the downloads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def download_youtube_audio(url):
    try:
        yt = YouTube(url)
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            return {'error': 'No audio stream found'}
        
        # Download the audio
        output_path = audio_stream.download(output_path=app.config['UPLOAD_FOLDER'])
        
        # Convert to MP3
        mp3_path = os.path.splitext(output_path)[0] + '.mp3'
        stream = ffmpeg.input(output_path)
        stream = ffmpeg.output(stream, mp3_path, acodec='libmp3lame', audio_bitrate='192k')
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        
        # Clean up the original file
        os.remove(output_path)
        
        return {
            'title': yt.title,
            'filename': os.path.basename(mp3_path),
            'filepath': mp3_path
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