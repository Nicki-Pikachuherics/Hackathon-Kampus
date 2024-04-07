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
  infoInput.value = infoText.innerText;
  infoInput.style.display = "block";
}

SaveInfoText = () => {
  const infoInput = document.getElementById("infoInput");
  const infoText = document.getElementById("info-text");
  
  infoText.innerText = infoInput.value;
  infoText.style.display = "block";
  infoInput.style.display = "none";
}
