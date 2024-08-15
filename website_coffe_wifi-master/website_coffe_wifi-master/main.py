from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

#Create Data Base
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create Table

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(60), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("index.html", cafes=cafes)

@app.route("/coffee/delete/<int:cafe_id>")
def delete_coffee(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    
    db.session.delete(cafe)
    db.session.commit()
    
    return redirect(url_for('home'))

@app.route("/coffee/add", methods=['POST'])
def add_cafe():
    
    if request.method == 'POST':
        
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            img_url=request.form.get('img_url'),
            location=request.form.get('location'),
            seats=request.form.get('seats'),
            has_toilet=request.form.get('has_toilet') == 'true',
            has_wifi=request.form.get('has_wifi') == 'true',
            has_sockets=request.form.get('has_sockets') == 'true',
            can_take_calls=request.form.get('can_take_calls') == 'true',
            coffee_price=request.form.get('coffee_price')
        )
        
        db.session.add(new_cafe)
        db.session.commit()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
