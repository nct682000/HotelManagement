import json, hashlib
from HotelApp.models import User, Room, Category, Receipt, ReceiptDetail
from HotelApp.admin import *
from flask import request

# Truy vấn loại phòng
def read_category():
    categories = Category.query
    return categories.all()

# Truy vấn phòng
def read_rooms(cate_id = None, empty = None, kw = None):

    rooms = Room.query.join(Category).add_columns(Category.price, Category.image, Category.name)
    if cate_id:
        rooms = rooms.filter(Room.catgory_id == cate_id)

    if empty:
        rooms = rooms.filter(Room.active == empty)

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    return rooms.group_by(Room.id).all()

# Lấy thông tin phòng thông qua id
def get_room_by_id(room_id):
    room = Room.query.join(Category,Room.catgory_id == Category.id)\
        .add_columns(Category.price, Category.image, Category.description).filter(Room.id == room_id)

    return room.all()[0]

# Thêm tài khoản
def add_user(name, username, password, email, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name=name,
                username=username,
                email = email,
                password = password,
                avatar = avatar)
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False

#
# def cart_update(cart):
#     total_amount, total_quantity = 0, 0
#     if cart:
#         for r in cart.values():
#             total_quantity = r['quantity']
#             total_amount = r['price']
#     return total_quantity, total_amount

# Hàm tính tổng tiền trong cart
def cart_stats(cart):
    sum, sum_total = 0, 0
    if cart:
        for r in cart.values():
            sum = sum + r["sum"]
            sum_total = sum_total + r["total"]

    return sum, sum_total

# Thêm hóa đơn - Chi tiết hóa đơn
def add_receipt(cart):
    if cart:
        sum_total = 0
        guest = ''
        phone = ''
        for r in list(cart.values()):
            sum_total += r['total']
            guest = r['guest']
            phone =r['phone']

        receipt = Receipt(customer_id=1, total=sum_total, guest = guest, phone = phone)
        db.session.add(receipt)

        for r in list(cart.values()):
            detail = ReceiptDetail(receipt=receipt,
                                   room_id=int(r["id"]),
                                   date = r["date"],
                                   quantity=r["quantity"],
                                   is_foreign = r["is_foreign"],
                                   price=r["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False

# Thay đổi trạng thái phòng thông qua id
def changeActive(room_id):
    room = Room.query.get(room_id)
    room.active = not room.active
    db.session.add(room)
    db.session.commit()

# Lấy thông tin của qui định
def getReg():
    reg = Regulations.query
    return reg.first()

