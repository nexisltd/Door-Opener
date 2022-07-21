const open = document.getElementById("openBtn");
let url = `ws://${window.location.host}/ws/socket-server/`
const doorSocket = new WebSocket(url)
// doorSocket.send(JSON.stringify({
//     'message': 'Open'
// }))
doorSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    console.log('data : ', data)
    if (data.type === 'door') {
        if (data.message === 'Open') {
            opened()
        } else {
            closed()
        }
    }
}

const opened = () => {
    document.getElementById("openBtn").disabled = true;
    document.getElementById("doorOpenCmdText").innerHTML = "";
    document.getElementById("closeText").style.color = "red";
    document.getElementById("powerIcon").style.color = "#fff";
    document.getElementById("openBtn").style.background = "#f1f5f9";
    document.getElementById("openBtn").style.opacity = 0.5;
    document.getElementById("openBtn").innerHTML =
        '<i class="fa-solid fa-power-off text-2xl"></i>';
}

const closed = () => {
    document.getElementById("openBtn").disabled = false;
    document.getElementById("openBtn").style.opacity = 1;
    document.getElementById("closeText").innerHTML = "";
    document.getElementById("doorOpenCmdText").innerHTML =
        "The door is close, please open.";

    document.getElementById("openBtn").style.background = "#e2e8f0";
    document.getElementById("openBtn").innerHTML =
        '<i class="fa-solid fa-power-off text-2xl"></i>';
}

open.addEventListener("click", () => {
    fetch("/door")
        .then(res => {
            if (res.status === 200) {
                doorSocket.send(JSON.stringify({
                    'message': 'Open'
                }))
                opened()
                let timeLeft = 10;
                let closeTimer = setInterval(function () {
                    if (timeLeft <= 0) {
                        clearInterval(closeTimer);
                    }
                    document.getElementById("closeText").innerText =
                        "The door will close in " + timeLeft + " second.";
                    timeLeft -= 1;
                    if (timeLeft < 0) {
                        closed()
                        doorSocket.send(JSON.stringify({
                            'message': 'Close'
                        }))
                    }
                }, 1000);
            }
            return res.json()
        })
        .catch(err => {
            console.log(err);
        })
});

