const audio = new Audio('');
let masterPlay = document.getElementById('masterPlay');
let currentSong = null;

function playSong(song_author, song_name, song_filename, username, playlist_id) {
    if (currentSong !== song_filename) {
        // Остановить текущую аудиозапись (если есть)
        if (currentSong !== null) {
            audio.pause();
            audio.currentTime = 0; // Сбросить текущее время до начала
        }

        // Устанавливаем новый источник аудио для объекта Audio
        audio.src = `/static/songs/playlists/${username}/${playlist_id}/${song_filename}`;
        currentSong = song_filename;

        // Обновить элемент управления воспроизведением
        masterPlay.setAttribute('icon', 'line-md:pause');
        masterPlay.style.marginRight = '10px';
        masterPlay.style.width = '50px';
    }

    if (audio.paused) {
        // Воспроизведение аудио
        audio.play()
            .then(() => {
                var song = document.getElementById('song-name');
                song.innerText = song_name;
                var author = document.getElementById('song-author');
                author.innerText = song_author;
            })
            .catch((error) => {
                // Обработка ошибки воспроизведения
                console.error('Error during playback:', error);
            });
    } else {
        // Пауза аудио
        audio.pause();

        // Обновление элемента управления воспроизведением
        masterPlay.setAttribute('icon', 'line-md:play-filled');
        masterPlay.style.width = '50px';
    }
}
