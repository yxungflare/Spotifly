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
        console.log(currentDescription);
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