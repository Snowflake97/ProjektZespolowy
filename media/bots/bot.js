var readline = require('readline');
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

var current_row = 7
var current_col = 12
var current_direction = "left"

rl.on('line', function (line) {
    if (line.includes("move")) {
        // next move
        current_col = getRandomIntInclusive(0, 19)
        current_row = getRandomIntInclusive(0, 19)
        console.log("MOVE---" + current_row + "---" + current_col)
    } else if (line.includes("position_and_direction")) {
        console.log("ROW---" + current_row + "---COLUMN---" + current_col + "---DIRECTION---" + current_direction)
    } else if (line.includes("map")) {
        console.log("MAP_RECEIVED")
    }
})

