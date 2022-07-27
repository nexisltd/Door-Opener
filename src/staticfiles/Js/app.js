// Socket connect
let url = `${window.location.protocol == "https:" ? "wss" : "ws"}://${
  window.location.host
}/ws/socket-server/`;
const doorSocket = new WebSocket(url);

// Element defined in HTML
const openBtn = document.getElementById("openBtn");
const doorOpenCmdText = document.getElementById("doorOpenCmdText");
const closeText = document.getElementById("closeText");
const timer = document.getElementById("timer");

// Socket event
doorSocket.onmessage = function (e) {
  const { type = "", message = "" } = JSON.parse(e?.data);
  console.log(type, message);
  switch (type) {
    case "door_handler":
      if (message === "Close") {
        closeDoor();
      }
      break;
    case "timer":
      openDoor()
      timerUpdate(message)
    case "client":
      console.log(message)
  }
};
// Timer
timerUpdate = (time) => timer.innerHTML = time;

// Open door
const openDoor = () => {
  openBtn.disabled = true;
  openBtn.classList.remove("bg-gray-100");
  openBtn.classList.remove("cursor-pointer");
  openBtn.classList.add("bg-gray-500");
  openBtn.classList.add("cursor-not-allowed");
  doorOpenCmdText.style.display = "none";
  closeText.style.display = "block";
};

// Close door
const closeDoor = () => {
  openBtn.disabled = false;
  openBtn.classList.remove("bg-gray-500");
  openBtn.classList.remove("cursor-not-allowed");
  openBtn.classList.add("bg-gray-100");
  openBtn.classList.add("cursor-pointer");
  doorOpenCmdText.style.display = "block";
  closeText.style.display = "none";
};

// Open door event
openBtn.addEventListener("click", () => {
  doorSocket.send(JSON.stringify({ type: "door_handler", message: "Open" }));
});
