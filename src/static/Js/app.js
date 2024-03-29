// // Socket connect
// let url = `${window.location.protocol == "https:" ? "wss" : "ws"}://${
//     window.location.host
// }/ws/socket-server/`;
// const doorSocket = new WebSocket(url);
//
// // Element defined in HTML
// const openBtn = document.getElementById("openBtn");
// const doorOpenCmdText = document.getElementById("doorOpenCmdText");
// const closeText = document.getElementById("closeText");
//
// doorSocket.onmessage = function (e) {
//     let data = JSON.parse(e.data);
//     console.log(data)
//   if (data.type === "door") {
//     const msg = data?.message;
//     console.log(msg)
//     const t = data.time
//     if (msg !== "Close") {
//       opened(t);
//     } else {
//       closed();
//     }
//   }
// };
// //     if (data.type === "door") {
// //         // const msg = data?.message;
// //         // console.log(msg)
// //         const t = data.time
// //         if (t !== 1) {
// //             opened(t);
// //         } else {
// //             closed();
// //         }
// //     }
// // };
//
// const opened = (t) => {
//     openBtn.disabled = true;
//     openBtn.classList.remove("bg-gray-100");
//     openBtn.classList.remove("cursor-pointer");
//     openBtn.classList.add("bg-gray-500");
//     openBtn.classList.add("cursor-not-allowed");
//     doorOpenCmdText.style.display = "none";
//     closeText.innerText = "The door will close in " + t + " second.";
//     doorSocket.send(
//         JSON.stringify({
//             message: "Close",
//         })
//     );
// };
//
// const closed = () => {
//     openBtn.disabled = false;
//     closeText.innerText = "";
//     openBtn.classList.remove("bg-gray-500");
//     openBtn.classList.remove("cursor-not-allowed");
//     openBtn.classList.add("bg-gray-100");
//     openBtn.classList.add("cursor-pointer");
//     doorOpenCmdText.style.display = "block";
// };
//
// openBtn.addEventListener("click", () => {
//     fetch("/door")
//         .then((res) => {
//             if (res.status === 200) {
//                 doorSocket.send(
//                     JSON.stringify({
//                         message: "Open",
//                     })
//                 );
//             }
//             return res.json();
//         })
//         .catch((err) => {
//             console.log(err);
//         });
// });
// Socket connect
let url = `${window.location.protocol == "https:" ? "wss" : "ws"}://${
    window.location.host
}/ws/socket-server/`;
const doorSocket = new WebSocket(url);
// doorSocket.addEventListener('open', (e) => {
//     let data = JSON.parse(e.data);
//     console.log(data)
//
// });

// Element defined in HTML
const openBtn = document.getElementById("openBtn");
const doorOpenCmdText = document.getElementById("doorOpenCmdText");
const closeText = document.getElementById("closeText");

doorSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    // console.log(data);
    if (data.type === "door") {
        // const msg = data?.message;
        // console.log(msg)
        const t = data.time

        // const t = data.time

        if (t !== 1) {
            opened(t);
        } else {
            closed();
        }
    }
};

const opened = (t) => {
    openBtn.disabled = true;
    openBtn.classList.remove("bg-gray-100");
    openBtn.classList.remove("cursor-pointer");
    openBtn.classList.add("bg-gray-500");
    openBtn.classList.add("cursor-not-allowed");
    doorOpenCmdText.style.display = "none";
    closeText.innerText = "The door will close in " + t + " second.";
    // doorSocket.send(JSON.stringify({message: t,}));
    // doorSocket.send(JSON.stringify({message:'ksdk'}));
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
                        message: "Open",
                    })
                );
            }
            return res.json();
        })
        .catch((err) => {
            console.log(err);
        });
});