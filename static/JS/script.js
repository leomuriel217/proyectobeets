// Función para abrir el popup
function abrirpopup() {
    document.getElementById("popup").style.display = "flex";
}

// Función para cerrar el popup
function closePopup() {
    document.getElementById("popup").style.display = "none";
}

//funcion para validar que los input del formulario tengan información

document.querySelector(".formulario").addEventListener("submit", function (e) {
    // Selecciona el formulario usando su clase "formulario"
    // Añade un evento que se dispara cuando se intenta enviar el formulario
    e.preventDefault(); 
    // Evita el comportamiento por defecto del formulario (recargar la página al enviar)

    const nombre = document.getElementById("nombre").value;
    // Obtiene el valor del campo de entrada con el id "nombre"

    if (nombre.trim() === "") {
        // Verifica si el campo está vacío (después de eliminar espacios en blanco)
        alert("Por favor, completa tu nombre antes de enviar el formulario.");
        // Muestra un mensaje de alerta si el campo está vacío
    } else {
        alert(`¡Bienvenido, ${nombre}! Gracias por contactarnos. Nos pondremos en contacto contigo lo más pronto posible.`);
        // Muestra un mensaje personalizado si el campo tiene contenido
    }

});
