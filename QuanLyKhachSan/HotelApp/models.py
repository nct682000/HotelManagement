from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from HotelApp import db
from flask_login import UserMixin
from flask_login import current_user
from enum import Enum as UserEnum
from datetime import datetime


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

# class UserRole(UserEnum):
#     USER = 1
#     ADMIN = 2


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50),nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100))
    avatar = Column(String(100))
# Cờ để phân biệt user thường và ADMIN
    is_admin = Column(Boolean, default=False)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name

    def is_accessible(self):
        return current_user.is_authenticated

class Category(Base):
    __tablename__ = 'category'

    rooms = relationship('Room',
                            backref='category', lazy=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    description = Column(String(255))

class Room(Base):
    __tablename__ = 'room'
    active = Column(Boolean, default=False)
    catgory_id = Column(Integer, ForeignKey(Category.id),
                        nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='room', lazy=True)

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    guest = Column(String(50))
    phone = Column(String(20))
    total = Column(Float, default=0)
    details = relationship('ReceiptDetail',
                           backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    price = Column(Integer, default=0)
    date = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    is_foreign = Column(Boolean, default=False)


class Regulations(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    sercharse = Column(Float, default = 0.25)
    increase = Column(Float, default = 1.5)
    max = Column(Integer, default = 3)


if __name__ == '__main__':
    db.create_all()