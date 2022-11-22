'use strict'

function ShowItems(box) {
    var items = box.getElementsByClassName('items')[0];
    
    if (items.classList.contains('show-items')) {
        items.classList.remove('show-items');
    } else {
        items.setAttribute('class', 'items show-items');
    }

}


document.getElementById("id_username").placeholder = "Usuario";
document.getElementById("id_password1").placeholder = "Contraseña";
document.getElementById("id_password2").placeholder = "Confirmar contraseña";