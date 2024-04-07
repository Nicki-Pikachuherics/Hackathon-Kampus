
document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    fetch('/post/comment', {method: 'POST', body: formData}).then((response) => {
      location.reload()
    })
  });
});

function changeInfoText(university_id){
  const infoText = document.getElementById("infoText");
  const changeInfoBtn = document.getElementById("changeinfoBtn");
  infoText.style.display = "none";
  changeInfoBtn.style.display = "none";
  const saveInfoBtn = document.getElementById("saveinfoBtn");
  const infoInput = document.getElementById("infoInput");
  saveInfoBtn.style.display = "block";
  infoInput.style.display = "block";
  infoInput.value = infoText.textContent;
};

function SaveInfoText(university_id){
  const infoInput = document.getElementById("infoInput");
  const infoText = document.getElementById("infoText");
  fetch('/university/info', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'newInfo': infoInput.value, 'university_id': university_id})})
  infoText.innerText = infoInput.value;
  infoText.style.display = "block";
  infoInput.style.display = "none";
  const changeInfoBtn = document.getElementById("changeinfoBtn");
  const saveInfoBtn = document.getElementById("saveinfoBtn");
  changeInfoBtn.style.display = "block";
  saveInfoBtn.style.display = "none";
}
