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


@app.route('/new_story.html')
def empty_user_story():
    return render_template('form.html')


@app.route('/story', methods=['POST'])
def add_user_story():
    new_user_story = UserStory.create(title=request.form["story title"],
                                      story=request.form["user story"], criteria=request.form["acceptance criteria"], value=request.form["business value"], estimation=request.form["estimation"], status=request.form["status"])
    new_user_story.save()
    flash('New User Story successfully added')
    return redirect(url_for('show_user_stories'))

if __name__ == "__main__":
    init_db()
    app.run()
