from flask import Flask, render_template, url_for,session, redirect, flash, request
import requests
from items import Salute, Bengals, Fountains, Petards, User
from pprint import pprint
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from forms import AuthForm, RegForm


app = Flask(__name__)
api = 'http://restfastapi:8000'
app.secret_key='sw283phz3mf4384f34hfjp390mh4fmzfa00z39mfz8934h8fj3f43fffwdf'
loging_manager = LoginManager()
loging_manager.init_app(app)

@loging_manager.user_loader          
def load_user(user_name):
    user = User(new=False, user_name=user_name)
    print("dict:", user.__dict__)
    return user

##################################################################################################################################
###########################            DEFAULT DEFS            ###################################################################
##################################################################################################################################


def items(Class, header, request):
    form = Class.form()
    filters = Class.filter()
    if request.method=='GET':
        response = requests.get(url=Class.ref_api)
    if request.method=='POST':
        if request.form['action']=='Добавить':
            if form.validate_on_submit():
                item = Class()
                item.parse(request)
                response = requests.post(Class.ref_api, data=item.params_to_json())
        elif request.form['action']=='Показать':
            print('CATCHED')
            filters_dict = Class.parse_filter(request)
            response = Class.send_filter(filters_dict)
            print(response.json())
    response = response.json()
    return render_template('many/catalog_filters.html', form=form, response=response, header=header, filters=filters)


def item(Class, request):
    ref = f"{Class.ref_api}{request.args.get('id')}"
    form = Class.red_form()
    if request.method == 'GET':
        response = requests.get(ref)
    elif request.method == 'POST':
        if request.form['action']=='Добавить':
            item = Class({'id': request.args.get('id')}) # Create item with only 1 param: id
            item.parse(request)
            response = requests.put(ref, data=item.params_to_json())
            response = requests.get(ref)
        elif request.form['action']=='Удалить':
            response = requests.delete(ref)
            return redirect(url_for(f"/{Class.group}s"))
    response = response.json()
    print(response)
    item = Class(response.pop(0))
    return render_template(Class.one, items=response, item=item, header=item.name, form=form)



##################################################################################################################################
#################################            ROUTES            ###################################################################
##################################################################################################################################

@app.route('/')
@app.route('/main')
def main():
    return(render_template('main.html'))

@app.route('/colors/')
def colors():
    return(render_template('colors.html'))

#########################################################################################
##                         REG/AUTH                                                   ##
#########################################################################################
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(new=True, form=form)
            if user:
                flash("Регистрация прошла успешно!", 'info')
                return redirect(url_for('auth'))
            flash("Неправильный логин или пароль", 'error')
    return render_template('registration.html', form=form, header='Регистрация')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    form = AuthForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(new=False, form=form)
            print("USER:", user.__dict__)
            print(user)
            if user.id:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main'))
            flash("Неправильный логин или пароль", 'error')
    return render_template('auth.html', form=form, header='Вход')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


#########################################################################################
##                         SALUTES                                                     ##
#########################################################################################
@app.route('/salutes/', methods=['GET', 'POST'])
def salutes():
    return items(Class=Salute, header='Салюты', request=request)

@app.route('/salutes/salute', methods=['GET', 'POST'])
def salute():
    return item(Class=Salute, request=request)


#########################################################################################
##                         BENGALS                                                     ##
#########################################################################################
@app.route('/bengals/', methods=['GET', 'POST'])
def bengals():
    return items(Class=Bengals, header='Бенгальские свечи', request=request)

@app.route('/bengals/bengal', methods=['GET', 'POST'])
def bengal():
    return item(Class=Bengals, request=request)


#########################################################################################
##                         FOUNTAINS                                                   ##
#########################################################################################
@app.route('/fountains/', methods=['GET', 'POST'])
def fountains():
    return items(Class=Fountains, header='Фонтаны', request=request)

@app.route('/fountains/fountain', methods=['GET', 'POST'])
def fountain():
    return item(Class=Fountains, request=request)


#########################################################################################
##                         PETARDS                                                     ##
#########################################################################################
@app.route('/petards/', methods=['GET', 'POST'])
def petards():
    return items(Class=Petards, header='Петарды', request=request)

@app.route('/petards/petard', methods=['GET', 'POST'])
def petard():
    return item(Class=Petards, request=request)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)