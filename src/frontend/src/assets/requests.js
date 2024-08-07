function update() {
    let url = SERVER + "/update-feed"
    evtSrc = new EventSource(url);
    evtSrc.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log("data received", data);
    }
    evtSrc.onerror = (e) => {
        console.log("error", e);
        evtSrc.close();
    };
}

function post(url, data) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => {
        return true;
    }).catch(error => {
        console.log(error);
        return false;
    });
}


