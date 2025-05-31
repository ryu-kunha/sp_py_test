from flask import Flask, render_template, request, jsonify
import io
import contextlib
import random

app = Flask(__name__)

# 예시 문제 목록 (자유롭게 추가 가능)
questions = [
    {"code": "print(3 + 5)", "answer": "8"},
    {"code": "print('Hello' + 'World')", "answer": "HelloWorld"},
    {"code": "print(len([1, 2, 3, 4]))", "answer": "4"},
    {"code": "a = 10\nb = 20\nprint(a * b)", "answer": "200"},
    {"code": "print('파이썬'[::-1])", "answer": "썬이파"},
    {"code": "for i in range(3):\n    print(i)", "answer": "0\n1\n2"},
    {"code": "print(sum([1, 2, 3]))", "answer": "6"},
    {"code": "def f(x):\n    return x**2\nprint(f(4))", "answer": "16"},
    {"code": "x = [1, 2, 3]\nx.append(4)\nprint(x)", "answer": "[1, 2, 3, 4]"},
    {"code": "print(bool(''))", "answer": "False"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    q = random.choice(questions)
    return jsonify({"code": q["code"]})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    user_code = data.get('code')
    user_answer = data.get('user_answer')

    # 코드 실행 후 출력값 얻기
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f):
            exec(user_code, {})
        output = f.getvalue().strip()
    except Exception as e:
        return jsonify({"result": "error", "msg": str(e)})

    # 정답 비교
    if output == user_answer.strip():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong", "correct_output": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
