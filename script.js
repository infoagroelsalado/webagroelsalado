document.getElementById("whatsapp-form")?.addEventListener("submit", function (e) {
    e.preventDefault();

    // Obtener los valores del formulario
    const nombre = document.querySelector('input[name="nombre"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const telefono = document.querySelector('input[name="telefono"]').value;

    const selectMotivo = document.querySelector('select[name="motivo"]');
    const motivo = selectMotivo.options[selectMotivo.selectedIndex].text;

    const mensaje = document.querySelector('textarea[name="mensaje"]').value;

    // AQUÍ DEBES PONER TU NÚMERO DE WHATSAPP (Ej: 5491100000000)
    // 54 = Argentina, 9 = celular, 11 = código de área, etc. No uses el símbolo +
    const numeroWhatsApp = "5492345448922";

    // Construir el texto del mensaje
    let texto = `Hola, me contacto desde la web de Agroelsalado.\n\n`;
    texto += `*Nombre:* ${nombre}\n`;
    texto += `*Email:* ${email}\n`;
    if (telefono) texto += `*Teléfono:* ${telefono}\n`;
    texto += `*Motivo:* ${motivo}\n\n`;
    if (mensaje) texto += `*Mensaje:* ${mensaje}`;

    // Codificar para URL
    const textoCodificado = encodeURIComponent(texto);

    // Crear el enlace a la API de WhatsApp y abrirlo en una nueva pestaña
    const url = `https://wa.me/${numeroWhatsApp}?text=${textoCodificado}`;
    window.open(url, '_blank');
});
