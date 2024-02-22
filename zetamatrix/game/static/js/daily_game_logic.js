const { send } = require("express/lib/response");

function sendData(score, gameLength, questionsSolved, is_dailychallenge=true) {
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

function startGame(gameLength, questions) {
    let timeLeft = gameLength;
    let answerBox = document.getElementById('answer');
    let questionBox = document.getElementById('question');
    let solvedBox = document.getElementById('score');
    let score = 0;
    let questionsSolved = [];
    let i = 0;
    
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
        document.getElementById('finalScore').innerText = `Your score is: ${score}`; 
        document.getElementById('gameResults').style.display = 'block';
        return;
    }

    function askQuestion() {
        let lastTime = Date.now();
        let { num1, oper, num2 } = questions[i];
        i+=1;
        if (i>=300) {
            endGame();
        }

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

            if (userAnswer === correctAnswer) {
                let timeTaken = Date.now() - lastTime; 
                // need number of key strokes entered minus legth of answer. 
                score = score + 1;
                solvedBox.innerText = `Score: ${score}`;
                console.log(num1, oper, num2, timeTaken);
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
