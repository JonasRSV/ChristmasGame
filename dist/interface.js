//Connection variables
const INTERFACE_URL = "ws://" + window.location.hostname + ":8000/interface"
var SOCKET = null
var SOCKET_OPEN = false

// State variables
var CLIENT_NAME = "Mr. Smith"
var LAST_CLICK = new Date().getTime()


window.onload = () => {
    renderSnow();
    setupSocket();
    setupEventListeners();
}


setupSocket = () => {
    SOCKET = new WebSocket(INTERFACE_URL)
    console.log("Attempting to connect to " + INTERFACE_URL)
    SOCKET.onopen = () => SOCKET_OPEN = true
    SOCKET.onmessage = (event) => renderData(JSON.parse(event.data));
    SOCKET.onclose = (event) => {
        SOCKET_OPEN = false;
        setTimeout(() => setupSocket(), 10000);
    }
}

setupEventListeners = () => {
    var package_add = document.getElementById("package-add")
    var input_field = document.getElementById("client-name")
    var name_field = document.getElementById("name")

    package_add.addEventListener("click", () => {
        if ((new Date().getTime() - LAST_CLICK) < 2000) {
            return null
        }

        LAST_CLICK = new Date().getTime()

        if (SOCKET_OPEN) {
            SOCKET.send(CLIENT_NAME)
            console.log("Set animation")

            // Not sure how it is intended to apply temporary keyframe animations
            // this hack works though
            package_add.style.animation = "gift-add 1s linear";
            setTimeout(() => package_add.style.animation = null, 950);
        } else {
            document.body.style.animation = "gift-add-fail 2s linear";
            setTimeout(() => document.body.style.animation = null, 2000);
            console.log("Socket is not open")
        }

    }, false);

    input_field.addEventListener("keydown", (data) => {
        if (data["key"] === "Enter") {
            CLIENT_NAME = input_field.value
            name_field.innerHTML = CLIENT_NAME

            input_field.style.animation = "name-disappear linear 0.5s"
            setTimeout(() => {
                package_add.style.display = "block"
                input_field.style.display = "none"
                input_field.readOnly = true

                // Package fade in
                package_add.style.animation = "gift-appear linear 1s"
                setTimeout(() => package_add.style.animation = null, 950)
            }, 450);

        } else if (data["key"].length > 2) {
            setTimeout(() => name_field.innerHTML = input_field.value, 10)
        } else {
            name_field.innerHTML = input_field.value + data["key"]
        }

    }, false);

    name_field.addEventListener("click", () => {

        // Package fade out
        package_add.style.animation = "gift-disappear linear 1s";
        setTimeout(() => {
            package_add.style.animation = null;
            package_add.style.display = "none";

            input_field.style.animation = "name-appear linear 0.5s";
            input_field.style.display = "block";
            input_field.readOnly = false;
            setTimeout(() => input_field.animation = null, 500);

        }, 950)

    }, false);
}

// Data
// # ways to sort the packages
// # of packages
renderData = (data) => {
    var tuples = [
        ["packages", data["packages"]],
        ["combinations", data["combinations"]]
    ]

    var information = d3.select("div.information-container").selectAll("div.information").data(tuples).text((d) => d[0] + ": " + d[1]);
    information = information.enter().append("div").attr('class', 'information').text((d) => d[0] + ": " + d[1]);
    information.exit().remove();
}


renderSnow = () => {
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
