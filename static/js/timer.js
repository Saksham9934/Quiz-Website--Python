/* timer.js — a small reusable countdown timer.
   Usage:
     const timer = createTimer(totalSeconds, {
         onTick: (secondsLeft) => { ... },
         onExpire: () => { ... }
     });
     timer.start();
     timer.stop();
     timer.getElapsed();
*/

function createTimer(totalSeconds, { onTick, onExpire } = {}) {
    let secondsLeft = totalSeconds;
    let intervalId = null;

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60).toString().padStart(2, "0");
        const s = Math.floor(seconds % 60).toString().padStart(2, "0");
        return `${m}:${s}`;
    }

    function tick() {
        secondsLeft -= 1;
        if (onTick) onTick(secondsLeft, formatTime(secondsLeft));
        if (secondsLeft <= 0) {
            stop();
            if (onExpire) onExpire();
        }
    }

    function start() {
        if (intervalId) return;
        if (onTick) onTick(secondsLeft, formatTime(secondsLeft));
        intervalId = setInterval(tick, 1000);
    }

    function stop() {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
    }

    function getElapsed() {
        return totalSeconds - secondsLeft;
    }

    function getRemaining() {
        return secondsLeft;
    }

    return { start, stop, getElapsed, getRemaining, formatTime };
}
