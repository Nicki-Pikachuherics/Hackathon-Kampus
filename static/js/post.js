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