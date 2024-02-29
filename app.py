from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube
import os
import threading

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        resolution = request.form['resolution']
        try:
            yt = YouTube(url)
            
            if resolution == 'audio':
                audio_stream = yt.streams.filter(only_audio=True).first()
                threading.Thread(target=download_audio, args=(audio_stream,)).start()
            else:
                video_stream = yt.streams.get_highest_resolution()
                threading.Thread(target=download_video, args=(video_stream,)).start()
                
            flash('Download started!', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('download'))
    return render_template('download.html')

def download_video(stream):
    try:
        stream.download(output_path=DOWNLOAD_FOLDER)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

def download_audio(stream):
    try:
        stream.download(output_path=DOWNLOAD_FOLDER)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

if __name__ == '__main__':
    app.run(debug=True)
