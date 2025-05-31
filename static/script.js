// 현재 문제 코드를 저장하는 변수
let currentCode = '';

// 문제 불러오기
async function loadQuestion() {
  const response = await fetch('/get_question');
  const data = await response.json();
  currentCode = data.code;

  document.getElementById('python-question').textContent = currentCode;
  document.getElementById('answer-input').value = '';
  document.getElementById('result-message').textContent = '정답을 제출하면 결과가 여기에 표시됩니다.';
  document.getElementById('result-message').style.color = '#ffffff';
}

// 정답 제출 처리
async function submitAnswer() {
  const userAnswer = document.getElementById('answer-input').value.trim();

  const response = await fetch('/check_answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_answer: userAnswer,
      code: currentCode
    })
  });

  const result = await response.json();
  const messageBox = document.getElementById('result-message');

  if (result.result === 'correct') {
    messageBox.textContent = '✅ 정답입니다! 잘했어요!';
    messageBox.style.color = '#00FFAA';
  } else if (result.result === 'wrong') {
    messageBox.textContent = `❌ 오답입니다. 정답: ${result.correct_output}`;
    messageBox.style.color = '#FFBABA';
  } else {
    messageBox.textContent = `⚠️ 오류: ${result.msg}`;
    messageBox.style.color = 'orange';
  }

  // 정답 여부 표시 후 자동으로 다음 문제로 이동 (2.5초 후)
  setTimeout(() => {
    loadQuestion();
  }, 2500);  // 2500ms = 2.5초
}

// 이벤트 연결
document.getElementById('submit-answer').addEventListener('click', submitAnswer);

// 페이지 로드 시 문제 불러오기
window.onload = loadQuestion;
