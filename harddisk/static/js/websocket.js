var domain = location.hostname;
var wsdomain = null;
if (location.protocol.indexOf("https") > -1){
    wsdomain = "wss://" + domain + "/ws/";

}else {
    wsdomain = "ws://"+ domain +":1337/ws/";
}

let sc = new WebSocket(wsdomain + sKey + "/");

sc.onopen = function (e) {
};

sc.onmessage = function (event) {
    let obj = JSON.parse(event.data);
    let notification = document.getElementById("notificaon-id");
    if(notification){
        if(obj.count>-1) {
            notification.innerHTML = obj.count;
        } else {
            notification.innerHTML = "-1";
        }
    }

};

sc.onclose = function (event) {
};
