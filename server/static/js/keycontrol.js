let deltaTime = 0.2; // seconds between updates
let deltaTimeMillis = deltaTime * 1000;
let acceleration = 0.3; // speed increase per second
let forwardKey = "ArrowUp";
let backwardKey = "ArrowDown";
let leftKey = "ArrowLeft";
let rightKey = "ArrowRight";
let stopKey = ' ';
let stopKey2 = 'Spacebar';

var forwardSpeed = 0;
var prevLeftSpeed = 0;
var prevRightSpeed = 0;

var inputInterval;

function enableKeyControl() {
    inputInterval = setInterval(handleKeyInput, deltaTimeMillis);
}

function disableKeyControl() {
    if (inputInterval != null) {
        clearInterval(inputInterval);
    }
    inputInterval = null;
}


const keystates = {};
window.addEventListener('keydown', (e) => onKeyDown(e));
window.addEventListener('keyup', (e) => keystates[e.key] = false);

function onKeyDown(e) {
    keystates[e.key] = true;
    if (e.key == stopKey || e.key == stopKey2 && !e.repeat) {
        forwardSpeed = 0
        prevLeftSpeed = 0
        prevRightSpeed = 0
        sendSetLeftRightSpeeds(0, 0);
    }
}

function isKeyDown(key) {
    return keystates.hasOwnProperty(key) && keystates[key];
}

function handleKeyInput() {

        if (isKeyDown(forwardKey)) {
            forwardSpeed += deltaTime * acceleration;
        }
        if (isKeyDown(backwardKey)) {
            forwardSpeed -= deltaTime * acceleration;
        }

        if (forwardSpeed > 1) {
            forwardSpeed = 1;
        }
        else if (forwardSpeed < -1) {
            forwardSpeed = -1;
        }

        leftSpeed = forwardSpeed;
        rightSpeed = forwardSpeed;

        if (isKeyDown(leftKey) && isKeyDown(rightKey)) {

        }
        else if (isKeyDown(leftKey)) {
            leftSpeed = -1;
            rightSpeed = 1;
        }
        else if (isKeyDown(rightKey)) {
            leftSpeed = 1;
            rightSpeed = -1;
        }

        if (isKeyDown(stopKey) || isKeyDown(stopKey2)) {
            forwardSpeed = 0;
            leftSpeed = 0;
            rightSpeed = 0;
        }

        if (prevLeftSpeed != leftSpeed && prevRightSpeed != rightSpeed) {
            sendSetLeftRightSpeeds(leftSpeed, rightSpeed);
            prevLeftSpeed = leftSpeed;
            prevRightSpeed = rightSpeed;
        }

}

