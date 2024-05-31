from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import yt_dlp as youtube_dl
import os
import re

app = Flask(__name__, static_folder='static')

VIDEO_DIR = 'download'

def download_video(url, dir_path=VIDEO_DIR):
    try:
        # Try to download in 1080p format first
        youtube_dl_options = {
            'restrictfilenames': True,
            'outtmpl': f'{dir_path}/%(title)s.%(ext)s',
            'format': '(bestvideo[height<=1080]+bestaudio/best[height<=1080])/best',
            'merge_output_format': 'mp4',
        }
        with youtube_dl.YoutubeDL(youtube_dl_options) as you_dl:
            you_dl.download([url])
    except youtube_dl.utils.DownloadError as e:
        print(f"1080p format not available for {url}. Falling back to best available format.")
        # Fall back to the best available format
        youtube_dl_options = {
            'restrictfilenames': True,
            'outtmpl': f'{dir_path}/%(title)s.%(ext)s',
            'format': 'best',
        }
        with youtube_dl.YoutubeDL(youtube_dl_options) as you_dl:
            you_dl.download([url])


def get_files_in_directory(dir, file_ext=None):
    if file_ext:
        return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(file_ext)]
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['text']
        try:
            download_video(video_url, VIDEO_DIR)
            return render_template('success.html')
        except Exception as e:
            error_msg = str(e)
            print(error_msg)
            return render_template('failure.html', error_msg = error_msg)
    else:
        video_list = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
        return render_template('index.html', video_list=video_list, VIDEO_DIR=VIDEO_DIR)


@app.route('/'+ VIDEO_DIR + '/<path:filename>')
def video(filename):
    return send_from_directory(os.path.join(os.getcwd(), VIDEO_DIR), filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{filename}' deleted successfully.")
    return redirect(url_for('index'))


@app.route('/rename', methods=['POST'])
def rename_file():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    old_file_path = os.path.join(VIDEO_DIR, old_name)
    new_file_path = os.path.join(VIDEO_DIR, new_name + '.mp4')

    if os.path.exists(old_file_path):
        if os.path.exists(new_file_path):
            print(f"File '{new_name}' already exists.")
        elif not re.match(r'^[A-Za-z0-9]', new_name):  # Check if the new name starts with a letter or digit
            print(f"File name '{new_name}' does not start with a letter or digit.")
        elif len(new_name)<1:  #Not really needed since the field cannot be empty.
            print(f"File name is too short")
        else:
            os.rename(old_file_path, new_file_path)
            print(f"File '{old_name}' renamed to '{new_name}.mp4' successfully.")
    else:
        print(f"File '{old_name}' not found.")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

