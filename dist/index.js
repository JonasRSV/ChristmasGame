

setupEventListeners = () => {
  var interfaceFrame = document.getElementById("interface-frame")
  var gameFrame = document.getElementById("game-frame")

  interfaceFrame.addEventListener("click", () => {
    window.location.href = "http://" + window.location.hostname + "/interface.html";
  }, false);

  gameFrame.addEventListener("click", () => {
    window.location.href = "http://" + window.location.hostname + "/xmas.html";
  }, false);
}

window.onload = setupEventListeners
