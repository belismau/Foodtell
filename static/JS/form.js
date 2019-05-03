var datum = new Date().toISOString().substr(0, 10);
document.getElementById('today').value = datum;

var time = new Date();
var tid = time.getHours() + ":" + time.getMinutes();
document.getElementById('today1').value = tid;
