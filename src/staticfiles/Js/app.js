// Socket connect
let url = `wss://${window.location.host}/ws/socket-server/`;
const doorSocket = new WebSocket(url);

// Element defined in HTML
const openBtn = document.getElementById("openBtn");
const doorOpenCmdText = document.getElementById("doorOpenCmdText");
const closeText = document.getElementById("closeText");

doorSocket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  //   console.log(data);

  if (data.type === "door") {
    const msg = data?.message?.message;
    if (msg !== "Close") {
      msg !== "Open" && opened(msg);
    } else {
      closed();
    }
  }
};

const time = () => {
  let timeLeft = 10;
  let closeTimer = setInterval(function () {
    if (timeLeft <= 0) {
      clearInterval(closeTimer);
    }
    doorSocket.send(
      JSON.stringify({
        message: { message: timeLeft },
      })
    );
    timeLeft -= 1;

    if (timeLeft < 0) {
      doorSocket.send(
        JSON.stringify({
          message: { message: "Close" },
        })
      );
    }
  }, 1000);
  // return timeLeft;
};

const opened = (msg) => {
  openBtn.disabled = true;
  openBtn.classList.remove("bg-gray-100");
  openBtn.classList.remove("cursor-pointer");
  openBtn.classList.add("bg-gray-500");
  openBtn.classList.add("cursor-not-allowed");
  doorOpenCmdText.style.display = "none";
  closeText.innerText = "The door will close in " + msg + " second.";
  //   console.log(msg);
  //   time();
};

const closed = () => {
  openBtn.disabled = false;
  closeText.innerText = "";
  openBtn.classList.remove("bg-gray-500");
  openBtn.classList.remove("cursor-not-allowed");
  openBtn.classList.add("bg-gray-100");
  openBtn.classList.add("cursor-pointer");
  doorOpenCmdText.style.display = "block";
};

openBtn.addEventListener("click", () => {
  fetch("/door")
    .then((res) => {
      if (res.status === 200) {
        doorSocket.send(
          JSON.stringify({
            message: { message: "Open" },
          })
        );
        // opened(12);
        time();
      }
      return res.json();
    })
    .catch((err) => {
      console.log(err);
    });
});
