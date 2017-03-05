from models import *
from flask import Flask, request, g, redirect, url_for, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True, SECRET_KEY='any_random_string'))


def init_db():
    db = CreateDatabase.create_db_object()
    db.connect()
    db.create_tables([Userstories], safe=True)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'dry'):
        g.postgre_db.close()


@app.route('/')
def show_entries():
    stories = Userstories.select().order_by(Userstories.id.asc())

    return render_template('list.html', stories=stories)


@app.route('/empty_story')
def empty_user_story():
    return render_template('form.html', story=None)


@app.route('/add_user_story', methods=['POST'])
def add_user_story():
    new_entry = Userstories.create(story_title=request.form['story_title'],
                                   user_story=request.form['user_story'],
                                   acceptance_criteria=request.form['acceptance_criteria'],
                                   business_value=request.form['business_value'],
                                   estimation=request.form['estimation'],
                                   status=request.form['status'])
    new_entry.save()
    return redirect('/')


@app.route('/story/<int:story_id>', methods=['GET'])
def get_story_for_edit(story_id):
    story = Userstories.select().where(Userstories.id == story_id).get()
    return render_template('form.html', story=story)


@app.route('/story/<int:story_id>', methods=['POST'])
def edit_user_story(story_id):
    story_for_update = Userstories.update(story_title=request.form['story_title'],
                                          user_story=request.form['user_story'],
                                          acceptance_criteria=request.form['acceptance_criteria'],
                                          business_value=request.form['business_value'],
                                          estimation=request.form['estimation'],
                                          status=request.form['status']).where(Userstories.id == story_id)
    story_for_update.execute()
    return redirect('/')


@app.route('/delete/<int:story_id>')
def delete_user_story(story_id):
    story = Userstories.get(Userstories.id == story_id)
    story.delete_instance()

    return redirect('/')


if __name__ == "__main__":
    init_db()
    app.run()
