const open = document.getElementById("open");

open.addEventListener("click", () => {
  fetch("/door");
  document.getElementById("close").style.color = "red";
  document.getElementById("open").style.background = "red";
  document.getElementById("open").innerHTML = "Opened";
  let timeLeft = 10;
  let closeTimer = setInterval(function () {
    if (timeLeft <= 0) {
      clearInterval(closeTimer);
    }
    // let left = (document.getElementById("timer").innerText = 10 - timeLeft);
    document.getElementById("close").innerText =
      "door close in " + (10 - timeLeft) + " second";
    // document.getElementById("progressBar").value = 10 - timeLeft;
    timeLeft -= 1;
    if (timeLeft < 0) {
      document.getElementById("close").innerHTML = "";
      document.getElementById("open").style.background = "#60A5FA";
      document.getElementById("open").innerHTML = "Open";

    }
  }, 1000);
});
