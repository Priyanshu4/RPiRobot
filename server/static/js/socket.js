// connects socket to flask webserver
var socket = io();
socket.on('connect', function () {
    socket.send('I\'m connected!');
});

function sendTurnOn() {
    socket.emit('turn on');
}

function sendTurnOff() {
    socket.emit('turn off');
}

function sendSetLeftRightSpeeds(left, right) {
    socket.emit('set left right speeds', left, right)
}

function sendSetForwardTurnSpeeds(forward, turn) {
    socket.emit('set forward turn speeds', forward, turn)
}

function sendSaveSnapshot() {
    socket.emit('save snapshot');
}

function sendSetControlMode(controlMode) {
    socket.emit('set control mode', controlMode);
}
