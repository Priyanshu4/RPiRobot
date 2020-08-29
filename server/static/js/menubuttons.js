let onoffbuttonid = "onoffbutton";
let on = "Turn On";
let off = "Turn Off";
let oncolor = "#4CAF50";
let offcolor = "red";

let videofeedcaptionid = "videofeedcaption";
let controlmodeheaderid = "controlmodeheader";

let keyboardcontrol = "Keyboard Control";
var currentcontrolmode;

function turnOnRobot() {
    document.getElementById(onoffbuttonid).innerHTML = off;
    document.getElementById(onoffbuttonid).style.backgroundColor = offcolor;
    sendTurnOn();
    if (currentcontrolmode == keyboardcontrol) {
        enableKeyControl();
    }
}

function turnOffRobot() {
    document.getElementById(onoffbuttonid).innerHTML = on;
    document.getElementById(onoffbuttonid).style.backgroundColor = oncolor;
    sendTurnOff();
    disableKeyControl();
}

function toggleOnOff() {
    if (document.getElementById(onoffbuttonid).innerHTML === on) {
        turnOnRobot();
    }
    else {
        turnOffRobot();
    }
}

function saveSnapshot() {
    sendSaveSnapshot();
    document.getElementById(videofeedcaptionid).innerHTML = "Saving Snapshot...";
    setTimeout(clearVideoFeedCaption, 1000);
}

function clearVideoFeedCaption() {
    document.getElementById(videofeedcaptionid).innerHTML = "";
}

function setRobotControlMode(controlmode) {
    if (controlmode == keyboardcontrol) {
        enableKeyControl();
    }
    else {
        disableKeyControl();
    }
    currentcontrolmode = controlmode;
    sendSetControlMode(controlmode);
    document.getElementById(controlmodeheaderid).innerHTML = controlmode + " Mode";
}

