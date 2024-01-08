api = 'http://restfastapi:8000'
import requests
import json
from flask import request
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from filters import *
from forms import AddBengal, AddFountain, AddPetard, AddSalute, RedactBengal, RedactFountain, RedactPetard, RedactSalute
from pprint import pprint

class Item(object):

    api = 'http://restfastapi:8000'
    params_list = []
    params_list_int = []
    params_list_bool = []
    filter_list_attrs = []

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


class Salute(Item):
    ref_api = f"{api}/salutes/"
    params_list = ['name', 'calibers', 'description', 'picture', 'video']
    params_list_int = ['shoots', 'duration', 'height', 'price', 'tax', 'visits', 'sales', 'available']
    params_list_bool = ['visible']
    filter_list_attrs = ['shoots_filter', 'duration_filter', 'calibers_filter']
    group = 'salute'
    one = 'one/salute.html'
    filter = FilterSalut
    form = AddSalute
    red_form = RedactSalute

class Bengals(Item):
    ref_api = f"{api}/bengals/"
    params_list = ['name', 'colors', 'description', 'picture', 'video']
    params_list_int = ['length', 'count', 'duration', 'price', 'tax', 'visits', 'sales', 'available']
    params_list_bool = ['visible']
    filter_list_attrs = ['complection_filter', 'length_filter']
    group = 'bengal'
    one = 'one/bengal.html'
    filter = FilterBengal
    form = AddBengal
    red_form = RedactBengal


class Fountains(Item):
    ref_api = f"{api}/fountaines/"
    params_list = ['name', 'description', 'picture', 'video']
    params_list_int = ['height', 'duration', 'price', 'tax', 'visits', 'sales', 'available']
    params_list_bool = ['visible']
    filter_list_attrs = ['height_filter', 'duration_filter']
    group = 'fountain'
    one = 'one/fountaine.html'
    filter = FilterFountaine
    form = AddFountain
    red_form = RedactFountain
    
class Petards(Item):
    ref_api = f"{api}/petards/"
    params_list = ['name', 'description', 'picture', 'video']
    params_list_int = ['count', 'price', 'tax', 'visits', 'sales', 'available']
    params_list_bool = ['flight', 'packet', 'visible']
    filter_list_attrs = ['complection_filter', 'flight_filter']
    group='petard'
    one = 'one/petard.html'
    filter = FilterPetard
    form = AddPetard
    red_form = RedactPetard

class User(UserMixin):

    def __init__(self, new: bool=False, form=None, user_name=None):
        if new:
            if self.check_registration(form=form):
                self.id = form.username.data
                self.password = generate_password_hash(form.password.data)
                print("DATA FOR REG:", self.__dict__)
                self.post()
                self = None
        else:
            if form:
                user_name = form.username.data
                if not self.check_auth(form):
                    self.id=0
                    return
            self.__dict__ = requests.get(f"{api}/user/{user_name}").json()

    def check_registration(self, form):
        response = requests.get(f'{api}/reg/{form.username.data}').json()
        if response:
            return False
        else:
            return True       

    def check_auth(self, form):
        hashed = requests.get(f"{api}/password?id={form.username.data}")
        print(hashed.json())
        if check_password_hash(hashed.json(), form.password.data):
            print("check", True)
            return True
        else:
            print("check", False)
            return False
        
    def post(self):
        requests.post(f"{api}/reg", data=json.dumps(self.__dict__, indent=4))



    
