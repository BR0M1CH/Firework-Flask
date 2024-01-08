from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, SelectMultipleField
import requests
from wtforms.widgets import ListWidget, CheckboxInput, TableWidget

api = 'http://restfastapi:8000'


class FilterSalut(FlaskForm):
    min_price_filter = IntegerField('min_price_filter', description=0)
    max_price_filter = IntegerField('max_price_filter', description=int(requests.get(f"{api}/salutes/param/?param=price").content))

    shoots_filter = SelectMultipleField('Количество выстрелов', 
                                 choices=[('1', 'до 16'), ('2', '16-25'), ('3', '25-36'), ('4', '36-50'), ('5', '50-100'), ('6', '100-200'), ('7', 'более 200')], 
                                 coerce=int, 
                                 option_widget=CheckboxInput(),
                                 name = 'shoots_filter')
    duration_filter = SelectMultipleField('Длительность', 
                                   choices=[('1', 'до 20c'), ('2', '20c - 40c'), ('3', '40c - 60c'), ('4', '60c - 90c'), ('5', 'более 90с')], 
                                   widget=TableWidget(), 
                                   option_widget=CheckboxInput(),
                                   name = 'duration_filter')
    calibers_filter = SelectMultipleField('Калибр', 
                                   choices=[(0.8, '0.8"'), (1.0, '1.0"'), (1.1, '1.1"'), (1.25, '1.25"'), (1.5, '1.5"'), (2.0, '2.0"')], 
                                   widget=TableWidget(), 
                                   option_widget=CheckboxInput(),
                                   name = 'calibers_filter')
    submit = SubmitField(label='Показать', name='action')
    

class FilterPetard(FlaskForm):
    min_price_filter = IntegerField('min_price_filter', description=0)
    max_price_filter = IntegerField('max_price_filter', description=int(requests.get(f"{api}/petards/param/?param=price").content))

    flight_filter = SelectMultipleField('Взлетающая', 
                                 choices=[('1', 'Взлетающая'), ('0', 'Наземная')], 
                                 coerce=int, 
                                 option_widget=CheckboxInput(),
                                 name = 'flight_filter')
    complection_filter = SelectMultipleField('Комплектация', 
                                   choices=[('1', '1 шт'), ("4", '4 шт'), ('6', '6 шт'), ('12', '12 шт'), ('20', "больше 20 шт")], 
                                   widget=TableWidget(), 
                                   option_widget=CheckboxInput(),
                                   name = 'complection_filter')
    submit = SubmitField('Показать', name='action')


class FilterFountaine(FlaskForm):
    min_price_filter = IntegerField('min_price_filter', description=0)
    max_price_filter = IntegerField('max_price_filter', description=int(requests.get(f"{api}/fountaines/param/?param=price").content))

    height_filter = SelectMultipleField('Высота', 
                                 choices=[('2', '~ 2м'), ('3', '~ 3м'), ('4', '~ 4м')], 
                                 coerce=int, 
                                 option_widget=CheckboxInput(),
                                 name = 'height_filter')
    duration_filter = SelectMultipleField('Длительность', 
                                   choices=[('1', 'До 40 с'), ('2', '40c - 60c'), ('3', '60c - 80c'), ('4', "более 80 с")], 
                                   widget=TableWidget(), 
                                   option_widget=CheckboxInput(),
                                   name = 'duration_filter')
    submit = SubmitField('Показать', name='action')
    

class FilterBengal(FlaskForm):
    min_price_filter = IntegerField('min_price_filter', description=0)
    max_price_filter = IntegerField('max_price_filter', description=int(requests.get(f"{api}/bengals/param/?param=price").content))

    complection_filter = SelectMultipleField('Комплектация', 
                                 choices=[('2', '2 шт'), ('3', '3 шт'), ('4', '4 шт'), ('6', '6 шт')], 
                                 coerce=int, 
                                 option_widget=CheckboxInput(),
                                name = 'complection_filter')
    length_filter = SelectMultipleField('Длина', 
                                choices=[('200', '200 мм'), ('300', '300 мм'), ('400', '400 мм'), ('650', '650 мм')], 
                                coerce=int, 
                                option_widget=CheckboxInput(),
                                name = 'length_filter')
    submit = SubmitField('Показать', name='action')