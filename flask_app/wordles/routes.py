from flask import Blueprint, render_template, url_for, redirect, flash, abort
from flask_login import current_user, login_required

from ..forms import SearchForm, WordleManualForm, WordlePasteForm
from ..models import User, Wordle
from ..utils import current_time, parse_pasted_wordle, todays_wordle, generate_figure

wordles = Blueprint("wordles", __name__)

@wordles.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("wordles.wordle_detail", wordle_day=form.search_query.data))

    submissions = Wordle.objects()

    if len(submissions) == 0:
        fig = None
    else:
        fig = generate_figure(submissions)

    return render_template(
        "index.html", 
        form=form,
        todays_wordle=todays_wordle(),
        fig=fig
    )

@wordles.route("/submit", methods=["GET", "POST"])
@login_required
def submit_wordle():
    paste_form = WordlePasteForm()
    manual_form = WordleManualForm()
    user = User.objects(username=current_user.username).first()

    # pasted
    if paste_form.text.data and paste_form.validate_on_submit():
        text = paste_form.text.data
        data = parse_pasted_wordle(text)

        if data is not None:
            wordle = Wordle.objects(wordle_day=data["day"], user=user).first()

            if wordle is None:
                new_wordle = Wordle(
                    user=current_user._get_current_object(),
                    grid=data["grid"], 
                    date=current_time(), 
                    wordle_day=data["day"], 
                    guesses=data["guesses"]
                )
                new_wordle.save()
            else:
                wordle.modify(
                    grid=data["grid"], 
                    date=current_time(), 
                    wordle_day=data["day"], 
                    guesses=data["guesses"]
                )
                wordle.save()

            return redirect(url_for("wordles.submit_wordle"))
        else:
            flash("Invalid Wordle data!")
    
    # manual
    if manual_form.wordle_day.data and manual_form.guesses.data and manual_form.validate_on_submit():
        wordle = Wordle.objects(wordle_day=manual_form.wordle_day.data, user=user).first()

        if wordle is None:
            new_wordle = Wordle(
                user=current_user._get_current_object(),
                grid="No grid data",
                date=current_time(), 
                wordle_day=manual_form.wordle_day.data,
                guesses=manual_form.guesses.data
            )
            new_wordle.save()
        else:
            wordle.modify(
                grid="No grid data",
                date=current_time(), 
                wordle_day=manual_form.wordle_day.data,
                guesses=manual_form.guesses.data
            )
            wordle.save()
        
        return redirect(url_for("wordles.submit_wordle"))

    return render_template(
        "submit.html",
        paste_form=paste_form,
        manual_form=manual_form,
        title="Submit Wordle"
    )


@wordles.route("/wordle/<wordle_day>", methods=["GET"])
def wordle_detail(wordle_day):
    if int(wordle_day) < 1:
        abort(404)

    submissions = Wordle.objects(wordle_day=wordle_day)

    if len(submissions) == 0:
        fig = None
    else:
        fig = generate_figure(submissions)

    return render_template(
        "wordle_detail.html",
        wordle_day=wordle_day,
        submissions=submissions,
        fig=fig,
        title="Wordle " + wordle_day
    )


@wordles.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    submissions = Wordle.objects(user=user).order_by("-wordle_day")

    if len(submissions) == 0:
        fig = None
    else:
        fig = generate_figure(submissions)

    return render_template(
        "user_detail.html", 
        username=username,
        submissions=submissions,
        fig=fig,
        title=username + "\'s Profile"
    )

@wordles.route("/about")
def about():
    return render_template(
        "about.html",
        title="About Statdle"
    )