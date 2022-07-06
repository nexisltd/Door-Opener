const open = document.getElementById("openBtn");

open.addEventListener("click", () => {
  fetch("/door")
  .then(res=>{
    if( res.status===200){
      document.getElementById("openBtn").disabled = true;
      document.getElementById("doorOpenCmdText").innerHTML = "";
      document.getElementById("closeText").style.color = "red";
      document.getElementById("openBtn").style.background = "#334155";
      document.getElementById("openBtn").style.opacity = 0.6;
      document.getElementById("openBtn").innerHTML =
        '<i class="fa-solid fa-power-off text-2xl"></i>';
      let timeLeft = 10;
      let closeTimer = setInterval(function () {
        if (timeLeft <= 0) {
          clearInterval(closeTimer);
        }
        document.getElementById("closeText").innerText =
          "The door will close in " + timeLeft + " second.";
        timeLeft -= 1;
        if (timeLeft < 0) {
      
          document.getElementById("openBtn").addEventListener("mouseover", mouseOver);
          document.getElementById("openBtn").addEventListener("mouseout", mouseOut);
          
          function mouseOver() {
            document.getElementById("openBtn").style.opacity = 0.6;          }
          
          function mouseOut() {
            document.getElementById("openBtn").style.opacity = 1;          }
          document.getElementById("openBtn").disabled = false;
          document.getElementById("openBtn").style.opacity = 1;
          document.getElementById("closeText").innerHTML = "";
          document.getElementById("doorOpenCmdText").innerHTML =
            "The door is close, please open.";
    
          document.getElementById("openBtn").style.background = "#e2e8f0";
          document.getElementById("openBtn").innerHTML =
            '<i class="fa-solid fa-power-off text-2xl"></i>';
        }
      }, 1000);
    }
    return res.json()
  })
  .catch(err=>{
    console.log(err);
  })

  
});
