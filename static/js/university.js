let count = 0;

function increaseCounter() {
  const counter = document.getElementById("counter");
  count++;
  counter.innerText = count;
  counter.classList.add("animate");
  setTimeout(() => {
    counter.classList.remove("animate");
  }, 500);
}

document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    fetch('/post/comment', {method: 'POST', body: formData}).then((response) => {
      location.reload()
    })
  });
})

ChangeInfoText = () => {
  const infoText = document.getElementById("info-text");
  infoText.style.display = "none";
  const infoInput = document.getElementById("infoInput");
  infoInput.style.display = "block";
}