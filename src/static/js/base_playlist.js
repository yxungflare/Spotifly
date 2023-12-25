function editButtonWithtextarea() {
    // Get the button element
    var addButton = document.getElementById('edit-description');
    // Create an textarea element
    var textarea = document.createElement('textarea');
    var currentDescription = document.getElementById('playlist_description').textContent;
    textarea.value = currentDescription;
    document.getElementById('playlist_description').remove();
    textarea.style.marginRight = '10px';
    textarea.style.resize ='both';
    textarea.cols = '30';
    textarea.rows = '2';
    textarea.name = 'description';


    // Create an OK button element
    var okButton = document.createElement('button');
    okButton.innerHTML = 'OK';
    okButton.type = 'submit';
    // Add an event listener to the OK button if needed
    okButton.addEventListener('click', function() {
        // Code to handle the OK button click event
    });

    // Replace the "Добавить описание" button with the textarea and the OK button
    addButton.parentNode.replaceChild(textarea, addButton);
    textarea.parentNode.insertBefore(okButton, textarea.nextSibling);
};


if(document.getElementById('edit-description')){
// You would also need to set up an event listener for the original button
    document.getElementById('edit-description').addEventListener('click', editButtonWithtextarea);
}


// Добавляем описание
function addDescription() {
    var addButton = document.getElementById('add-description-button');
    if(addButton){
        var currentDescription = addButton.textContent;
        var textarea = document.createElement('textarea');
        textarea.value = currentDescription;
        textarea.style.marginRight = '10px';
        textarea.style.resize ='both';
        textarea.cols = '30';
        textarea.rows = '2';
        textarea.name = 'description';


    // Create an OK button element
        var okButton = document.createElement('button');
        okButton.innerHTML = 'OK';
        okButton.type = 'submit';
    // // Add an event listener to the OK button if needed
        okButton.addEventListener('click', function() {
        //     // Code to handle the OK button click event
        });

    // // Replace the "Добавить описание" button with the textarea and the OK button
        addButton.parentNode.replaceChild(textarea, addButton);
        textarea.parentNode.insertBefore(okButton, textarea.nextSibling);
    }
}


if(document.getElementById('add-description-button')){
    document.getElementById('add-description-button').addEventListener('click', addDescription);
}


function editButtonWithName() {
    // Get the button element
    var addButton = document.getElementById('edit-name');
    // Create an input element
    var input = document.createElement('input');
    var currentName = document.getElementById('playlist_name').textContent;
    input.value = currentName;
    document.getElementById('playlist_name').remove();
    input.style.marginRight = '10px';
    input.style.resize ='both';
    input.cols = '30';
    input.rows = '2';
    input.name = 'name';


    // Create an OK button element
    var okButton = document.createElement('button');
    okButton.innerHTML = 'OK';
    okButton.type = 'submit';
    // Add an event listener to the OK button if needed
    okButton.addEventListener('click', function() {
        // Code to handle the OK button click event
    });

    // Replace the "Добавить описание" button with the input and the OK button
    addButton.parentNode.replaceChild(input, addButton);
    input.parentNode.insertBefore(okButton, input.nextSibling);
};


if(document.getElementById('edit-name')){
    document.getElementById('edit-name').addEventListener('click', editButtonWithName);
}


function editViewPlaylistCover(){

    icon_button = document.getElementById('edit-cover')
    icon_button.style.display = 'none';

    cover = document.getElementById('playlist_cover')
    cover.addEventListener('mouseover', function() {
        icon_button.style.display = 'block';
    });
    cover.addEventListener('mouseout', function() {
        icon_button.addEventListener('mouseover', function(){
            icon_button.style.display = 'block';
        })
        icon_button.addEventListener('mouseout', function(){
            icon_button.style.display = 'none';
        })
        icon_button.style.display = 'none';
    });


    icon_button_name = document.getElementById('edit-name')
    icon_button_name.style.display = 'none';

    playlist_name = document.getElementById('currentName')
    playlist_name.addEventListener('mouseover', function() {
        icon_button_name.style.display = 'block';
    });
    playlist_name.addEventListener('mouseout', function() {
        icon_button_name.addEventListener('mouseover', function(){
            icon_button_name.style.display = 'block';
        })
        icon_button_name.addEventListener('mouseout', function(){
            icon_button_name.style.display = 'none';
        })
        icon_button_name.style.display = 'none';
    });


    if(document.getElementById('edit-description')){
        icon_button_description = document.getElementById('edit-description')
        icon_button_description.style.display = 'none';

        playlist_description = document.getElementById('currentDescription')
        playlist_description.addEventListener('mouseover', function() {
            icon_button_description.style.display = 'block';
        });
        playlist_description.addEventListener('mouseout', function() {
            icon_button_description.addEventListener('mouseover', function(){
                icon_button_description.style.display = 'block';
            })
            icon_button_description.addEventListener('mouseout', function(){
                icon_button_description.style.display = 'none';
            })
            icon_button_description.style.display = 'none';
        });
    }
}


window.onload = editViewPlaylistCover


function updateFormAction(formId, newAction) {
    document.getElementById(formId).action = newAction;
}


function handleFileInput() {
    const fileInput = document.getElementById('file-input');
    const formId = fileInput.getAttribute('data-form-id');

    // Обновляем action формы, используя путь для загрузки обложки
    updateFormAction(formId, `/collections/{{ username }}/playlist/{{ playlist.id }}/edit_playlist_cover`);

    // Отправляем форму сразу после выбора файла
    document.getElementById(formId).submit();
}


function copyCurrentURL(){
    // Получаем текущий URL-адрес
    var currentURL = window.location.href;

    // Создаем временный элемент textarea для копирования текста
    var tempTextArea = document.createElement('textarea');
    tempTextArea.value = currentURL;

    // Делаем его невидимым
    tempTextArea.style.position = 'absolute';
    tempTextArea.style.left = '-9999px';

    // Добавляем его на страницу
    document.body.appendChild(tempTextArea);

    // Выделяем текст в textarea
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, currentURL.length);

    // Копируем выделенный текст в буфер обмена
    document.execCommand('copy');

    // Удаляем временный элемент textarea
    document.body.removeChild(tempTextArea);
}

function cursorSong(song_id, playlists, username, song_id_just_digits, playlist_id_array){
    // Добавим мусорку

    const svgCode = `
      <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        viewBox="0 0 791.908 791.908" style="enable-background:new 0 0 791.908 791.908;" xml:space="preserve" width="25" height="25">
        <g>
          <path d="M648.587,99.881H509.156C500.276,43.486,452.761,0,394.444,0S287.696,43.486,279.731,99.881H142.315
            c-26.733,0-48.43,21.789-48.43,48.43v49.437c0,24.719,17.761,44.493,41.564,47.423V727.64c0,35.613,28.655,64.268,64.268,64.268
            h392.475c35.613,0,64.268-28.655,64.268-64.268V246.087c23.711-3.937,41.564-23.711,41.564-47.423v-49.437
            C697.017,121.67,675.228,99.881,648.587,99.881z M394.444,36.62c38.543,0,70.219,26.733,77.085,63.261H316.351
            C324.225,64.268,355.901,36.62,394.444,36.62z M618.924,728.739c0,14.831-11.901,27.648-27.648,27.648H198.71
            c-14.831,0-27.648-11.901-27.648-27.648V247.185h446.948v481.554H618.924z M660.397,197.748c0,6.958-4.944,11.902-11.902,11.902
            H142.223c-6.958,0-11.902-4.944-11.902-11.902v-49.437c0-6.958,4.944-11.902,11.902-11.902h505.265
            c6.958,0,11.901,4.944,11.901,11.902v49.437H660.397z M253.09,661.45V349.081c0-9.887,7.873-17.761,17.761-17.761
            s17.761,7.873,17.761,17.761V661.45c0,9.887-7.873,17.761-17.761,17.761C260.964,680.309,253.09,671.337,253.09,661.45z
             M378.606,661.45V349.081c0-9.887,7.873-17.761,17.761-17.761c9.887,0,17.761,7.873,17.761,17.761V661.45
            c0,9.887-7.873,17.761-17.761,17.761C386.57,680.309,378.606,671.337,378.606,661.45z M504.212,661.45V349.081
            c0-9.887,7.873-17.761,17.761-17.761s17.761,7.873,17.761,17.761V661.45c0,9.887-7.873,17.761-17.761,17.761
            C513.093,680.309,504.212,671.337,504.212,661.45z"/>
        </g>
      </svg>
    `;

    // Создаем новый элемент SVG
    const svgElement = new DOMParser().parseFromString(svgCode, 'image/svg+xml').documentElement;

    // Получаем контейнер по идентификатору
    const container_for_util_basket = document.getElementById(song_id);
    // Очищаем контейнер
    container_for_util_basket.innerHTML = '';

    // Добавляем SVG в контейнер
    container_for_util_basket.appendChild(svgElement);


    // Теперь убирем время проигрывания и вставим дополнительные кнопки
    songDuration = document.getElementById('song_duration_' + song_id);
    songDuration.style.display = 'none';

    const buttonsWithPlaylists = () => {
        let buttonsGroupCode = '';
    
        // Вне цикла создаем начало и конец группы кнопок
        buttonsGroupCode += `
            <div class="btn-group" role="group">
                <button type="button" class="btn dropdown-toggle btn-md" data-bs-toggle="dropdown" style="background-color: rgba(172, 255, 47, 0.397);" aria-expanded="false">
                    ...
                </button>
                <ul class="dropdown-menu">
                    <li><button type="button" onclick="copyCurrentSong()" class="dropdown-item text-end" id="liveToastBtn">Поделиться</button></li>
                    <li><button type="button" data-bs-toggle="modal" data-bs-target="#addToPlaylistModal" onclick="addToPlaylist()" class="dropdown-item text-end" id="liveToastBtn"><b>+</b> Добавить в плейлист </button></li>
                </ul>
        
                <!-- Модальное окно -->
                <div class="modal fade" id="addToPlaylistModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Добавить в плейлист</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                            </div>
                            <div class="modal-body">
                                <ul class="list-group">`;
         
        for (const key in playlists) {
            buttonsGroupCode += `
                <li class="list-group-item">
                    <input class="form-check-input me-1" type="checkbox" value="${key}" id="${key}CheckboxStretched" name="${key}">
                    <label class="form-check-label stretched-link" for="${key}CheckboxStretched">${playlists[key]}</label>
                </li>`;
        }
        

        // Завершаем группу кнопок
        buttonsGroupCode += `
                                </ul>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                                <button type="button" onclick="addSongToAnotherPlaylist('${username}', ${song_id_just_digits}, ${JSON.stringify(playlist_id_array)});" class="btn btn-primary">ОК</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
    
        return buttonsGroupCode;
    };
    
    const buttonsGroupHTML = buttonsWithPlaylists(); // Генерируем HTML код
    
    // Получаем контейнер по идентификатору
    const containerForGroupButton = document.getElementById('container_for_group_button_' + song_id);
    containerForGroupButton.style.display = 'block';
    
    // Очищаем контейнер
    containerForGroupButton.innerHTML = '';
    
    // Добавляем созданный HTML в контейнер
    containerForGroupButton.insertAdjacentHTML('beforeend', buttonsGroupHTML);
    
}

function deleteCursorSong(song_id){
    const container_for_util_basket = document.getElementById(song_id);
    container_for_util_basket.innerHTML = '';

    const container_for_group_button = document.getElementById('container_for_group_button_' + song_id);
    container_for_group_button.innerHTML = '';
    container_for_group_button.style.display ='none';

    songDuration = document.getElementById('song_duration_' + song_id);
    songDuration.style.display ='block';
}


function delete_playlist(username, playlist_id){
    fetch('/collections/' + username + '/playlist/' + playlist_id + '/delete', { method: 'DELETE' })
    return false;
}


function updateFormAction(formId, newAction) {
    document.getElementById(formId).action = newAction;
    }

function handleFileInput(username, playlist_id) {
    const fileInput = document.getElementById('file-input');
    const formId = fileInput.getAttribute('data-form-id');
    // Обновляем action формы, используя путь для загрузки обложки
    updateFormAction(formId, `/collections/` + username + `/playlist/` + playlist_id + `/edit_playlist_cover`);
    // Отправляем форму сразу после выбора файла
    document.getElementById(formId).submit();
}

function addSong(username, playlist_id) {
    const fileInput = document.getElementById('file-song');
    const formId = fileInput.getAttribute('data-form-id');

    // Обновляем action формы, используя путь для загрузки обложки
    updateFormAction(formId, `/collections/` + username + `/playlist/` + playlist_id + `/add_song`);

    // Отправляем форму сразу после выбора файла
    document.getElementById(formId).submit();
}


function make_favorite_playlist(username, playlist_id){
    fetch('/collections/' + username + '/playlist/' + playlist_id + '/make_favorite', { method: 'POST' })
}

function make_not_favorite_playlist(username, playlist_id){
    fetch('/collections/' + username + '/playlist/' + playlist_id + '/make_not_favorite', { method: 'POST' })
}

function delete_song(song_id, username, playlist_id){
    fetch('/collections/' + username + '/playlist/' + playlist_id + '/delete_song/'+song_id, { method: 'DELETE' })
    location.reload();
}

function addSongToAnotherPlaylist(username, song_id, playlist_id_array){
    active_checkbox_playlists = []
    for(p=0; p < playlist_id_array.length; p++){
        checkbox = document.getElementById(playlist_id_array[p] +'CheckboxStretched')
        if(checkbox.checked){
            active_checkbox_playlists[p] = checkbox;
            fetch('/collections/' + username + '/playlist/' + checkbox.value + '/add_song/' + song_id, { method: 'POST' });
            location.reload();     
        }
    }
}


function make_favorite_song(username, song_id){
    fetch('/collections/' + username + '/make_favorite_song/' + song_id, { method: 'POST' })
}

function make_not_favorite_song(username, song_id){
    fetch('/collections/' + username + '/make_not_favorite_song/' + song_id, { method: 'POST' })
}

// .playlist-list
// submit_find_song


document.querySelector('#submit_find_song').oninput = function(){
    
    var emptyFound = document.getElementById('emptyFound');

    // если не существует
    if(emptyFound){
        emptyFound.remove();
    }
    emptyFound = document.createElement('div');
    emptyFound.innerText = 'Не найдено';
    emptyFound.id = 'emptyFound';
    emptyFound.style.display = 'none';
    document.body.appendChild(emptyFound);

    let val = this.value.toLowerCase();
    let songBlock = document.querySelectorAll('.song-list')

    let songCounter = 0

    var regex = new RegExp(val);
    for(let song of songBlock){
        let songValue = song.querySelector('.song-name').innerText.toLowerCase();
        if(val != ''){
            if(!regex.test(songValue)){
                song.style.display = 'none';
                songCounter += 1
            }
        }

        else{
            song.style.display = 'flex';
        }
    }

    console.log(songCounter, songBlock.length)
    if(songCounter == songBlock.length){
        emptyFound.style.textAlign  = 'center';
        emptyFound.style.display = 'block';
    }
};