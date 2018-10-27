//const SOCKET_URL = "ws://192.168.10.222:8000/";
//const SOCKET_URL = "ws://172.26.5.176:8000/";
const SOCKET_URL = "ws://" + window.location.hostname + ":8000/game"
const hostIP = document.createTextNode("http://" + window.location.hostname + ":" + window.location.port + "/game")
var PACKAGE_TEXT = null
var PACKAGE_CONTAINER = null
var UPDATE_POLL = null


//for dev
// const SOCKET_URL = "ws://0.0.0.0:5000/"

UpdateText = (text) => {

    PACKAGE_TEXT = text

    //Gets comment object from page
    gift = document.getElementById("gift").cloneNode(true)
    gift.id = ""
    gift.style = ""

    //Creates and appends text
    node = document.createTextNode(text);
    gift.firstElementChild.appendChild(node);

    if (PACKAGE_CONTAINER.hasChildNodes()) {
        PACKAGE_CONTAINER.insertBefore(gift, PACKAGE_CONTAINER.firstElementChild);
    } else {
        PACKAGE_CONTAINER.appendChild(gift);
    }

    setTimeout(() => {
        gift.className = "gift--container active"
    }, 200);
}

UpdateGift = (text) => {
    if (text != PACKAGE_TEXT) {
        PACKAGE_CONTAINER.firstElementChild.className = "gift--container inactive"
        setTimeout(() => UpdateText(text), 1500);
        setTimeout(() => PACKAGE_CONTAINER.removeChild(PACKAGE_CONTAINER.lastElementChild), 1500);
    }
}


InitializeSocketComms = () => {

    connectingIcon = document.getElementById("connecting")
    var socket = new WebSocket(SOCKET_URL)

    //Open and recieve
    socket.onopen = () => {
      UPDATE_POLL = setInterval(() => socket.send("Ping"), 2000);
      connectingIcon.className = "icon--connecting inactive";
    }

    socket.onmessage = (event) => UpdateGift(event.data);

    //Repeatedly check for reconnect
    socket.onclose = (event) => {
        clearInterval(UPDATE_POLL);
        connectingIcon.className = "icon--connecting active"

        console.log("Retrying Connection in a few seconds.. ")
        setTimeout(() => InitializeSocketComms(), 10000);
    }
}


runGame = () => {
    snowyRun();
    PACKAGE_CONTAINER = document.getElementById("gifts");
    UpdateText("Xmas Game 2017");

    InitializeSocketComms();


    console.log(hostIP);
    console.log(document.getElementById("ip--info"));
    document.getElementById("ip--info").appendChild(hostIP);
}

window.onload = runGame



snowyRun = () => {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    var W = window.innerWidth;
    var H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;

    var mp = 25; //max particles
    var particles = [];
    for (var i = 0; i < mp; i++) {
        particles.push({
            x: Math.random() * W, //x-coordinate
            y: Math.random() * H, //y-coordinate
            r: Math.random() * 4 + 1, //radius
            d: Math.random() * mp //density
        })
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
        ctx.beginPath();
        for (var i = 0; i < mp; i++) {
            var p = particles[i];
            ctx.moveTo(p.x, p.y);
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2, true);
        }
        ctx.fill();
        update();
    }

    var angle = 0;

    function update() {
        angle += 0.01;
        for (var i = 0; i < mp; i++) {
            var p = particles[i];
            p.y += Math.cos(angle + p.d) + 1 + p.r / 2;
            p.x += Math.sin(angle) * 2;

            if (p.x > W + 5 || p.x < -5 || p.y > H) {
                if (i % 3 > 0) //66.67% of the flakes
                {
                    particles[i] = {
                        x: Math.random() * W,
                        y: -10,
                        r: p.r,
                        d: p.d
                    };
                } else {
                    if (Math.sin(angle) > 0) {
                        particles[i] = {
                            x: -5,
                            y: Math.random() * H,
                            r: p.r,
                            d: p.d
                        };
                    } else {
                        particles[i] = {
                            x: W + 5,
                            y: Math.random() * H,
                            r: p.r,
                            d: p.d
                        };
                    }
                }
            }
        }
    }

    setInterval(draw, 33);
}
