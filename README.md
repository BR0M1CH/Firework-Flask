# I: main.py

Файл main.py представляет ключевую реализацию рендеринга страниц, маршрутизации и инициализации самого приложения.

Для описания всех "товаров" существует файл *items.py*, к которому вернемся позже. Базово все большинство действий с объектами на самом высоком уровне описаны в двух функциях: *item()* и *items()*

Функция *item()*:
```
ref = f"{Class.ref_api}{request.args.get('id')}"
    form = Class.red_form()
    if request.method == 'GET':
        response = requests.get(ref)
    elif request.method == 'POST':
        if request.form['action']=='Add':
            item = Class({'id': request.args.get('id')}) # Create item with only 1 param: id
            item.parse(request)
            response = requests.put(ref, data=item.params_to_json())
            response = requests.get(ref)
        elif request.form['action']=='Delete':
            response = requests.delete(ref)
            return redirect(url_for(f"/{Class.group}s"))
    response = response.json()
    print(response)
    item = Class(response.pop(0))
    return render_template(Class.one, items=response, item=item, header=item.name, form=form)
```

Служит для описания действий над одним предметом (товаром) и используется тогда, когда пользователь перешел на страницу товара. Определяется метод запроса, если это *GET*, то функция отправит запрос микросервису на FastAPI, который подтянет с MongoDB все данные о конкретном товаре, если же запрос *POST*, то функция выяснит какое действие совершается: Редактирование или Удаление товара **(To-do: добавить добавление в корзину)**.
В зависимости от действия отправляется put или delete запрос в тот же FastAPI, который является "распределительным центром" всей системы.

![Пример отрисовки страницы товара](https://i.yapx.ru/W9Njq.png "Страница с салютом")

Функция *items()*:
```
def items(Class, header, request):
    form = Class.form()
    filters = Class.filter()
    if request.method=='GET':
        response = requests.get(url=Class.ref_api)
    if request.method=='POST':
        if request.form['action']=='Add':
            if form.validate_on_submit():
                item = Class()
                item.parse(request)
                response = requests.post(Class.ref_api, data=item.params_to_json())
        elif request.form['action']=='Filter':
            print('CATCHED')
            filters_dict = Class.parse_filter(request)
            response = Class.send_filter(filters_dict)
            print(response.json())
    response = response.json()
    return render_template('many/catalog_filters.html', form=form, response=response, header=header, filters=filters)
```

Служит для отображения списка товаров конкретной категории. Если *GET*-запрос происходит забор данных с базы через FastAPI, если *POST* - одно из двух действий:
1. Фильтрация
2. Добавление товара

В зависимости от выбранного действия отправляется запрос по соответствующему адресу.

![Пример отрисовки страницы товаров](https://i.yapx.ru/W9Nv4.png)

Так же в файле *main.py* представлены маршруты к списку товаров и самим товарам, которые и вызывают одну из двух функций: *item()* или *items()* и маршруты авторизации, в которых нет явно прописанной логики валидации данных, она написана в файле *forms.py*

# II: forms.py

Файл *forms.py* служит для описания базовых форм для реализации CRUD методов для работы с товарами, так же в нем дополнительно внесены две формы для регистрации и авторизации.

1. Формы для работы с товарами:

    Создаётся одна мастер-форма, которая описывает все поля (характеристики) присущие каждому товару:

    ```
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
    ```

    Список параметров для примера: название, описание, цена, скидка, видео и прочие х-ки.

    От этой мастер-формы будут наследоваться все дальнейшие формы для каждой категории товаров, ведь у них разные параметры: у салютов к примеру - количество залпов, у бенгальских огней - длина и т.д. и т.п.

    ```
    class AddSalute(MasterForm):
    picture = StringField('picture', default='/static/pictures/salutes/', description='Ссылка на картинку')

    shoots = IntegerField('shoots', description='Количество выстрелов')

    calibers = StringField('calibers', description='Калибры, через запятую')

    duration = IntegerField('duration', description='Длительность салюта')

    height = IntegerField('height', description='Высота')

    submit = SubmitField('Добавить', name='action', default='Add')
    ```

    В конечном счете каждая форма будет содержать ряд параметров и кнопку *Добавить*. Но требуется большее: отображение кнопки Добавить в каталоге и отображение кнопок Редактировать и Удалить на странице товара. Для этого от этих классов форм унаследуется еще один класс, в который просто добавиться одно поле: удалить:
    ```
    #Да с названием плохо получилось, но уже не успеваю переделать
    class RedactSalute(AddSalute):
    delete = SubmitField('Удалить', name='action', default='Delete')
    ```

    Таким образом формы Add и Redact представляют собой почти одно и то же, лишь с неболльшой разницей, описанной выше. (Создание нового класса с наследованием требуется по следующим причинам:
    1. В HTML формы отрисовываются циклом, а не поэтапно
    2. В обработке форм проще циклом пройтись по форме, нежели забирать данные вручную по каждому ключу)

2. Формы авторизации:

    Авторизация
    ```
    class AuthForm(FlaskForm):
    username = IntegerField("Username", validators=[DataRequired(), UserNotInBase(), PhoneValidate()])

    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember Me")

    submit = SubmitField("Войти")
    ```
    
    Регистрация
    ```
    class RegForm(FlaskForm):
    username = IntegerField("Username", validators=[DataRequired(), UserInBase(), PhoneValidate()])

    password = PasswordField("Password", validators=[DataRequired()])

    repeat_password = PasswordField('Repeat_Password', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])

    submit = SubmitField("Зарегистрироваться")
    ```

    Из особенностей в некоторых полях указаны самописные валидаторы, которые не дадут отправить некорректные данные

3. Валидаторы

    ```
    class UserNotInBase(object):        #for auth

    def __init__(self): 
    self.message = 'Пользователь с таким телефоном не зарегистрирован'

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
    ```

    Принцип работы валидатора основан на dunder-методе __call__, логика проста - описывать нет смысла

# III: filters.py

Фильтры представляют собой обычные классы, с наследованием от FlaskForm, единственная особенность, на которую стоит обратить внимание - для удобной отрисовки тем же циклом сделаны следующие шаги:

    1. Минимальная и максимальная цена - отдельные числовые поля, их отрисовка идет отдельно
    2. Все остальные характеристики "засунуты" в SelectMultipleField, в котором описано поведение при отрисовке: каждая опция Select`а будет представлять собой чекбокс

Таким образом удалось достичь универсальности шаблона: для любого товара справедлива отрисовка вида:

    |Минимальная цена| |Максимальная цена|
    |Все характеристики (чекбокс поля)|
    |Кнопка отфильтровать|

Пример фильтра бенгальских свечей:
```
class FilterBengal(FlaskForm):
    #Да, криво перевел комплектацию

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
    
    submit = SubmitField('Показать', name='action', default='Filter')
```

# IV: items.py - итог

Если файл *main.py* был центром принятия решений в рамках данного приложение - файл *items.py* будет все решения реализовывать. В этом файле описаны сущности (товары), пользователи и их правила поведения.

Создаётся мастер-класс Item, который соберет в себя все методы, которые буду использовать другие классы:
```
class Item(object):

    api = 'http://restfastapi:8000' #ссылка на контейнер с FastAPI
    params_list = []    #Личный для каждого класса список параметров (строчных)
    params_list_int = [] #По аналогии с предыдущим
    params_list_bool = [] #По аналогии с предыдущими
    filter_list_attrs = [] #Личный для каждого класса список параметров фильтрации

    def __init__(self, params=None):
        if not params:
            response = requests.get(f'{self.__class__.ref_api}param/?param=id').content
            self.id = response+1
        else:
            self.set_params(params)

    def parse(self, request: request):
        for param in self.params_list:
            setattr(self, param, request.form.get(param))
        for param in self.params_list_int:
            setattr(self, param, int(request.form.get(param)))
        for param in self.params_list_bool:
            setattr(self, param, bool(request.form.get(param)))

    def params(self):
        return self.__dict__

    def params_to_json(self):
        return json.dumps(self.__dict__, indent=4)
    
    def set_params(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)
        self.group=self.__class__.group

    @classmethod
    def parse_filter(cls, request: request):
        filter_dict = {}
        min_price = request.form.get('min_price_filter')
        max_price = request.form.get('max_price_filter')
        if not min_price:
            filter_dict['min_price_filter'] = 0
        else:
            filter_dict['min_price_filter'] = int(min_price)
        if not max_price:
            filter_dict['max_price_filter'] = 1_000_000
        else:
            filter_dict['max_price_filter']= int(max_price)
        for param in cls.filter_list_attrs:
            filter_dict[param] = request.form.getlist(param)
            # if request.form.getlist(param) != []:
            #     filter_dict[param] = request.form.getlist(param)
            # else:
            #     filter_dict[param] = -1
        return filter_dict
    
    @classmethod
    def send_filter(cls, params):
        ref = f"{cls.ref_api}filtered/"
        pprint(params)
        response = requests.post(ref, data=json.dumps(params, indent=4))
        return response
```

* Метод init отвечает за инициализацию объектов и имеет два варианта поведения:
        Если были переданы какие-то параметры - значит объект не новый - не нужно делать запрос к БД с целью присвоения новому объекту уникального ID, просто присваиваются параметры с помощью метода set_params. Если же параметры не были переданы - делается запрос, присвивается ID.


* Метод parse проходит циклом по всем трем группам параметров и забирает из формы данные, введенные для редактирования или добавления товара.

* Метод parse_filter делает то же самое, только меняет None-данные на корректные, например, если не была введена максимальная цена, которой нужно ограничить выборку каталога - пусть она будет равна 1000000. 

* Метод send_filter отправит данные о фильтрации в FastAPI.

Важно: send_filter и parse_filter являются методами класса, для их успешной работы не нужно создавать объект класса, они не зависят от объектов. 

После описание мастер-класса можно приступить к описание дочерних классов, пример класса:
```

class Salute(Item):
    ref_api = f"{api}/salutes/"

    params_list = ['name', 'calibers', 'description', 'picture', 'video']

    params_list_int = ['shoots', 'duration', 'height', 'price', 'tax', 'visits', 'sales', 'available']

    params_list_bool = ['visible']

    filter_list_attrs = ['shoots_filter', 'duration_filter', 'calibers_filter']

    group = 'salute'

    one = 'one/salute.html' #адрес страницы товара

    filter = FilterSalut

    form = AddSalute

    red_form = RedactSalute
```

Если абстрагироваться от наследования - можно сказать, что это просто ДатаКласс, потому что сами классы хранят только уникальные данные о себе, все методы прописаны в родительском классе и являются универсальными для любых дочерних классов. 

Класс пользователя описывать не стоит, в нем описаны процессы выбора действия: регистрация или авторизация и проверка пароля и уникальности пользователя

# V: Подведение итогов

В построении приложения (на мой взгляд) удалось достичь выполнения таких важных принципов как: чистота кода, неповторяемость кода, универсальность, что позволяет с легкостью масштабировать приложение, добавляя новые категории товаров. 

Контейнер прилагается
