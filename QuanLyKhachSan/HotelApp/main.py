from flask import render_template, redirect, request, session, jsonify
from HotelApp import app, utils, login, decorator
from HotelApp.admin import *
from HotelApp.models import *
from flask_login import login_user, login_required
import hashlib, os, json
from datetime import datetime

# Trang Client
@app.route('/')
def index():
    category = utils.read_category()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    empty = request.args.get('active')
    rooms = utils.read_rooms(cate_id = cate_id, kw = kw, empty = empty)

    return render_template('index.html', rooms = rooms,
                           category = category)

# Trang chi tiết phòng
@app.route("/index/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(room_id)
    return render_template('room-detail.html', room=room)
# Đăng nhập
@app.route('/admin/login', methods = ['post', 'get'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password.strip()).first()
        if user:
            login_user(user=user)

            return redirect('/admin')
        else:
            err_msg = "Đăng nhập không thành công"

    return redirect('/admin')

# Trang đăng ký tài khoản
@app.route("/admin/register", methods=['post', 'get'])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() == confirm.strip():
            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            file = request.files["avatar"]
            avatar_path = 'images/upload/%s' % file.filename
            if file:
                file.save(os.path.join(app.root_path, 'static/', avatar_path))

            if utils.add_user(name=name, username=username, password=password, avatar=avatar_path, email=email):
                return redirect('/admin')
            else:
                err_msg = "Something Wrong!!!"

        else:
            err_msg = "Mật khẩu không trùng khớp"

    return redirect('/register')
# Trang tạm dùng để lấy thông tin đặt phòng của khách điền từ form
@app.route('/payment', methods=['post'])
def add_to_cart():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        price = float(request.form.get('price'))
        local = int(request.form.get('local'))
        foreign = int(request.form.get('foreign'))
        in_date = request.form.get('in_date')
        out_date = request.form.get('out_date')
        guest = request.form.get('guest')
        phone = request.form.get('phone')
        reg = utils.getReg()
        date = datetime.strptime(out_date, '%Y-%m-%d') - datetime.strptime(in_date, '%Y-%m-%d')
        quantity = local + foreign
        total = float(price) * date.days

# Kiểm tra quy định
        if int(date.days) <= 0:
            total = 0
            date = datetime.strptime(in_date, '%Y-%m-%d') - datetime.strptime(in_date, '%Y-%m-%d')

        if local + foreign <= reg.max:
            if quantity > 2:
                total = total + (quantity - 2) * total * reg.sercharse
        else:
            quantity = 0
            total = 0

        if foreign > 0:
            total *= reg.increase
            is_foreign = True
        else:
            is_foreign = False
# Lưu thông tin đặt hàng vào cart
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']


    cart[id] = {
        "id": id,
        "name": name,
        "price": price,
        "date": date.days,
        "quantity": quantity,
        "is_foreign": is_foreign,
        "total": total,
        "sum": 1,
        "guest": guest,
        "phone": phone
    }
    session['cart'] = cart
# Tính và lưu tổng tiền trong cart
    sum , sum_total = utils.cart_stats(cart)
    cart_info = {
        "sum": sum,
        "sum_total": sum_total
    }
    return render_template("payment.html",cart_info = cart_info)
# Trang thanh toán
@app.route('/payment', methods=['get', 'post'] )
def payment():
    sum, sum_total = utils.cart_stats(session.get('cart'))
    cart_info = {
        "sum": sum,
        "sum_total": sum_total
    }
    return render_template('payment.html', cart_info=cart_info)

# Xử lí thanh toán và lưu hóa đơn
@app.route('/api/pay', methods=['post'])
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']
        return (jsonify({
            "message": "Đã thêm hóa đơn thành công!",
            "err_code": 200,
        }))

    return jsonify({
        "message": "Thanh toán thất bại!!!"
    })

# Trang thuê phòng tại sảnh
@app.route('/admin/checkin')
def checkin():
    rooms = utils.read_rooms()
    return render_template('admin/checkin.html', rooms=rooms)

# Trang thuê phòng đặt trước.....(Chưa thực thi)
@app.route('/admin/e-checkin')
def e_checkin():
    return render_template('admin/e-checkin.html')

# Trang trả phòng
@app.route('/admin/checkout')
def checkout():
    return render_template('admin/checkout.html')

# Xử lí thay đổi trạng thái phòng
@app.route('/api/changeActive', methods=['GET','POST'])
def changeActive():
    data = json.loads(request.data)
    room_id = str(data.get('id'))
    utils.changeActive(room_id)
    return jsonify({})

# Xử lí xóa phòng trong cart ở trang thanh toán
@app.route('/api/delCart', methods = ['post'])
def delCart():
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    data = json.loads(request.data)
    id = str(data.get('id'))

    if id in cart:
        cart.pop(id)
    session['cart'] = cart

    if not cart:
        del session['cart']

    return jsonify({})


@app.route('/contact')
def contact():
    return render_template('contact.html')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run(debug=True, port='5555')