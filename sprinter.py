from models import *
from flask import Flask, request, g, redirect, url_for, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)


def init_db():
    db = CreateDatabase.create_db_object()
    db.connect()
    db.create_tables([Entries], safe=True)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
def show_entries():
    entries_query = Entries.select().order_by(Entries.id)
    return render_template('list.html', user_entries=entries_query)


@app.route('/story')
def empty_user_story():
    return render_template('form.html', story=None)


@app.route('/add_user_story', methods=['POST'])
def add_user_story():
    new_user_story = Entries.create(story_title=request.form["story-title"],
                                    user_story=request.form["user-story"],
                                    acceptance_criteria=request.form["acceptance-criteria"],
                                    business_value=request.form["business-value"],
                                    estimation=request.form["estimation"],
                                    status=request.form["status"])
    new_user_story.save()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_user_story():
    story_id = request.form["id_for_delete"]
    selected_story = Entries.get(Entries.id == story_id)
    selected_story.delete_instance()
    return redirect('/')







@app.route('/story/<story_id>', methods=['POST'])
def get_user_story(story_id):
    story_id = request.form["id_for_update"]
    selected_story = Entries.get(Entries.id == story_id)
    return render_template('form.html', story=selected_story)


@app.route('/update', methods=['POST'])
def update_user_story():
    story_for_update = Entries.update(title=request.form["story-title"],
                                        story=request.form["user-story"],
                                        criteria=request.form["acceptance-criteria"],
                                        value=request.form["business-value"],
                                        estimation=request.form["estimation"],
                                        status=request.form["status"]).where(Entries.id == request.form["id"])
    story_for_update.execute()
    return redirect('/')





if __name__ == "__main__":
    init_db()
    app.run()
