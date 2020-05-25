function previewFile() {
    const preview = document.querySelector('img');
    const file = document.querySelector('input[type=file]').files[0];
    const label = document.querySelector('.validate')
    const reader = new FileReader();

    reader.onloadend = function() {
        preview.src = reader.result;
    }

    if(file) {
        label.value = file.name.substr(0,35);
        reader.readAsDataURL(file);
    } else {
        preview.src = "";
    }
}
