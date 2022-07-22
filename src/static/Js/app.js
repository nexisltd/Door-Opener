const open = document.getElementById("openBtn");
let url = `ws://${window.location.host}/ws/socket-server/`
const doorSocket = new WebSocket(url)

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
    document.getElementById("doorOpenCmdText").style.display = "none";
    document.getElementById("openBtn").classList.remove('bg-gray-100')
    document.getElementById("openBtn").classList.remove('cursor-pointer')
    document.getElementById("openBtn").classList.add('bg-gray-500')
    document.getElementById("openBtn").classList.add('cursor-not-allowed')
    document.getElementById("closeText").style.color = "red";
    let timeLeft = 10;
    let closeTimer = setInterval(function () {
        if (timeLeft <= 0) {
            clearInterval(closeTimer);
        }
        document.getElementById("closeText").innerText =
            "The door will close in " + timeLeft + " second.";
        timeLeft -= 1;
        if (timeLeft < 0) {
            doorSocket.send(JSON.stringify({
                'message': 'Close'
            }))
        }
    }, 1000);
}

const closed = () => {
    document.getElementById("openBtn").disabled = false;
    document.getElementById("closeText").innerHTML = "";
    document.getElementById("openBtn").classList.remove('bg-gray-500')
    document.getElementById("openBtn").classList.remove('cursor-not-allowed')
    document.getElementById("openBtn").classList.add('bg-gray-100')
    document.getElementById("openBtn").classList.add('cursor-pointer')
    document.getElementById("doorOpenCmdText").style.display = "block";
}

open.addEventListener("click", () => {
    fetch("/door")
        .then(res => {
            if (res.status === 200) {
                doorSocket.send(JSON.stringify({
                    'message': 'Open'
                }))
                opened()
            }
            return res.json()
        })
        .catch(err => {
            console.log(err);
        })
});

