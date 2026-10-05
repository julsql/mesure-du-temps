// Navigation clavier dans la visionneuse de l'album : ← / → changent de photo, Échap ferme.
// La visionneuse elle-même reste en CSS pur (:target) ; ce script ne fait que suivre ses liens.
const KEYS = {
  ArrowLeft: ".lightbox__nav--prev",
  ArrowRight: ".lightbox__nav--next",
  Escape: ".lightbox__close",
};

document.addEventListener("keydown", (event) => {
  const lightbox = document.querySelector(".lightbox:target");
  const selector = KEYS[event.key];
  if (!lightbox || !selector) return;

  event.preventDefault();
  location.replace(lightbox.querySelector(selector).getAttribute("href"));
});
