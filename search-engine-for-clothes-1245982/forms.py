from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    """ forms"""
    classification = SelectField('category',
        choices=[('Sweaters', 'Sweaters'), ('Denim', 'Denim'), ('Blazers', 'Blazers'), ('Pants', 'Pants'),('Shirts', 'Shirts'),('Blousers', 'Blousers')],
        render_kw={'class': 'form-control'})
    color = StringField(label='color', validators=[DataRequired("please type the color of the clothes")],
        description="please type the color of the clothes",
        render_kw={"required": "required", "class": "form-control"})
    brand = StringField(label='brand', validators=[DataRequired("please type the brand of the clothes")],
        description="please type the brand of the clothes",
        render_kw={"required": "required", "class": "form-control"})
    year_to_buy = StringField(label='year', validators=[DataRequired("please type the year of the clothes")],
        description="please type the year of the clothes",
        render_kw={"required": "required", "class": "form-control"})
    location = StringField(label='location', validators=[DataRequired("please type the location ")],
        description="please type the location of clothes in the wardrobe",
        render_kw={"required": "required", "class": "form-control"})
    image = StringField(label='image',
        description='please type the url',
        render_kw={'required': 'required', 'class': 'form-control'})
    description = TextAreaField(label='description', validators=[DataRequired("please type in the description for the clothes")],
        description="please type in the description for the clothes",
        render_kw={"required": "required", "class": "form-control"})
    submit = SubmitField('提交')
