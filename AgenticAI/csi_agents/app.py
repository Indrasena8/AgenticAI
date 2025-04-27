from flask import Flask, request, render_template, redirect
import json
import os
import requests

app = Flask(__name__)
data_file = 'judging_data.json'

rubric_criteria = ["Innovation", "Technical Complexity", "User Experience", "Impact"]

if not os.path.exists(data_file) or os.stat(data_file).st_size == 0:
    with open(data_file, 'w') as f:
        json.dump({"judges": []}, f)

@app.route('/', methods=['GET', 'POST'])
def judge_form():
    if request.method == 'POST':
        judge_name = request.form['judge_name']
        participant_name = request.form['participant_name']
        scores = {criterion: float(request.form[criterion]) for criterion in rubric_criteria}
        average_score = round(sum(scores.values()) / len(scores), 2)

        new_entry = {
            "judge_name": judge_name,
            "participant_name": participant_name,
            "scores": scores,
            "average_score": average_score
        }

        with open(data_file, 'r+') as f:
            data = json.load(f)
            data['judges'].append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        return redirect('/')

    return render_template('judge_form.html', rubric_criteria=rubric_criteria)

@app.route('/declare-winners', methods=['POST'])
def trigger_declare_winners():
    try:
        backend_url = "http://localhost:8000/declare-winners"  # judge.py server
        response = requests.post(backend_url)
        if response.status_code == 200:
            return "🏆 Winners Declared Successfully!"
        else:
            return "❌ Failed to declare winners."
    except Exception as e:
        return f"❌ Error: {str(e)}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)