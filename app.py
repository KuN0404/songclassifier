from flask import Flask, render_template, request, jsonify
import re
import joblib
from datetime import datetime

app = Flask(__name__)

# Path ke model yang disimpan
MODEL_PATH = "svm_genre_model.joblib"

# Memuat model
model = joblib.load(MODEL_PATH)

# Fungsi untuk membersihkan input lirik
def clean_lyrics(lyrics):
    lyrics = lyrics.lower()  # Ubah semua huruf menjadi kecil
    lyrics = re.sub(r'[^A-Za-z\s]', '', lyrics)  # Hilangkan karakter khusus
    lyrics = lyrics.replace('\n', ' ')  # Hilangkan newline
    lyrics = lyrics.replace('\\', '')  # Menghilangkan karakter backslash
    return lyrics

@app.route('/')
def index():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    genre = None
    lyrics = None
    cleaned_lyrics = None

    if request.method == 'POST':
        # Mengambil input lirik dari form
        lyrics = request.form['lyrics']
        cleaned_lyrics = clean_lyrics(lyrics)  # Filterisasi lirik
        prediction = model.predict([cleaned_lyrics])  # Prediksi genre
        genre = prediction[0]  # Ambil hasil prediksi pertama

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'genre': genre, 'lyrics': lyrics, 'clean_lyrics': cleaned_lyrics})

    return render_template('prediction.html', genre=genre, lyrics=lyrics, clean_lyrics=cleaned_lyrics)

if __name__ == '__main__':
    app.run(debug=True)
