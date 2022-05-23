from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


debug = DebugToolbarExtension(app)

responses = []
question_list = list(range(len(surveys["satisfaction"].questions)))

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/question/<int:question_num>')
def handle_questions(question_num):
    if not question_list: 
        return redirect("/thank-you")
    elif question_num == question_list[0]:
        survey = surveys["satisfaction"]
        return render_template("form.html", num=question_num, survey=survey)
    else: 
        flash("You must go in order sorry.")
        return redirect(f'/question/{question_list[0]}')


@app.route('/response/<int:num>', methods=["POST"])
def handle_answer(num):
    answer = request.form["question"]
    responses.append(answer)
    num = num + 1
    if(num == len(surveys["satisfaction"].questions)):
        print(responses)
        return redirect("/thank-you")
    else: 
        question_list.pop(0)
        return redirect(f"/question/{num}")


@app.route('/thank-you')
def thank_you():
    return render_template("thank.html")