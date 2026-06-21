from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import UserBadge, UserXP
from services.community import create_answer, create_post, get_post_detail, get_recent_posts, upvote_answer
from student_routes import student_required


community_bp = Blueprint("community", __name__, url_prefix="/community")


@community_bp.route("")
@student_required
def community_home():
    posts = get_recent_posts()
    xp_profile = UserXP.query.filter_by(user_id=session["user_id"]).first()
    badges = UserBadge.query.filter_by(user_id=session["user_id"]).order_by(UserBadge.awarded_at.desc()).all()
    return render_template(
        "community/community_home.html",
        posts=posts,
        xp_profile=xp_profile,
        badges=badges,
    )


@community_bp.route("/post", methods=["GET", "POST"])
@student_required
def post_question():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        if not title or not content:
            flash("Please enter both a title and content for your community post.", "warning")
            return redirect(url_for("community.post_question"))
        post = create_post(session["user_id"], title, content)
        return redirect(url_for("community.question_page", id=post.id))

    return render_template("community/post_question.html")


@community_bp.route("/question/<int:id>")
@student_required
def question_page(id):
    detail = get_post_detail(id)
    return render_template(
        "community/question_page.html",
        post=detail["post"],
        answers=detail["answers"],
    )


@community_bp.route("/answer", methods=["POST"])
@student_required
def answer_question():
    post_id = request.form.get("post_id", type=int)
    answer_text = (request.form.get("answer_text") or "").strip()
    if not post_id or not answer_text:
        flash("Please provide an answer before submitting.", "warning")
        return redirect(url_for("community.community_home"))
    create_answer(post_id, session["user_id"], answer_text)
    return redirect(url_for("community.question_page", id=post_id))


@community_bp.route("/upvote/<int:answer_id>", methods=["POST"])
@student_required
def upvote(answer_id):
    answer = upvote_answer(answer_id)
    return redirect(url_for("community.question_page", id=answer.post_id))
