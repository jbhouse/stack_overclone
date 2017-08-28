  function printMessage() {
    console.log('it is working')
  }

  function checkCommentOne() {
    if (answer_comments[0].childNodes[1].childNodes[1]) {
      spanTotal ++
    }
  }
  function checkCommentTwo() {
    if (answer_comments[1].childNodes[1].childNodes[1]) {
      spanTotal ++
    }
  }

  var answerCommentDiv = document.getElementsByClassName('answer-comment-section')[answerCount-1];
  var answerCommentId = answerCommentDiv.getAttribute('id').slice(16,answerCommentDiv.getAttribute('id').length)
  var answer_comments = answerCommentSection.getElementsByTagName('li')
  var theButton = document.getElementById('answer-comment-button-'+answerCommentId)
  var spanTotal = 0
  if (answer_comments.length == 0) {
    theButton.className = ''
    theButton.className += 'btn btn-primary answer-comment-button no-comment-button'
  } else if (answer_comments.length == 1) {
    checkCommentOne()
    if (spanTotal == 1) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button one-comment-button'
    } else {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button one-comment-no-span-button'
    }
  } else if (answer_comments.length == 2) {
    checkCommentOne()
    checkCommentTwo()
    if (spanTotal == 2) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button two-comment-two-span-button'
    } else if (spanTotal == 1) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button two-comment-one-span-button'
    } else if (spanTotal == 0) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button two-comment-no-span-button'
    }
  } else {
    checkCommentOne()
    checkCommentTwo()
    if (spanTotal == 2) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button load-comment-two-span-button'
    } else if (spanTotal == 1) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button load-comment-one-span-button'
    } else if (spanTotal == 0) {
      theButton.className = ''
      theButton.className += 'btn btn-primary answer-comment-button load-comment-no-span-button'
    }
  }
