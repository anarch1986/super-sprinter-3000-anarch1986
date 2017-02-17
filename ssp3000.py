from models import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

DEBUG = True

app = Flask(__name__, static_url_path="/templates", static_folder="templates")
app.config.from_object(__name__)


def init_db():
    db = CreateDatabase.create_db_object()
    try:
        db.connect()
        db.create_tables([UserStory], safe=True)
        print("Database connection established.")
    except:
        print("Can't connect to database.\nPlease check your connection.txt file.")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
@app.route('/list')
def show_user_stories():
    user_stories = UserStory.select().order_by(UserStory.id.asc())
    return render_template('list.html', stories=user_stories)


@app.route('/story')
def empty_user_story():
    return render_template('form.html', story=None)


@app.route('/new_story', methods=['POST'])
def add_user_story():
    new_user_story = UserStory.create(title=request.form["story title"],
                                      story=request.form["user story"], criteria=request.form[
                                          "acceptance criteria"],
                                      value=request.form[
                                          "business value"], estimation=request.form["estimation"],
                                      status=request.form["status"])
    new_user_story.save()
    return redirect(url_for('show_user_stories'))


@app.route('/story/<story_id>', methods=['POST'])
def get_user_story(story_id):
    story_id = request.form["id_for_update"]
    selected_story = UserStory.get(UserStory.id == story_id)
    return render_template('form.html', story=selected_story)


@app.route('/update', methods=['POST'])
def update_user_story():
    story_for_update = UserStory.update(title=request.form["story title"],
                                        story=request.form["user story"], criteria=request.form[
                                            "acceptance criteria"],
                                        value=request.form[
                                            "business value"], estimation=request.form["estimation"],
                                        status=request.form["status"]).where(UserStory.id == request.form["id"])
    story_for_update.execute()
    return redirect(url_for('show_user_stories'))


@app.route('/delete', methods=['POST'])
def delete_user_story():
    story_id = request.form["id_for_delete"]
    selected_story = UserStory.get(UserStory.id == story_id)
    selected_story.delete_instance()
    return redirect(url_for('show_user_stories'))

if __name__ == "__main__":
    init_db()
    app.run()
