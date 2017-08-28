function checkCommentOne() {
  if (question_comments[0].childNodes[1].childNodes[1]) {
    spanCount ++
  }
}
function checkCommentTwo() {
  if (question_comments[1].childNodes[1].childNodes[1]) {
    spanCount ++
  }
}

var question_comment_list = document.getElementById("qc-list");
var question_comments = question_comment_list.getElementsByTagName("li");
var theButton = document.getElementById('question-comment-button')
var spanCount = 0
if (question_comments.length > 2) {
  checkCommentOne()
  checkCommentTwo()
  if (spanCount == 2) {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-load-more-two-span-button'
  } else if (spanCount == 1) {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-load-more-one-span-button'
  } else {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-load-more-no-span-button'
  }
} else if (question_comments.length == 2) {
  checkCommentOne()
  checkCommentTwo()
  if (spanCount == 2) {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-two-span-button'
  } else if (spanCount == 1) {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-one-span-button'
  } else {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-no-span-button'
  }
} else if (question_comments.length == 1) {
  checkCommentOne()
  if (spanCount == 1) {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-one-com-one-span-button'
  } else {
    theButton.className = ''
    theButton.className += 'btn btn-primary qc-one-com-no-span-button'
  }
} else {
  theButton.className = ''
  theButton.className += 'btn btn-primary qc-no-com-button'
}
