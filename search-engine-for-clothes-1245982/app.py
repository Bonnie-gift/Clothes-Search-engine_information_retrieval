from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy
from forms import NewsForm
from tfidf import calculate_tfidf as Searching

#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:@localhost:3306/wardrobe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'a random string'

app.config.from_object('config')
db = SQLAlchemy(app)

class wardrobe(db.Model):
    """ 新闻模型 """
    __tablename__ = 'private_wardrobe_for_bonnie'
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.Enum('Sweaters', 'Denim', 'Blazers', 'Pants','Shirts','Blousers'))
    color = db.Column(db.String(200), nullable=False)
    brand= db.Column(db.String(200), nullable=False)
    year_to_buy = db.Column(db.String(4),nullable=False)
    location= db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(300),nullable=False)
    description = db.Column(db.String(300),nullable=False)
    tf_idf=db.Column(db.String(300),nullable=True)
    def __repr__(self):
        return '<Wardrobe %r>' % self.classification

@app.route('/detail/<int:pk>/')
def detail(pk):
    """ 新闻详情页 """
    new_obj = wardrobe.query.get(pk)
    return new_obj.classification

@app.route('/search_results')
def searchresults():
    """ 新闻首页 """
    keyword = request.args.get('search')
    keywordL=keyword.split(' ', 1 )
    color=keywordL[0]
    classification=keywordL[1]

    #query = wardrobe.query.all()
    query = wardrobe.query \
    .filter_by(color=color, classification=classification) \
    .all()
    search_results = []
        
    for doc in query:
        search_results.append(doc)
    return render_template('search_results.html',
                                search_results=search_results
                                )

@app.route('/recommend_results/<int:id>/')
def recommend_results(id):
    Searching.get_result(id)
    query = wardrobe.query.all()
    search_results = []
    for doc in query:
        search_results.append(doc)
    return render_template('search_results.html',
                                search_results=search_results
                                )
    
#'/'
@app.route('/')
def index():
     return render_template('search.html')

#'admin'
@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
    """ 后台管理首页 """
    if page is None:
        page = 1
    page_data = News.query.paginate(page=page, per_page=4)
    return render_template("admin/index.html", page_data=page_data)

# 增加记录
@app.route('/admin/add/', methods=['GET', 'POST'])
def add():
    """ add record """
    form = NewsForm()
    if form.validate_on_submit():
        print('error')
        n1 = wardrobe(
             classification = form.classification.data,
             color = form.color.data,
             brand= form.brand.data,
             year_to_buy = form.year_to_buy.data,
             location= form.location.data,
             image = form.image.data,
             description =form.description.data,
             tf_idf='0'
            )
        db.session.add(n1)
        db.session.commit()
        flash("success")
        return redirect(url_for('add'))
    return render_template("admin/add.html", form=form)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])