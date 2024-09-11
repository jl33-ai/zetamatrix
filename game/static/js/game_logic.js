const { send } = require("express/lib/response");

function generateQuestion() {
    const opList = ['+', '-', '*', '/'];
    const oper = opList[Math.floor(Math.random() * opList.length)];
    let num1, num2;

    if (oper === '+' || oper === '-') {
        num1 = Math.floor(Math.random() * 99) + 2; // 2 to 100
        num2 = Math.floor(Math.random() * 99) + 2; // 2 to 100
    } else if (oper === '*') {
        num1 = Math.floor(Math.random() * 11) + 2; // 2 to 12
        num2 = Math.floor(Math.random() * 99) + 2; // 2 to 100
    } else if (oper === '/') {
        num2 = Math.floor(Math.random() * 11) + 2; // 2 to 12
        num1 = num2 * (Math.floor(Math.random() * 99) + 2); // Ensure divisibility
    }

    return [num1, oper, num2];
}

function sendData(score, gameLength, questionsSolved, is_dailychallenge=false) {
    /*
    console.log(score)
    console.log(gameLength)
    console.log(questionsSolved)*/
    
    const csrfToken = document.getElementById('csrfToken').value;
    fetch('/game/save_game_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }, 
        body: JSON.stringify( { score, gameLength, questionsSolved, is_dailychallenge } )
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function startGame(gameLength) {
    let timeLeft = gameLength;
    let answerBox = document.getElementById('answer');
    let questionBox = document.getElementById('question');
    let solvedBox = document.getElementById('score');
    let score = 0;
    let questionsSolved = [];
    let slowest = [0, '', 0, 0];
    let slowest_time = 0;
    let fastest = [0, '', 0, 0];
    let fastest_time = 99999;
    
    // Hide the results panel at the start of every new game
    document.getElementById('gameResults').style.display='none';
    
    function updateTimerDisplay() {
        document.getElementById('timer').innerText = `Seconds left: ${timeLeft}`;
        timeLeft -= 1;
        if (timeLeft < 0) {
            endGame();
        }
    }

    let timerInterval = setInterval(updateTimerDisplay, 1000);

    function endGame() {
        clearInterval(timerInterval); // Stop the timer
        sendData(score, gameLength, questionsSolved);
        console.log(fastest[0], fastest[1], fastest[2], fastest[3])
        document.getElementById('finalScore').innerText = `Your score is: ${score}`; 
        document.getElementById('fastestQuestionBox').innerText = `☻ fastest: ${fastest_time}s  |  ${fastest[0]} ${fastest[1]} ${fastest[2]} = ${fastest[3]}`; 
        document.getElementById('slowestQuestionBox').innerText = `☹︎ slowest: ${slowest_time}s  |  ${slowest[0]} ${slowest[1]} ${slowest[2]} = ${slowest[3]}`; 
        document.getElementById('slowestQuestionBox').innerText = `test`;
        document.getElementById('gameResults').style.display = 'block';
        return;
    }

    function askQuestion() {
        let lastTime = Date.now();
        let [num1, oper, num2] = generateQuestion();
        questionBox.innerText = `${num1} ${oper} ${num2}`;

        answerBox.value = '';

        answerBox.oninput = function() {
            let userAnswer = parseFloat(answerBox.value);
            let correctAnswer;

            try {
                correctAnswer = eval(questionBox.innerText);
            } catch (e) {
                console.error("Error evaluating question:", e);
                return;
            }

            if (!isNaN(userAnswer) && userAnswer === correctAnswer) {
                let timeTaken = Date.now() - lastTime; 
                if (timeTaken < fastest_time) {
                    fastest_time = timeTaken;
                    fastest = [num1, oper, num2, correctAnswer];
                }
                if (timeTaken > slowest_time) {
                    slowest_time = timeTaken;
                    slowest = [num1, oper, num2, correctAnswer];
                }
                // need number of key strokes entered minus legth of answer. 
                score = score + 1;
                solvedBox.innerText = `Score: ${score}`;
                questionsSolved.push({
                    num1: num1,
                    operator: oper,
                    num2: num2,
                    timeTaken: timeTaken
                });
                askQuestion();
            }
        };
    }

    askQuestion(); // Start the game by asking the first question
}
