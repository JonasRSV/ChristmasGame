const FACTS_URL = "ws://" + window.location.hostname + ":8000/facts"

d3.select("body").data([1, 2, 3, 4, 5]).enter().append("div").append("p").text((d) => "Im number " + d);

FACTS_POLL = null

InitializeFactsComms = () => {

    var socket = new WebSocket(FACTS_URL)

    //Open and recieve
    socket.onopen = () => FACTS_POLL = setInterval(() => socket.send("Ping"), 2000);

    socket.onmessage = (event) => console.log(event.data);

    //Repeatedly check for reconnect
    socket.onclose = (event) => {
        clearInterval(FACTS_POLL);

        console.log("Retrying Connection in a few seconds.. ")
        setTimeout(() => InitializeFactsComms(), 10000);
    }
}

window.onload = InitializeFactsComms
