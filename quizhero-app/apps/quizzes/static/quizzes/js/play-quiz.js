const quiz = JSON.parse(document.currentScript.getAttribute('data-quiz'));

const quizBox = document.querySelector('.quiz_box'),
    optionsList = document.querySelector('.options_list');

let queCount = 0,
    queNumber = 1,
    userRating = 0,
    widthValue = 0;

window.onload = function () {
    quizBox.classList.add("activeQuiz");
    show_questions(0);
    queCounter(1);
};

const nextBtn = document.querySelector('.question-footer .next_btn'),
    question_counter_down = document.querySelector('.question-footer .total_que');

const backBtn = document.querySelector('.question-footer .back_btn');

backBtn.onclick = () => {
    if (queCount > 0) {
        queCount--;
        queNumber--;
        show_questions(queCount);
        queCounter(queNumber);
    }
};

nextBtn.onclick = () => {
    if (queCount < quiz.questions.length - 1) {
        queCount++;
        queNumber++;
        show_questions(queCount);
        queCounter(queNumber);
    }
};

function show_questions(index) {
    const queText = document.querySelector('.que_text');

    let queTag = '<span>' + (index + 1) + ". " + quiz.questions[index].description + '</span>';
    let optionTag = '';
    for (let i = 0; i < quiz.questions[index].alternatives.length; i++) {
        optionTag += '<div class="option" data-alternative=\'' + JSON.stringify(quiz.questions[index].alternatives[i]) + '\'>'
            + '<span>' + quiz.questions[index].alternatives[i].description + '</span></div>';
    }

    queText.innerHTML = queTag;
    optionsList.innerHTML = optionTag;

    const option = optionsList.querySelectorAll('.option');

    for (let i = 0; i < option.length; i++) {
        option[i].setAttribute("onclick", "optionSelected(this)");
    }
}

let tickIcon = '<div class="icon tick"><i class="fas fa-check"></i></div>';
let crossIcon = '<div class="icon cross"><i class="fas fa-times"></i></div>';

function optionSelected(answer) {
    const selectedAlternative = JSON.parse(answer.getAttribute('data-alternative'));

    const allOptions = optionsList.children.length;

    for (let i = 0; i < quiz.questions[queCount].alternatives.length; i++) {
        if (quiz.questions[queCount].alternatives[i].is_correct) {
            correctAnswer = quiz.questions[queCount].alternatives[i].description;
        }
    }

    if (selectedAlternative.is_correct) {
        userRating += 1;
        answer.classList.add("correct");
        answer.insertAdjacentHTML('beforeend', tickIcon);
        console.log('Correct Answer');
        console.log('Your correct answers = ' + userRating);
    } else {
        answer.classList.add('incorrect');
        answer.insertAdjacentHTML('beforeend', crossIcon);
        console.log('Wrong Answer');

        for (let i = 0; i < allOptions; i++) {
            if (optionsList.children[i].textContent === correctAnswer) {
                optionsList.children[i].setAttribute('class', 'option correct');
                optionsList.children[i].insertAdjacentHTML('beforeend', tickIcon);
                console.log('Auto selected correct answer');
            }
        }
    }

    for (let i = 0; i < allOptions; i++) {
        optionsList.children[i].classList.add('disabled');
    }
}

function queCounter(index) {
    let totalQueCounTag = '<span><p>' + index + '</p> of <p>' + quiz.questions.length + '</p> Questions</span>';
    question_counter_down.innerHTML = totalQueCounTag;
}
