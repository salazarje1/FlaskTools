from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


debug = DebugToolbarExtension(app)

survey = surveys["satisfaction"]

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/start-survey', methods=['POST'])
def start_survey():
    session["responses"] = []
    return redirect('/question/0')

@app.route('/question/<int:question_num>')
def handle_questions(question_num):
    responses = session['responses']
    print(len(survey.questions))
    print(len(responses))

    if len(responses) == len(survey.questions):
        return redirect("/thank-you")
    elif len(responses) != question_num: 
        flash("You must go in order sorry.")
        return redirect(f'/question/{len(responses)}')
    else: 
        return render_template("form.html", survey=survey, num=len(responses))


@app.route('/response/<int:num>', methods=["POST"])
def handle_answer(num):
    answer = request.form["question"]
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    num += 1 
    if(len(survey.questions) == len(responses)):
        return redirect("/thank-you")
    else: 
        return redirect(f"/question/{num}")


@app.route('/thank-you')
def thank_you():
    return render_template("thank.html")