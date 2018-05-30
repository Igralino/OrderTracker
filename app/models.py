import datetime
import random
import string

from flask import url_for, render_template, session
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, app, mail


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    email = db.Column(db.String)
    confirmed = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    processes = db.relationship('Process', backref='business', lazy='dynamic')
    chats = db.relationship('Chat', backref='business_side', lazy='dynamic')
    possible_processes = db.relationship('PossibleProcess', backref='business', lazy='dynamic')

    def __repr__(self):
        return '<Business {}>'.format(self.name, self.email, self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def __init__(self, name, password, email, confirmed):
        self.name = name
        self.password = generate_password_hash(password)

        self.email = email
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed

    @staticmethod
    def get_name(id):
        n = Business.query.filter_by(id=id).first().name
        return n

    @staticmethod
    def get_email(id):
        e = Business.query.filter_by(id=id).first().email
        return e

    @staticmethod
    def get_possible_processes(id):
        b = Business.query.filter_by(id=id).first().possible_processes
        return b

    @staticmethod
    def get_processes(id):
        b = Business.query.filter_by(id=id).first().processes
        return b

    @staticmethod
    def name_is_free(name):
        business = Business.query.all()
        is_free = True
        for b in business:
            if b.name == name and Business.it_works(b.id):
                is_free = False
        return is_free

    @staticmethod
    def email_is_free(email):
        business = Business.query.all()
        is_free = True
        for b in business:
            if b.email == email and Business.it_works(b.id):
                is_free = False
        return is_free

    @staticmethod
    def password_is_valid(password):
        return password.isalnum()

    @staticmethod
    def check_b(email, password):
        b_email = Business.query.filter_by(email=email).first()
        if b_email:
            b_password = Business.query.filter_by(email=email).first().password
            if check_password_hash(b_password, password):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def it_works(id):
        if not Business.check_confirmed(id) and Business.account_is_old(id):
            return False
        return True

    @staticmethod
    def check_confirmed(id):
        if Business.query.filter_by(id=id).first().confirmed:
            return True
        return False

    @staticmethod
    def account_is_old(id):
        business = Business.query.all()
        is_old = False
        for b in business:
            if b.id == id:
                timeb = b.registered_on
                timenow = datetime.datetime.now()
                deltatime = timenow - timeb
                delta = deltatime.days
                if delta >= 7:
                    is_old = True
        return is_old

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        # noinspection PyBroadException
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email

    @staticmethod
    def send_email(to, subject, template):
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender='no_reply@mshp.yaconnect.com'
        )
        mail.send(msg)

    @staticmethod
    def send_token(email):
        token = Business.generate_confirmation_token(email)
        confirm_url = url_for('business.confirm_email', token=token, _external=True)
        html = render_template('email_letters/activate.html', confirm_url=confirm_url)
        subject = "Пожалуйста, подтвердите почту"
        Business.send_email(email, subject, html)

    @staticmethod
    def random_password(size, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def send_password(email, new_password):
        url = url_for('business.login_business', _external=True)
        html = render_template('email_letters/new_password.html', new_password=new_password, email=email, url=url)
        subject = "Ваш новый пароль"
        Business.send_email(email, subject, html)

    @staticmethod
    def send_password_client(email, number, password):
        url = url_for('index', _external=True)
        html = render_template('email_letters/new_password_client.html', email=email, new_password=password,
                               number=number,
                               url=url)
        subject = "Ваш новый пароль"
        Business.send_email(email, subject, html)

    @staticmethod
    def send_stages(email, stage_id, business, number, type):

        if "Закончен" == Stage.get_name(stage_id):
            url = url_for('index', _external=True)
            html = render_template('email_letters/finished_process.html', type=type, business=business, number=number,
                                   url=url)
            subject = "Заказ был завершен"
            Business.send_email(email, subject, html)
        else:
            if Process.get_send(Process.get_id(number)):
                url = url_for('index', _external=True)
                html = render_template('email_letters/send_stage.html', type=type, business=business,
                                       stage=Stage.get_name(stage_id), number=number, url=url)
                subject = "Изменение этапа"
                Business.send_email(email, subject, html)

    @staticmethod
    def get_all():
        return Business.query.all()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    processes = db.relationship('Process', backref='client', lazy='dynamic')

    def __repr__(self):
        return '<Client {}>'.format(self.email)

    def __init__(self, email):
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def is_real(email, id):
        i = False
        process = Process.query.all()
        for p in process:
            if Client.get_email(p.client_id) == email and p.business_id == int(id):
                i = True
        return i

    @staticmethod
    def get_processes(id):
        u = Client.query.filter_by(id=id).first().processes
        return u

    @staticmethod
    def get_email(id):
        e = Client.query.filter_by(id=id).first().email
        return e

    @staticmethod
    def get_id(email):
        e = Client.query.filter_by(email=email).first().id
        return e

    @staticmethod
    def email_is_free(email):
        if Client.query.filter_by(email=email).first() is None:
            return True
        return False

    @staticmethod
    def random_password(size, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_for_business = db.Column(db.Integer)
    id_for_client = db.Column(db.Integer)
    number = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    type = db.Column(db.Integer, db.ForeignKey('possible_process.id'))
    desc = db.Column(db.String)
    current_stage = db.Column(db.Integer)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    data = db.Column(db.DateTime, nullable=False)
    percent = db.Column(db.Integer)
    # price = db.Column(db.String)
    send_all_stages = db.Column(db.Boolean)
    password = db.Column(db.String)
    star = db.Column(db.Integer)
    # chat = db.relationship('Chat', backref="process_side")
    chat = db.relationship('Chat', uselist=False, back_populates="process")
    price = db.Column(db.String(50))

    def __repr__(self):
        return '<Process client: {}, type: {}>'.format(self.client_id, self.type)

    def __init__(self, type, desc, business_id, client_id, number, price, password, data=None, percent=None):
        self.type = type
        self.desc = desc
        self.business_id = business_id
        self.client_id = client_id
        self.number = number
        self.id_for_business = Process.how_much(self.business_id) + 1
        self.id_for_client = Process.how_much_for_client(self.client_id) + 1
        self.data = data or datetime.datetime.now()
        self.percent = percent or 0
        self.current_stage = Stage.get_not_started(type)
        self.price = price
        self.send_all_stages = False
        self.password = generate_password_hash(password)
        self.star = -1
        self.chat = Chat(self.id, self.business_id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        self.chat.process_id = self.id
        self.chat.save()
        return self.id

    @staticmethod
    def how_much(id):
        h = 0
        process = Process.query.all()
        for p in process:
            if p.business_id == id:
                h += 1
        return h

    @staticmethod
    def how_much_for_client(id):
        h = 0
        process = Process.query.all()
        for p in process:
            if p.client_id == id:
                h += 1
        return h

    @staticmethod
    def find(words, id):
        i = 0
        pr = [0] * Process.how_much(id)
        process = Process.query.all()
        for p in process:
            if (p.number.lower().find(words.lower(),
                                      0, len(p.number)) >= 0 or p.desc.lower().find(
                words.lower(), 0, len(p.desc)) >= 0 or Client.get_email(
                p.client_id).lower().find(words.lower(), 0,
                                          len(Client.get_email(p.client_id))) >= 0 or PossibleProcess.get_type(
                p.type).lower().find(words.lower(), 0,
                                     len(PossibleProcess.get_type(p.type))) >= 0) and p.business_id == id:
                pr[i] = p
                i += 1
        return pr

    @staticmethod
    def find_for_client(words, id):
        i = 0
        pr = [0] * Process.how_much_for_client(int(id))
        process = Process.query.all()
        for p in process:
            if (p.number.lower().find(words.lower(), 0, len(p.number)) >= 0 or
                p.desc.lower().find(words.lower(), 0,
                                    len(
                                        p.desc)) >= 0 or PossibleProcess.get_type(
                        p.type).lower().find(words.lower(), 0,
                                             len(PossibleProcess.get_type(p.type))) >= 0 or Business.get_name(
                        p.business_id).lower().find(words.lower(), 0,
                                                    len(Business.get_name(p.business_id))) >= 0) and p.client_id == int(
                id):
                pr[i] = p
                i += 1
        return pr

    @staticmethod
    def check_p(id, password):

        if Process.query.filter_by(id=id).first() is None:
            return False
        elif check_password_hash(Process.get_password(id), password):
            return True
        else:
            return False

    @staticmethod
    def get_percent(id):
        p = Process.query.filter_by(id=id).first().percent
        return p

    @staticmethod
    def get_star(id):
        p = Process.query.filter_by(id=id).first().star
        return p

    @staticmethod
    def get_password(id):
        p = Process.query.filter_by(id=id).first().password
        return p

    @staticmethod
    def get_price(id):
        p = Process.query.filter_by(id=id).first().price
        return p

    @staticmethod
    def get_data(id):
        d = Process.query.filter_by(id=id).first().data
        return d

    @staticmethod
    def is_real_number(number):
        i = Process.query.filter_by(number=number).first()
        return i

    @staticmethod
    def get_id(number):
        i = Process.query.filter_by(number=number).first().id
        return i

    @staticmethod
    def get_business(id):
        p = Process.query.filter_by(id=id).first().business_id
        return p

    @staticmethod
    def get_send(id):
        p = Process.query.filter_by(id=id).first().send_all_stages
        return p

    @staticmethod
    def get_number(id):
        n = Process.query.filter_by(id=id).first().number
        return n

    @staticmethod
    def get_type_id(id):
        t = Process.query.filter_by(id=id).first().type
        return t

    @staticmethod
    def get_client_id(id):
        c = Process.query.filter_by(id=id).first().client_id
        return c

    @staticmethod
    def get_client(id):
        c = Client.query.filter_by(id=id).first().email
        return c

    @staticmethod
    def get_stages(id):
        p = Process.query.filter_by(id=id).first().current_stage
        return p

    @staticmethod
    def get_stage_name(id_stage):
        s = Stage.query.filter_by(id=id_stage).first().type
        return s

    @staticmethod
    def get_desc(id):
        d = Process.query.filter_by(id=id).first().desc
        return d

    @staticmethod
    def get_chat(id):
        d = Process.query.filter_by(id=id).first().chat
        return d

    @staticmethod
    def get_all():
        return Process.query.all()

    @staticmethod
    def random_token(size, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def random_number():
        number = Process.random_token(6) + '-' + Process.random_token(6)
        return number

    @staticmethod
    def send_number(email, business, number, password):
        url = url_for('index', _external=True)
        html = render_template('email_letters/process_number.html', password=password, business=business, number=number,
                               url=url)
        subject = "Номер заказа"
        Business.send_email(email, subject, html)

    @staticmethod
    def is_real(id):
        if Process.query.filter_by(id=id).first() is None:
            return False
        else:
            return True

    def count_unseen_messages(self):
        b = Letter.query.filter_by(chat_id=self.chat.id, is_seen=False, is_business=False).all()
        return len(b)


class PossibleProcess(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String)
    desc = db.Column(db.String)
    stages = db.relationship('Stage', backref='possible_process', lazy='dynamic')
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    process = db.relationship('Process', backref='possible_process', lazy='dynamic')
    id_for_business = db.Column(db.Integer)
    price = db.Column(db.String)
    picture = db.Column(db.String)

    def __repr__(self):
        return '<PossibleProcess business: {}, type: {}>'.format(self.business_id, self.type)

    def __init__(self, type, desc, business_id, price):
        self.type = type
        self.desc = desc
        self.business_id = business_id
        self.id_for_business = PossibleProcess.how_much(self.business_id) + 1
        self.price = price
        self.picture = -1

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_picture(id):
        n = PossibleProcess.query.filter_by(id=id).first().picture
        return n

    @staticmethod
    def how_much(id):
        h = 0
        process = PossibleProcess.query.all()
        for p in process:
            if p.business_id == id:
                h += 1
        return h

    @staticmethod
    def find(words, id):
        i = 0
        pr = [0] * PossibleProcess.how_much(id)
        process = PossibleProcess.query.all()
        for p in process:
            if (p.type.lower().find(words.lower(), 0, len(p.type)) >= 0 or p.desc.lower().find(
                    words.lower(), 0,
                    len(p.desc)) >= 0) and p.business_id == id:
                pr[i] = p
                i += 1
        return pr

    @staticmethod
    def get_all():
        return PossibleProcess.query.all()

    @staticmethod
    def is_real(id):
        if PossibleProcess.query.filter_by(id=id).first() is None:
            return False
        else:
            return True

    @staticmethod
    def get_stages(id):
        p = PossibleProcess.query.filter_by(id=id).first().stages
        return p

    @staticmethod
    def get_type(id):
        p = PossibleProcess.query.filter_by(id=id).first().type
        return p

    @staticmethod
    def get_price(id):
        p = PossibleProcess.query.filter_by(id=id).first().price
        return p

    @staticmethod
    def get_desc(id):
        p = PossibleProcess.query.filter_by(id=id).first().desc
        return p

    @staticmethod
    def get_descs(id):
        p = PossibleProcess.query.filter_by(business_id=id).all()
        return p

    @staticmethod
    def get_business(id):
        p = PossibleProcess.query.filter_by(id=id).first().business_id
        return p


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String)
    id_for_business = db.Column(db.Integer)

    process_id = db.Column(db.Integer, db.ForeignKey('possible_process.id'))

    def __repr__(self):
        return '[OPTION] <%r>' % self.type

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def by_id_for_business(stage):
        return stage.id_for_business

    @staticmethod
    def sort_by_id_for_business(process_id):
        i = 0
        st = [0] * (Stage.get_finished_id_for_business(process_id) + 1)
        stage = Stage.query.all()
        for s in stage:
            if int(s.process_id) == int(process_id):
                st[i] = s
                i += 1
        stages = sorted(st, key=Stage.by_id_for_business)
        return stages

    @staticmethod
    def how_much(id):
        h = 0

        stage = Stage.query.all()
        for s in stage:
            if int(s.process_id) == int(id):
                h += 1
        return h

    @staticmethod
    def get_all():
        return Stage.query.all()

    @staticmethod
    def get_type(id):
        type = PossibleProcess.query.filter_by(id=id).first().type
        return type

    @staticmethod
    def get_name(id):
        name = Stage.query.filter_by(id=id).first().type
        return name

    @staticmethod
    def get_not_started(process_id):
        stage = Stage.query.all()
        i = 0
        for s in stage:
            if int(s.process_id) == int(process_id):
                if s.type == "Не начат":
                    i = s.id

        return i

    @staticmethod
    def get_finished_id_for_business(process_id):
        stage = Stage.query.all()
        for s in stage:
            if int(s.process_id) == int(process_id):
                if s.type == "Закончен":
                    i = s.id_for_business
        return i

    @staticmethod
    def fix_not_finished(id):

        stage = Stage.query.all()
        for s in stage:
            if int(s.process_id) == int(id):
                if s.type == "Закончен":
                    rows = Stage.query.filter_by(id=s.id).update({'id_for_business': Stage.how_much(id) - 1})
                    db.session.commit()

    @staticmethod
    def __init__(self, type, process_id):
        self.type = type
        self.process_id = process_id
        if type == "Не начат":
            self.id_for_business = 0
        elif type == "Закончен":
            self.id_for_business = 0
        else:
            self.id_for_business = Stage.how_much(process_id) - 1


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer)
    picture = db.Column(db.String)

    def __repr__(self):
        return '<Pictures: {}>'.format(self.id)

    def __init__(self, business_id):
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id


class BusinessCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    contact_information = db.Column(db.String)
    business_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    picture = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self):
        return '<Business card: {}>'.format(self.business_id)

    def __init__(self, name, description, contact_information, address, business_id):
        self.name = name
        self.description = description
        self.contact_information = contact_information
        self.address = address
        self.business_id = business_id
        self.rating = 0
        self.picture = "-1"

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def by_rating(card):
        return card.rating

    @staticmethod
    def sort_by_rating():
        card = BusinessCard.query.all()
        cards = sorted(card, key=BusinessCard.by_rating)
        return cards

    @staticmethod
    def find(words):
        i = 0
        car = [0] * BusinessCard.how_much()
        card = BusinessCard.query.all()
        for c in card:
            if c.name.lower().find(words.lower(), 0, len(c.name)) >= 0 or c.description.lower().find(
                    words.lower(), 0, len(c.description)) >= 0:
                car[i] = c
                i += 1

        return car

    @staticmethod
    def get_name(business_id):
        n = BusinessCard.query.filter_by(business_id=business_id).first().name
        return n

    @staticmethod
    def get_address(business_id):
        n = BusinessCard.query.filter_by(business_id=business_id).first().address
        return n

    @staticmethod
    def how_much():
        h = 0
        cards = BusinessCard.query.all()
        for c in cards:
            h += 1
        return h

    @staticmethod
    def get_picture(business_id):
        n = BusinessCard.query.filter_by(business_id=business_id).first().picture
        return n

    @staticmethod
    def get_new_rating(business_id):
        if BusinessCard.how_much_comments(business_id) == 0:
            rating = 0
        else:
            rating = round(BusinessCard.how_much_stars(business_id) / BusinessCard.how_much_comments(business_id), 2)
        # rows = BusinessCard.query.filter_by(business_id=business_id).update({'rating': rating})
        db.session.commit()
        return rating

    @staticmethod
    def how_much_comments(business_id):
        comments = Comments.query.all()
        how = 0
        for c in comments:
            if c.business_id == int(business_id):
                how += 1
        return how

    @staticmethod
    def how_much_stars(business_id):
        comments = Comments.query.all()
        how = 0
        for c in comments:
            if c.business_id == int(business_id):
                how += c.star
        return how

    @staticmethod
    def get_description(business_id):
        d = BusinessCard.query.filter_by(business_id=business_id).first().description
        return d

    @staticmethod
    def get_contact_information(business_id):
        c = BusinessCard.query.filter_by(business_id=business_id).first().contact_information
        return c

    @staticmethod
    def is_real(business_id):
        if BusinessCard.query.filter_by(business_id=business_id).first() is None:
            return False
        return True


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    client_id = db.Column(db.Integer)
    business_id = db.Column(db.Integer)
    client_name = db.Column(db.String)
    star = db.Column(db.Integer)

    def __repr__(self):
        return '<Comments: {}>'.format(self.id)

    def __init__(self, text, client_id, business_id, client_name, star):
        self.text = text
        self.client_id = client_id
        self.business_id = business_id
        self.client_name = client_name
        self.star = star

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_text(id):
        c = Comments.query.filter_by(id=id).first().text
        return c

    @staticmethod
    def get_name(id):
        c = Comments.query.filter_by(id=id).first().client_name
        return c

    @staticmethod
    def get_star(id):
        c = Comments.query.filter_by(id=id).first().star
        return c

    @staticmethod
    def get_email(id):
        c = Client.get_email(Comments.query.filter_by(id=id).first().client_id)
        return c


class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer)
    type = db.Column(db.String(5))
    url = db.Column(db.String(200))
    text = db.Column(db.String(200))
    textpos = db.Column(db.Integer)
    pages = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def __init__(self, bid, type, url, text, textpos, pages):
        self.business_id = bid
        self.type = type
        self.url = url
        self.text = text
        self.textpos = textpos
        self.pages = pages

    @staticmethod
    def get_url(bid):
        if Widget.query.filter_by(business_id=bid).first() is not None:
            url = Widget.query.filter_by(business_id=bid).first().url
            return url
        else:
            return False

    @staticmethod
    def get_pages(bid):
        pages = Widget.query.filter_by(business_id=bid).first().pages
        return pages

    @staticmethod
    def get_text(bid):
        text = Widget.query.filter_by(business_id=bid).first().text
        return text

    @staticmethod
    def if_exist(bid):
        if Widget.query.filter_by(business_id=bid).first():
            return True
        else:
            return False

    @staticmethod
    def get_type(bid):
        type = Widget.query.filter_by(business_id=bid).first().type
        return type

    @staticmethod
    def get_pos(bid):
        pos = Widget.query.filter_by(business_id=bid).first().textpos
        return pos


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    process_id = db.Column(db.Integer, db.ForeignKey('process.id'))
    process = db.relationship("Process", back_populates="chat")
    messages = db.relationship('Letter', backref='chat')

    def __repr__(self):
        return '<Chat: {}, with: {}>'.format(self.business_id, self.process_id)

    def __init__(self, process_id, business_id):
        self.process_id = process_id
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_messages(id):
        b = Chat.query.filter_by(id=id).first().messages
        return b

    @staticmethod
    def get_by_proc(proc_id):
        b = Chat.query.filter_by(process_id=int(proc_id)).first()
        return b

    @staticmethod
    def read_all(chat_id, is_business=True):
        for msg in Letter.query.filter_by(chat_id=chat_id, is_delivered=False, is_business=is_business):
            msg.is_delivered = True
        db.session.commit()

    @staticmethod
    def get_unread_messages(business_id):
        b = Letter.query.filter_by(is_business=False, is_delivered=False).all()
        return b

    @staticmethod
    def see_all(chat_id, is_business):
        for msg in Letter.query.filter_by(chat_id=chat_id, is_seen=False, is_business=is_business):
            msg.is_seen = True
        db.session.commit()

    @staticmethod
    def can_write(chat_id):
        c = Chat.query.get(chat_id)
        return str(c.business_id) == str(session.get('id', '')) or str(c.process.client_id) == str(
            session.get('id_client', ''))


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    text = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)
    is_business = db.Column(db.Boolean)
    is_delivered = db.Column(db.Boolean)
    is_seen = db.Column(db.Boolean)

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def __init__(self, chat_id, text, is_business):
        self.text = text
        self.chat_id = chat_id
        self.create_time = datetime.datetime.now()
        self.is_business = is_business
        self.is_delivered = False
        self.is_seen = False

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_text(id):
        c = Letter.query.filter_by(id=id).first().text
        return c

    @staticmethod
    def get_time(id):
        c = Letter.query.filter_by(id=id).first().create_time
        return c
