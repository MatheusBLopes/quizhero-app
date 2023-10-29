const quiz = JSON.parse(
    document.currentScript.nextElementSibling.textContent
  );

const quizBox = document.querySelector('.quiz_box'),
optionsList = document.querySelector('.options_list')

let queCount = 0,
queNumber = 1,
userRating = 0,
widthValue = 0;

window.onload = function() {
    quizBox.classList.add("activeQuiz")
    show_questions(0)
    queCounter(1)
};


const nextBtn = document.querySelector('#footer .next_btn'),
question_counter_down = document.querySelector('#footer .total_que');

const backBtn = document.querySelector('#footer .back_btn');

backBtn.onclick = () => {
    if(queCount > 0) {
        queCount--;
        queNumber--;
        show_questions(queCount);
        queCounter(queNumber);
    }
}


nextBtn.onclick = () => {
    if(queCount < quiz.questions.length - 1) {
        queCount++;
        queNumber++;
        show_questions(queCount);
        queCounter(queNumber);
    }
}

function show_questions(index) {
    const queText = document.querySelector('.que_text')
    let queTag = '<span>' + quiz.questions[index].numb + ". " + quiz.questions[index].question_description + '</span>'
    let optionTag = '<div class="option"><span>'+ quiz.questions[index].answers[0].answer_description + '</span></div>'
    + '<div class="option"><span>' + quiz.questions[index].answers[1].answer_description + '</span></div>'
    + '<div class="option"><span>' + quiz.questions[index].answers[2].answer_description + '</span></div>'
    + '<div class="option"><span>' + quiz.questions[index].answers[3].answer_description + '</span></div>'

    queText.innerHTML = queTag

    optionsList.innerHTML = optionTag

    const option = optionsList.querySelectorAll('.option')

    for(i=0; i < option.length; i++) {
        option[i].setAttribute("onclick", "optionSelected(this)")
    }
}

let tickIcon = '<div class="icon tick"><i class="fas fa-check"></i></div>'
let crossIcon = '<div class="icon cross"><i class="fas fa-times"></i></div>'

function optionSelected(answer) {

    let userAnswer = answer.textContent
    let correctAnswer = quiz.questions[queCount]
    const allOptions = optionsList.children.length

    for (i = 0; i < quiz.questions[queCount].answers.length; i++) {
        if(quiz.questions[queCount].answers[i].right_answer){
            correctAnswer = quiz.questions[queCount].answers[i].answer_description
        }
    }

    if(userAnswer == correctAnswer) {
        userRating += 1
        answer.classList.add("correct")
        answer.insertAdjacentHTML('beforeend', tickIcon)
        console.log('Correct Answer')
        console.log('Your correct answers = ' + userRating)
    } else {
        answer.classList.add('incorrect')
        answer.insertAdjacentHTML('beforeend', crossIcon)
        console.log('Wrong Answer')

        for (i=0; i < allOptions; i++) {
            if (optionsList.children[i].textContent == correctAnswer) {
                optionsList.children[i].setAttribute('class', 'option correct')
                optionsList.children[i].insertAdjacentHTML('beforeend', tickIcon)
                console.log('Auto selected correct answer')
            }
        }
    }

    for (i=0; i < allOptions; i++) {
        optionsList.children[i].classList.add('disabled')
    }

}

function queCounter(index) {
    let totalQueCounTag = '<span><p>' + index + '</p> of <p>' + quiz.questions.length + '</p> Questions</span>'
    question_counter_down.innerHTML = totalQueCounTag
}