from models import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

DATABASE = "tomi.db"
DEBUG = True
SECRET_KEY = "Irjabeapint"

app = Flask(__name__, static_url_path="/templates", static_folder="templates")
app.config.from_object(__name__)
db = CreateDatabase.create_db_object()


def init_db():
    db = CreateDatabase.create_db_object()
    try:
        db.connect()
        db.create_tables([UserStory], safe=True)
        print("Database connection established.")
    except:
        print("Can't connect to database.\nPlease check your database_data.txt file.")


@app.cli.command('initdb')
def initdb_command():
    init_db()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
@app.route('/list.html')
def show_user_stories():
    user_stories = UserStory.select().order_by(UserStory.id.asc())
    return render_template('list.html', stories=user_stories)


@app.route('/', methods=['POST'])
@app.route('/list.html', methods=['POST'])
def delete_user_story():
    story_id = request.form["id_for_delete"]
    selected_story = UserStory.get(UserStory.id == story_id)
    selected_story.delete_instance()
    return redirect(url_for('show_user_stories'))


@app.route('/update.html', methods=['POST'])
def get_user_story():
    story_id = request.form["id_for_update"]
    selected_story = UserStory.get(UserStory.id == story_id)
    return render_template('update_story.html', story=selected_story)


@app.route('/proceed_update.html', methods=['POST'])
def update_user_story():
    story_for_update = UserStory.update(title=request.form["story title"],
                                        story=request.form["user story"], criteria=request.form[
                                            "acceptance criteria"],
                                        value=request.form[
                                            "business value"], estimation=request.form["estimation"],
                                        status=request.form["status"]).where(UserStory.id == request.form["id"])
    story_for_update.execute()
    return redirect(url_for('show_user_stories'))


@app.route('/story.html')
def empty_user_story():
    return render_template('new_story.html')


@app.route('/story.html', methods=['POST'])
def add_user_story():
    new_user_story = UserStory.create(title=request.form["story title"],
                                      story=request.form["user story"], criteria=request.form[
                                          "acceptance criteria"],
                                      value=request.form[
                                          "business value"], estimation=request.form["estimation"],
                                      status=request.form["status"])
    new_user_story.save()
    return redirect(url_for('show_user_stories'))


if __name__ == "__main__":
    init_db()
    app.run()
