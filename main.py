from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laba.db'
db = SQLAlchemy(app)
f = open('templates/1.txt', 'r')
total_steps = int(f.read())
f.close()


class Article(db.Model):
    steps = db.Column(db.Integer, default=0)
    date = db.Column(db.Text, default=datetime.utcnow)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    id = db.Column(db.Integer, nullable=False, primary_key=True)

    def __repr__(self):
        return '<Article %r>' % self.id
        

@app.route('/')
def main():
    global total_steps
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('main.html', articles=articles, total_steps=total_steps)


@app.route('/<int:id>/del')
def form_delete(id):
    global total_steps
    article = Article.query.get_or_404(id)

    try:
        total_steps -= int(article.steps)
        f = open('templates/1.txt', 'w')
        f.write(str(total_steps))
        f.close()
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error occured while adding form'


@app.route('/del_all')
def form_delete_all():
    global total_steps
    articles = Article.query.all()
    try:
        for el in articles:
            db.session.delete(el)
            db.session.commit()
        total_steps = 0
        f = open('templates/1.txt', 'w')
        f.write(str(total_steps))
        f.close()
        return redirect('/') 
    except:
        return 'Error occured while adding form'


@app.route('/form', methods=['POST', 'GET'])
def form():
    global total_steps
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        date = request.form['date']
        steps = request.form['steps']
        total_steps += int(steps)
        f = open('templates/1.txt', 'w')
        f.write(str(total_steps))
        f.close()
        article = Article(firstName=firstName, lastName=lastName, date=date, steps=steps)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error occured while adding form'
    else:
        return render_template('form.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
