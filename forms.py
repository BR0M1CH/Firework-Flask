from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, SelectMultipleField
import re
from wtforms.validators import DataRequired, StopValidation, EqualTo
import requests

api = 'http://restfastapi:8000'

###############################################################################################################################
##########################################       FORMS FOR ITEMS CRUD #########################################################
###############################################################################################################################

class MasterForm(FlaskForm):
    name = StringField('name', description='Название')
    description = StringField('description', description='Описание')
    price = IntegerField('price', description='Цена')
    tax = IntegerField('tax', default=0, description='Скидка в %')
    visits = IntegerField('visits', default=1, description='Количество посещений')
    sales = IntegerField('sales', default=1, description='Количество продаж')
    available = IntegerField('available', default=1, description='Количество на складе')
    visible = BooleanField('visible', default=True, description='Отображение')
    video = StringField('video', default='https://www.youtube.com/embed/', description='Ссылка на видео')

class AddSalute(MasterForm):
    picture = StringField('picture', default='/static/pictures/salutes/', description='Ссылка на картинку')
    shoots = IntegerField('shoots', description='Количество выстрелов')
    calibers = StringField('calibers', description='Калибры, через запятую')
    duration = IntegerField('duration', description='Длительность салюта')
    height = IntegerField('height', description='Высота')
    submit = SubmitField('Добавить', name='action', default='Add')

class AddBengal(MasterForm):
    picture = StringField('picture', default='/static/pictures/bengals/', description='Ссылка на картинку')
    length = IntegerField('length', description='Длина')
    colors = StringField('colors', description='Цвета (вводить так, как будет отображаться)')
    count = IntegerField('count', description='Комплектность')
    duration = IntegerField('duration', description='Продолжительность горения')
    submit = SubmitField('Добавить', name='action', default='Add')

class AddFountain(MasterForm):
    picture = StringField('picture', default='/static/pictures/fountains/', description='Ссылка на картинку')
    height = IntegerField('height', description='Высота')
    duration = IntegerField('duration', description='Продолжительность горения')
    submit = SubmitField('Добавить', name='action', default='Add')

class AddPetard(MasterForm):
    picture = StringField('picture', default='/static/pictures/petards/', description='Ссылка на картинку')
    count = IntegerField('count', description='За какое кол-во цена')
    packet = BooleanField('packer', description='Пачка (если не выбрано - штучно)')
    flight = BooleanField('flight', description='Взлетающая (если не выбано - наземная)')
    submit = SubmitField('Добавить', name='action', default='Add')

class RedactPetard(AddPetard):
    delete = SubmitField('Удалить', name='action', default='Delete')

class RedactSalute(AddSalute):
    delete = SubmitField('Удалить', name='action', default='Delete')

class RedactFountain(AddFountain):
    delete = SubmitField('Удалить', name='action', default='Delete')

class RedactBengal(AddBengal):
    delete = SubmitField('Удалить', name='action', default='Delete')

###############################################################################################################################
##########################################       FORMS FOR AUTH/REG   #########################################################
###############################################################################################################################



class UserNotInBase(object):        #for auth
    def __init__(self): self.message = 'Пользователь с таким телефоном не зарегистрирован'
    def __call__(self, form, field):
        print(requests.get(f'{api}/reg/{field.data}').json())
        if not requests.get(f'{api}/reg/{field.data}').json():
            raise StopValidation(self.message)
        
class UserInBase(object):           #for registration
    def __init__(self): self.message = 'Номер телефона уже зарегистрирован'
    def __call__(self, form, field):
        if requests.get(f'{api}/reg/{field.data}').json():
            raise StopValidation('Номер телефона уже зарегистрирован')
        
class PhoneValidate(object):
    def __init__(self): self.message= 'Введите номер телефона в формате 89xxxxxxxxx'
    def __call__(self, form, field):
        match = re.match(r'^89\d{9}$', str(field.data))
        if not match:
            raise StopValidation(self.message)
    

class AuthForm(FlaskForm):
    username = IntegerField("Username", validators=[DataRequired(), 
                                                   UserNotInBase(),
                                                   PhoneValidate()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Войти")


class RegForm(FlaskForm):
    username = IntegerField("Username", validators=[DataRequired(), 
                                                   UserInBase(),
                                                   PhoneValidate()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField('Repeat_Password', validators=[DataRequired(), 
                                                                   EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField("Зарегистрироваться")

###############################################################################################################################
##########################################       FORMS FOR FILTERS    #########################################################
###############################################################################################################################

