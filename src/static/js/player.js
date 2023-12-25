document.addEventListener('DOMContentLoaded', function () {
    var randomSong = document.getElementById('randomSong');
  
    randomSong.addEventListener('click', function () {
        randomSong.classList.toggle('clicked');
    });

    var replayCounter = 0;
    var replaySong = document.getElementById('replaySong');
    replaySong.addEventListener('click', function () {
            if(replayCounter == 0){
                replaySong.classList.toggle('clicked');
                replayCounter = 1;
            }
            else if(replayCounter == 1){
                replaySong.classList.remove('clicked');
                replaySong.classList.toggle('double-clicked');
                replayCounter = 2;
            }
            else if(replayCounter == 2){
                replaySong.classList.remove('double-clicked');
                replayCounter = 0;
            }
        });
});


