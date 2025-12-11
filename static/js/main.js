function inicializarCarruselEmociones() {
  const carrusel = document.getElementById("carruselEmociones");
  const inputEmocion = document.getElementById("emocionSeleccionada");
  const flechaIzq = document.getElementById("flechaIzquierda");
  const flechaDer = document.getElementById("flechaDerecha");
  const tarjetas = document.querySelectorAll(".tarjeta-emocion");

  let indiceActual = 0;

  function actualizarActiva(indice) {
    tarjetas.forEach((tarjeta) => tarjeta.classList.remove("activa"));

    tarjetas[indice].classList.add("activa");

    const emocion = tarjetas[indice].getAttribute("data-emocion");
    inputEmocion.value = emocion;

    tarjetas[indice].scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });

    indiceActual = indice;
  }

  flechaIzq.addEventListener("click", function () {
    let nuevoIndice = indiceActual - 1;

    if (nuevoIndice < 0) {
      nuevoIndice = tarjetas.length - 1;
    }

    actualizarActiva(nuevoIndice);
  });

  flechaDer.addEventListener("click", function () {
    let nuevoIndice = indiceActual + 1;

    if (nuevoIndice >= tarjetas.length) {
      nuevoIndice = 0;
    }

    actualizarActiva(nuevoIndice);
  });

  tarjetas.forEach((tarjeta, indice) => {
    tarjeta.addEventListener("click", function () {
      actualizarActiva(indice);
    });
  });

  actualizarActiva(14);
}
