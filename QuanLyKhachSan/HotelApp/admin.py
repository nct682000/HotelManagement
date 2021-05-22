from urllib import response

from HotelApp import admin, db, utils
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from HotelApp.models import Category, Room, User, Receipt, ReceiptDetail, Regulations
from flask_login import current_user,logout_user
from flask import redirect, request


class Logout(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class Login(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/login.html')

    def is_accessible(self):
        return not current_user.is_authenticated


# Chỉ dành cho user là ADMIN
class ModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin == True


class Register(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/register.html')


class BaseView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated

class CheckIn(BaseView):
    @expose('/')
    def index(self):
        rooms = utils.read_rooms()
        return self.render('admin/checkin.html', rooms=rooms)

class ECheckIn(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/e-checkin.html')

class CheckOut(BaseView):
    @expose('/')
    def index(self):
        rooms = utils.read_rooms()
        return self.render('admin/checkout.html', rooms = rooms)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Receipt, db.session))
admin.add_view(ModelView(ReceiptDetail, db.session))
admin.add_view(ModelView(Regulations, db.session))
admin.add_view(CheckIn(name=None))
admin.add_view(ECheckIn(name=None))
admin.add_view(CheckOut(name=None))
admin.add_view(Register(name=None))
admin.add_view(Login(name=None))
admin.add_view(Logout(name=None))