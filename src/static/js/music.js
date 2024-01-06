let audio = new Audio('');
let masterPlay = document.getElementById('masterPlay');
let currentSong = null;
let currentSongName = null;
let currentSongAuthor = null;
let songsArray = [];
let user = null;
let playlistID = null;

// получаем список файловых имен песен в плейлисте
function FileNamesongsListInPlaylist(){
    let ids = []
    let songs = document.querySelectorAll('.song-name-line');
    for(var i = 0; i < songs.length ;i++){
        ids.push(songs[i].id);
    }
    return ids 
}


// получаем список названий песен в плейлисте
function NamesongsListInPlaylist(){
    let names = []
    let songs = document.querySelectorAll('.song-name-line');
    for(var i = 0; i < songs.length ;i++){
        names.push(songs[i].innerText);
    }
    return names 
}


// получаем список авторов песен в плейлисте
function AuthorsongsListInPlaylist(){
    let authors = []
    let songs = document.querySelectorAll('.author');
    for(var i = 0; i < songs.length ;i++){
        authors.push(songs[i].innerText);
    }
    return authors 
}


// следующая песня
function nextSong(){
    var songsFileNameList = FileNamesongsListInPlaylist();
    var songsName = NamesongsListInPlaylist();
    var songsAuthors = AuthorsongsListInPlaylist();

    for(var i = 0; i < songsFileNameList.length; i++){
        if(songsFileNameList[i] == currentSong){
            var nSongFileName = songsFileNameList[i + 1]; 
        }

        if(songsName[i] == currentSongName){
            var nSongName = songsName[i + 1]; 
        }

        if(songsAuthors[i] == currentSongAuthor){
            var nSongAuthor = songsAuthors[i + 1]; 
        }
    }
    // после всех вычислений информации о следующей песне вызываем функцию проигрывания
    playSong(nSongAuthor, nSongName, nSongFileName, user, playlistID);
}


// предыдущая песня
function previousSong(){
    var songsFileNameList = FileNamesongsListInPlaylist();
    var songsName = NamesongsListInPlaylist();
    var songsAuthors = AuthorsongsListInPlaylist();

    for(var i = 0; i < songsFileNameList.length; i++){
        if(songsFileNameList[i] == currentSong){
            var pSongFileName = songsFileNameList[i - 1]; 
        }

        if(songsName[i] == currentSongName){
            var pSongName = songsName[i - 1]; 
        }

        if(songsAuthors[i] == currentSongAuthor){
            var pSongAuthor = songsAuthors[i - 1]; 
        }
    }
    // после всех вычислений информации о предыдущей песне вызываем функцию проигрывания
    playSong(pSongAuthor, pSongName, pSongFileName, user, playlistID);
}


// случайное проигрывание
function randomSong(){
    var songsFileNameList = FileNamesongsListInPlaylist();
    var songsName = NamesongsListInPlaylist();
    var songsAuthors = AuthorsongsListInPlaylist();
    var randomIndex = Math.floor(Math.random() * songsFileNameList.length);

    for(var i = 0; i < songsFileNameList.length; i++){
        
        if(songsFileNameList[i] == currentSong){
            var rSongFileName = songsFileNameList[randomIndex]; 
        }

        if(songsName[i] == currentSongName){
            var rSongName = songsName[randomIndex]; 
        }

        if(songsAuthors[i] == currentSongAuthor){
            var rSongAuthor = songsAuthors[randomIndex]; 
        }
    }
    // после всех вычислений информации о предыдущей песне вызываем функцию проигрывания
    playSong(rSongAuthor, rSongName, rSongFileName, user, playlistID);
}


// Функция для обновления визуализации времени воспроизведения
function updateProgressBar(songDurationInput) {
    const bar2 = document.getElementById('bar2');
    const dot = document.querySelector('.bar2 .dot');
    const currentStart = document.getElementById('currentStart');
    const currentEnd = document.getElementById('currentEnd');
  
    const currentTime = audio.currentTime;
    const duration = audio.duration;
    const progress = (currentTime / duration) * 100;
  
    songDurationInput.value = progress;


    bar2.style.width = `${progress}%`;
    dot.style.left = `${progress}%`;
  
    const minutesStart = Math.floor(currentTime / 60);
    const secondsStart = Math.floor(currentTime % 60);
    const minutesEnd = Math.floor(duration / 60);
    const secondsEnd = Math.floor(duration % 60);
  
    currentStart.textContent = `${minutesStart}:${secondsStart < 10 ? '0' : ''}${secondsStart}`;
    currentEnd.textContent = `${minutesEnd}:${secondsEnd < 10 ? '0' : ''}${secondsEnd}`;
  }



async function seekToPosition() {
    let progress = document.getElementById('songDuration').value;
    let curTime = (progress / 100) * audio.duration;
    
    audio.currentTime = curTime;

}



// Новая функция для воспроизведения песни
function playSong(song_author, song_name, song_filename, username, playlist_id) {
    user = username;
    playlistID = playlist_id;
    currentSongName = song_name;
    currentSongAuthor = song_author;

    // Если текущая песня не совпадает с новой, обновляем аудио
    if (currentSong !== song_filename) {
        // Приостанавливаем воспроизведение
        audio.pause();

        // Сбрасываем текущее время
        audio.currentTime = 0;

        // Обновляем источник аудио
        audio.src = `/static/songs/playlists/${username}/${playlist_id}/${song_filename}`;
        currentSong = song_filename;

        // Добавляем обработчик события timeupdate для отслеживания прогресса
        audio.addEventListener('timeupdate', function() {
            // Обновляем визуализацию времени воспроизведения
            updateProgressBar(document.getElementById('songDuration'));
        });
    }

    // Если аудио приостановлено или закончилось, воспроизводим заново
    if (audio.paused || audio.ended) {
        audio.play()    
            .then(() => {
                // Обновляем информацию о песне
                var song = document.getElementById('song-name');
                song.innerText = song_name;
                var author = document.getElementById('song-author');
                author.innerText = song_author;

                masterPlay.setAttribute('icon', 'line-md:pause');
                masterPlay.style.marginRight = '10px';
                masterPlay.style.width = '50px';

                masterPlay.setAttribute('onclick', `playSong('${song_author}', '${song_name}', '${song_filename}', '${username}', '${playlist_id}');`);
            })
            .catch((error) => {
                console.error('Error during playback:', error);
            });
    } else {
        // Если аудио проигрывается, приостанавливаем
        audio.pause();

        masterPlay.setAttribute('icon', 'line-md:play-filled');
        masterPlay.style.width = '50px';

        masterPlay.setAttribute('onclick', `playSong('${song_author}', '${song_name}', '${song_filename}', '${username}', '${playlist_id}');`);
    }
}

// if (audio.play()) {
//     audio.addEventListener('ended', nextSong);
// }