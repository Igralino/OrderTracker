import os
from datetime import datetime

from flask import render_template, redirect, request, session, url_for
from flask import send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.models import Business, PossibleProcess, Stage, Process, Client, BusinessCard, Comments, Pictures, Chat
from app.models import Widget
from business_account.forms import RegistrationBusinessForm, LoginBusinessForm, ChangeBusinessNameForm, CommentsForm, \
    ChangeBusinessPasswordForm, PossibleProcessForm, ChangePossibleProcessForm, UnconfirmedForm, ForgotPasswordForm, \
    CreateProcessForm, \
    SelectFieldTypeForm, ChangeForm, SelectFieldStageForm, FindForm, DateForm, CreationCardForm, HelpForm, \
    WidgetDataForm, WidgetEraseForm
# from business_account.__init__ import ALLOWED_EXTENSIONS, secure_filename, os
from . import business

UPLOAD_FOLDER = './business_account/static/pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@business.route('/')
@business.route('/main_page')
def index():
    if session.get('id', '') != '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    return redirect(url_for('business.login_business'))


@business.route('/information_for_business')
def information_for_business():
    return render_template('information_for_business.html', title='Помощь')


@business.route('/registration_business', methods=['GET', 'POST'])
def registration_business():
    if session.get('id', '') != '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    session['id_client'] = ''
    form = RegistrationBusinessForm(csrf_enabled=False)
    if form.validate_on_submit():
        free_name = Business.name_is_free(form.name.data)
        free_email = Business.email_is_free(form.email.data)
        check_pass = (form.password.data == form.check_password.data)
        password_is_valid = Business.password_is_valid(form.password.data)
        if free_name and check_pass and password_is_valid and free_email:
            Business.send_token(form.email.data)
            business = Business(name=form.name.data, password=form.password.data,
                                email=form.email.data, confirmed=False)
            Business.save(business)
            return redirect(
                "/business/feedback/Регистрация прошла успешно. Пройдите по ссылке, \
                которую мы отправили вам на почту, чтобы подтвердить её")
        elif not free_name:
            form.name.errors = ('Название занято', '')
        elif not free_email:
            form.email.errors = ('Почта занята', '')
        elif not password_is_valid:
            form.check_password.errors = ('Пароль не может содержать пробелы', '')
        elif not check_pass:
            form.check_password.errors = ('Пароли не совпадают', '')
    return render_template('registration_business.html', title='Регистрация бизнеса', form=form)


@business.route('/login_business', methods=['GET', 'POST'])
def login_business():
    if session.get('id', '') != '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    session['id_client'] = ''
    form = LoginBusinessForm()
    if form.validate_on_submit():
        if Business.check_b(form.email.data, form.password.data):

            session['id'] = Business.query.filter_by(email=form.email.data).first().id
            if not Business.it_works(session.get('id', '')):
                session['id'] = ''
                form.password.errors = ('Неправильная почта или пароль', '')
            elif not Business.check_confirmed(session.get('id', '')):
                return redirect('/business/unconfirmed')
            else:
                return redirect(url_for('business.business_card', business_id=session.get('id', '')))
        else:
            form.password.errors = ('Неправильная почта или пароль', '')
    return render_template('login_business.html', title='Вход бизнеса', form=form)


@business.route('/exit_business', methods=['GET'])
def exit_business():
    session['id'] = ''
    return redirect('/business')


@business.route('/profile_business', methods=['GET'])
def profile_business():
    if session.get('id', '') == '':
        return redirect('/business')
    if not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    name = Business.query.filter_by(id=session.get('id', '')).first().name
    email = Business.query.filter_by(id=session.get('id', '')).first().email
    return render_template('profile_business.html', title='Профиль бизнеса', name=name, email=email)


@business.route('/change_business', methods=['GET', 'POST'])
def change_business():
    if session.get('id', '') == '':
        return redirect('/business')
    if not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    changename = ""
    changepassword = ""
    form_name = ChangeBusinessNameForm()
    form_password = ChangeBusinessPasswordForm()
    id = session.get('id', '')
    if form_name.submit1.data and form_name.validate_on_submit():
        free_name = Business.name_is_free(form_name.new_name.data)
        b_password = Business.query.filter_by(id=id).first().password
        b_name = Business.get_name(id)
        if free_name or b_name == form_name.new_name.data \
                and check_password_hash(b_password, form_name.password.data):
            rows = Business.query.filter_by(id=id).update({'name': form_name.new_name.data})
            db.session.commit()
            if BusinessCard.is_real(session.get('id', '')):
                rows = BusinessCard.query.filter_by(business_id=session.get('id', '')).update(
                    {'name': form_name.new_name.data})
                db.session.commit()
            changename = "Название было изменено"
            # return redirect('/change_business')
        elif not free_name and form_name.new_name.data != b_name:
            form_name.new_name.errors = ('Название занято', '')
        elif not check_password_hash(b_password, form_name.password.data):
            form_name.password.errors = ('Неправильный пароль', '')
    if form_password.submit2.data and form_password.validate_on_submit():
        b_password = Business.query.filter_by(id=id).first().password
        check_new = form_password.new_password.data == form_password.check_new_password.data
        check_old = check_password_hash(b_password, form_password.old_password.data)
        password_is_valid = Business.password_is_valid(form_password.new_password.data)
        if check_old and check_new and password_is_valid:
            new_password = generate_password_hash(form_password.new_password.data)
            rows = Business.query.filter_by(id=id).update({'password': new_password})
            db.session.commit()
            changepassword = "Пароль был изменен"
            # return redirect('/change_business')
        elif not password_is_valid:
            form_password.new_password.errors = ('Пароль не может содержать пробелы', '')
        elif not check_new:
            form_password.check_new_password.errors = ('Пароли не совпадают', '')
        elif not check_old:
            form_password.old_password.errors = ('Неправильный пароль', '')
    form_name.new_name.data = Business.query.filter_by(id=id).first().name
    return render_template('change_business.html', title='Изменить настройки бизнеса', form=form_name,
                           p_form=form_password,
                           changename=changename, changepassword=changepassword)


@business.route('/add_possible_process', methods=['GET', 'POST'])
def add_possible_process():
    if session.get('id', '') == '':
        return redirect('/business')
    if not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')

    b_id = session['id']
    form = PossibleProcessForm()
    if form.validate_on_submit():
        process = PossibleProcess(form.type.data, form.desc.data, b_id, form.price.data)
        pr_id = process.save()
        stage_not_started = Stage("Не начат", pr_id)
        stage_not_started.save()
        stage_finished = Stage("Закончен", pr_id)
        stage_finished.save()

        stages = form.stages.data
        for stage in stages:
            option_instance = Stage(stage, pr_id)
            db.session.add(option_instance)
        db.session.commit()
        Stage.fix_not_finished(pr_id)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    pic = Pictures(b_id)
                    id_picture = Pictures.save(pic)
                    picture = str(id_picture)
                    filename = secure_filename(file.filename)
                    picture += "." + filename.rsplit('.', 1)[1].lower()
                    rows = Pictures.query.filter_by(id=id_picture).update({'picture': picture})
                    rows = PossibleProcess.query.filter_by(id=pr_id).update({'picture': picture})
                    db.session.commit()
                    file.save(os.path.join(UPLOAD_FOLDER, str(picture)))

        return redirect('/business/possible_process_list')
    return render_template('add_possible_process.html', form=form, title="Создание услуги")


@business.route('/possible_process_list', methods=['GET', 'POST'])
def possible_process_list():
    if session.get('id', '') == '':
        return redirect('/business')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    form = FindForm()
    possible_process_list = Business.get_possible_processes(session['id'])
    if form.validate_on_submit():
        possible_process_list = PossibleProcess.find(form.words.data, session['id'])
        if possible_process_list[0] == 0:
            form.words.errors = ("Ничего не найдено", "")
    return render_template('possible_process_list.html', possible_process_list=possible_process_list[::-1],
                           title='Список возможных услуг', form=form)


from business_account.forms import HelpIdForm


@business.route('/possible_process/<possible_process_id>', methods=['GET', 'POST'])
def possible_process(possible_process_id):  # {{ url_for('business_account.process', process_id=process.id) }}
    if session.get('id', '') == '':
        return redirect('/business')
    elif not PossibleProcess.is_real(possible_process_id):
        return redirect('/business/possible_process_list')
    elif PossibleProcess.get_business(possible_process_id) != session.get('id', ''):
        return redirect('/business/possible_process_list')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    form = ChangePossibleProcessForm()
    formh = HelpIdForm()
    if form.validate_on_submit():
        PossibleProcess.query.filter_by(id=possible_process_id).update({'type': form.new_type.data})
        stages = form.stages.data

        list = request.form.getlist("id")

        id_for_business = 0
        for id in list:
            Stage.query.filter_by(id=id).update({'id_for_business': id_for_business})
            id_for_business += 1

        for stage in stages:
            option_instance = Stage(stage, possible_process_id)
            db.session.add(option_instance)
        db.session.commit()
        Stage.fix_not_finished(possible_process_id)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    pic = Pictures(session.get('id', ''))
                    id_picture = Pictures.save(pic)
                    picture = str(id_picture)
                    filename = secure_filename(file.filename)
                    picture += "." + filename.rsplit('.', 1)[1].lower()
                    rows = Pictures.query.filter_by(id=id_picture).update({'picture': picture})
                    rows = PossibleProcess.query.filter_by(id=possible_process_id).update({'picture': picture})
                    db.session.commit()
                    file.save(os.path.join(UPLOAD_FOLDER, str(picture)))
        return redirect(url_for('business.possible_process', possible_process_id=possible_process_id))
    stages_list = Stage.sort_by_id_for_business(possible_process_id)
    form.new_type.data = PossibleProcess.get_type(possible_process_id)
    form.desc.data = PossibleProcess.get_desc(possible_process_id)
    form.price.data = PossibleProcess.get_price(possible_process_id)
    picture = PossibleProcess.get_picture(possible_process_id)
    is_picture = (PossibleProcess.get_picture(possible_process_id) != "-1")
    return render_template('possible_process.html', stages_list=stages_list, form=form, title='Услуга', formh=formh,
                           picture=picture, is_picture=is_picture)


@business.route('/unconfirmed', methods=['GET', 'POST'])
def unconfirmed():
    if session.get('id', '') == '':
        return redirect('/business')
    elif Business.check_confirmed(session.get('id', '')):
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    form = UnconfirmedForm()
    id = session.get('id', '')
    if request.method == 'POST':
        Business.send_token(Business.get_email(id))
        session['id'] = ''
        return redirect(
            "/business/feedback/Пройдите по ссылке, \
            которую мы отправили вам на почту, чтобы подтвердить её")
    return render_template('unconfirmed.html', title="Аккаунт не подтвержден", form=form)


@business.route('/feedback/<text>', methods=['GET', 'POST'])
def feedback(text):
    return render_template('feedback.html', title='feedback', text=text)


@business.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('id', '') != '':
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    session['id_client'] = ''
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        if Business.query.filter_by(email=form.email.data).first():
            id = Business.query.filter_by(email=form.email.data).first().id
            if Business.it_works(id):
                new_password = Business.random_password(size=15)
                rows = Business.query.filter_by(id=id).update({'password': generate_password_hash(new_password)})
                db.session.commit()
                Business.send_password(form.email.data, new_password)
                return redirect(
                    "/business/feedback/Мы отправили вам новый пароль на почту! Если вы не получили письмо, \
                    проверьте, что вы написали почту правильно!")

            else:
                form.email.errors = ('Неправильная почта', '')
        else:
            form.email.errors = ('Неправильная почта', '')

    return render_template('forgot_password.html', title='Забыли пароль?', form=form)


@business.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = Business.confirm_token(token)
    except:
        return redirect('/business/feedback/Ссылка не действительна')
    business = Business.query.filter_by(email=email).first_or_404()
    if business.confirmed:
        return redirect('/business/feedback/Аккаунт был подтвержден. Пожалуйста, войдите.')
    else:
        if Business.account_is_old(business.id):
            return redirect('/feedback/Ссылка не действительна! Попробуйте зарегистрироваться еще раз!')
        business.confirmed = True
        business.confirmed_on = datetime.now()
        db.session.add(business)
        db.session.commit()
        return redirect('/business/feedback/Аккаунт был подтвержден. Пожалуйста, войдите.')


@business.route('/create_process', methods=['GET', 'POST'])
def create_process():
    if session.get('id', '') == '':
        return redirect('/business/')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    b_id = session['id']
    form = CreateProcessForm()
    s_form = SelectFieldTypeForm()
    h = HelpForm()
    s_form.select_type.choices = [(p.id, p.type) for p in PossibleProcess.query.filter_by(business_id=b_id).all()]
    d_form = DateForm()

    if form.validate_on_submit() and d_form.validate_on_submit():

        if Client.email_is_free(form.client_email.data):
            client = Client(form.client_email.data)
            cl_id = client.save()
        else:
            cl_id = Client.get_id(form.client_email.data)
        client_password = Client.random_password(10)
        number = Process.random_number()
        process = Process(s_form.select_type.data, form.description.data, b_id, cl_id, number, form.price.data,
                          client_password,
                          d_form.dt.data, 0)
        pr_id = process.save()
        id_stage = Stage.get_not_started(s_form.select_type.data)
        process = Process.query.filter_by(id=pr_id).first()
        process.current_stage = id_stage
        chat = Chat(pr_id, b_id)
        chat.save()
        process.save()

        Process.send_number(form.client_email.data, Business.get_name(b_id), number, client_password)

        # string = "Услуга была создана под номером: " + number
        return redirect(url_for('business.created_process', process_id=pr_id))
    elif form.validate_on_submit() and not d_form.validate_on_submit():
        d_form.dt.errors = ("Выберите дату", "")

    h.desc.choices = [(p.desc, p.desc) for p in PossibleProcess.query.filter_by(business_id=b_id).all()]
    h.price.choices = [(p.price, p.price) for p in PossibleProcess.query.filter_by(business_id=b_id).all()]
    h.pic.choices = [(p.picture, p.picture) for p in PossibleProcess.query.filter_by(business_id=b_id).all()]
    return render_template('create_process.html', form=form, h=h, s_form=s_form, d_form=d_form, title='Создание заказа')


@business.route('/created_process_list', methods=['GET', 'POST'])
def created_process_list():
    if session.get('id', '') == '':
        return redirect('/business/')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')

    form = FindForm()
    business_id = session['id']
    process_list = Business.get_processes(business_id)
    if form.validate_on_submit():
        process_list = Process.find(form.words.data, business_id)
        if process_list[0] == 0:
            form.words.errors = ("Ничего не найдено", "")
            '''
        if Process.is_real_number(form.words.data) is None:
            form.words.errors = ("Такого номера не существует", '')
        elif Process.get_business(Process.get_id(form.words.data)) != session.get('id', ''):
            form.words.errors = ("Такого номера не существует", '')
        else:
            return redirect(url_for('business.created_process', process_id=Process.get_id(form.words.data)))
            '''

    return render_template('created_process_list.html', title='Список заказов', form=form,
                           processes=process_list[::-1], PossibleProcess=PossibleProcess, Process=Process)


@business.route('/created_process/<process_id>', methods=['POST', 'GET'])
def created_process(process_id):
    if session.get('id', '') == '':
        return redirect('/business/')
    elif not Process.is_real(process_id):
        return redirect('/business/created_process_list')
    elif Process.get_business(process_id) != session.get('id', ''):
        return redirect('/business/created_process_list')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    form = ChangeForm()
    s_form = SelectFieldStageForm()
    d_form = DateForm()
    if form.validate_on_submit() and d_form.validate_on_submit():

        if int(Process.get_stages(process_id)) != int(s_form.select_stage.data):
            Business.send_stages(Client.get_email(Process.get_client_id(process_id)), s_form.select_stage.data,
                                 Business.get_name(session.get('id', '')), Process.get_number(process_id),
                                 PossibleProcess.get_type(Process.get_type_id(process_id)))
        rows = Process.query.filter_by(id=process_id).update({'desc': form.desc.data})
        rows = Process.query.filter_by(id=process_id).update({'current_stage': s_form.select_stage.data})
        rows = Process.query.filter_by(id=process_id).update({'data': d_form.dt.data})
        rows = Process.query.filter_by(id=process_id).update({'percent': round(form.percent.data)})
        rows = Process.query.filter_by(id=process_id).update({'price': form.price.data})
        db.session.commit()
        return redirect('/business/created_process_list')
    number = Process.get_number(process_id)
    client = Client.get_email(Process.get_client_id(process_id))
    type = PossibleProcess.get_type(Process.get_type_id(process_id))
    form.desc.data = Process.get_desc(process_id)
    percent = Process.get_percent(process_id)
    form.percent.data = percent
    form.price.data = Process.get_price(process_id)

    s_form.select_stage.choices = [(s.id, s.type) for s in
                                   Stage.sort_by_id_for_business(Process.get_type_id(process_id))]
    s_form.select_stage.default = Process.get_stages(process_id)
    s_form.process()

    d_form.dt.data = Process.get_data(process_id)
    desc_type = PossibleProcess.get_desc(Process.get_type_id(process_id))

    star = Process.get_star(process_id)
    chat = Chat.get_by_proc(process_id).id

    picture = PossibleProcess.get_picture(Process.get_type_id(process_id))
    is_picture = (PossibleProcess.get_picture(Process.get_type_id(process_id)) != "-1")
    return render_template('created_process.html', title='Созданная услуга', desc_type=desc_type, percent=percent,
                           d_form=d_form, id=process_id, form=form, s_form=s_form, number=number, type=type,
                           client=client, Process=Process, chat=chat, rating=star, picture=picture,
                           is_picture=is_picture)


@business.route('/creation_card', methods=['GET', 'POST'])
def creation_card():
    if session.get('id', '') == '':
        return redirect('/business/')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    form = CreationCardForm()
    business_id = session.get('id', '')
    name = Business.get_name(business_id)
    if form.validate_on_submit():
        if not BusinessCard.is_real(business_id):
            card = BusinessCard("", "", "", "", business_id)
            BusinessCard.save(card)
        rows = BusinessCard.query.filter_by(business_id=business_id).update({'name': name})
        rows = BusinessCard.query.filter_by(business_id=business_id).update({'description': form.description.data})
        rows = BusinessCard.query.filter_by(business_id=business_id).update(
            {'contact_information': form.contact_information.data})
        rows = BusinessCard.query.filter_by(business_id=business_id).update({'address': form.address.data})
        db.session.commit()

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    pic = Pictures(business_id)
                    id_picture = Pictures.save(pic)
                    picture = str(id_picture)
                    filename = secure_filename(file.filename)
                    picture += "." + filename.rsplit('.', 1)[1].lower()
                    rows = Pictures.query.filter_by(id=id_picture).update({'picture': picture})
                    rows = BusinessCard.query.filter_by(business_id=business_id).update({'picture': picture})
                    db.session.commit()
                    file.save(os.path.join(UPLOAD_FOLDER, str(picture)))
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    if BusinessCard.is_real(business_id):
        form.description.data = BusinessCard.get_description(business_id)
        form.contact_information.data = BusinessCard.get_contact_information(business_id)
        form.address.data = BusinessCard.get_address(business_id)
    else:
        form.description.data = ""
        form.contact_information.data = ""
        form.address.data = ""
    return render_template('create_business_card.html', title='Изменить страничку бизнеса', form=form, name=name)


@business.route('/business_card/<business_id>', methods=['GET', 'POST'])
def business_card(business_id):
    if int(business_id) == session.get('id', '') and (not BusinessCard.is_real(business_id)):
        not_created = True
        return render_template('business_card.html', title='Страница бизнеса', name="", description="",
                               contact_information="", not_created=not_created, Widget=Widget, bid=business_id)
    elif session.get('id', '') == '' and not BusinessCard.is_real(business_id):
        return redirect('/business/business_card_list')
    elif not BusinessCard.is_real(business_id):
        return redirect('/business/business_card_list')
    session['id_client'] = ''
    not_created = False
    name = BusinessCard.get_name(business_id)
    description = BusinessCard.get_description(business_id)
    contact_information = BusinessCard.get_contact_information(business_id)
    address = BusinessCard.get_address(business_id)
    form = CommentsForm()

    if form.validate_on_submit():
        if not Client.is_real(form.email.data, business_id):
            form.email.errors = (
                "Вы не можете отправлять комментарии, потому что вы не являетесь клиентом этого бизнеса", "")
        else:
            comments = Comments(form.text.data, Client.get_id(form.email.data), business_id, form.name.data,
                                form.star.data)
            Comments.save(comments)
            rating = BusinessCard.get_new_rating(business_id)
            rows = BusinessCard.query.filter_by(business_id=business_id).update(
                {'rating': rating})
            db.session.commit()

            return redirect(url_for('business.business_card', business_id=business_id))

    comment_list = Comments.query.filter_by(business_id=business_id).all()
    if session.get('id', '') == int(business_id):
        business_account = True
    else:
        business_account = False
    form.star.data = 1
    howmuchcomments = BusinessCard.how_much_comments(business_id)
    rating = BusinessCard.get_new_rating(business_id)
    return render_template('business_card.html', title='Страничка бизнеса',
                           name=name, description=description,
                           contact_information=contact_information, rating=rating, howmuchcomments=howmuchcomments,
                           business_account=business_account, business_id=business_id, not_created=not_created,
                           form=form, comment_list=comment_list[::-1], address=address, Comments=Comments,
                           BusinessCard=BusinessCard, Widget=Widget, bid=business_id)


@business.route('/business_card_list/', methods=['GET', 'POST'])
def business_card_list():
    if not session.get('id', '') == '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''

    form = FindForm()
    business_card_list = BusinessCard.sort_by_rating()[::-1]
    if form.validate_on_submit():
        business_card_list = BusinessCard.find(form.words.data)
        if business_card_list[0] == 0:
            form.words.errors = ("Ничего не найдено", "")
    return render_template('business_card_list.html', title='Странички бизнесов',
                           business_card_list=business_card_list, BusinessCard=BusinessCard, form=form)


@business.route('/widget_creation', methods=['GET', 'POST'])
def widget_creation():
    if session.get('id', '') == '':
        return redirect('/business/')
    elif not Business.check_confirmed(session.get('id', '')):
        return redirect('/business/unconfirmed')
    form = WidgetDataForm(request.form)
    erase_form = WidgetEraseForm(request.args)
    if erase_form.submit.data:
        upd = Widget.query.filter_by(business_id=session.get('id', ''))
        upd.update({'pages': int(erase_form.pages.data)})
        db.session.commit()

    if session.get('id', '') != '':
        if request.method == 'GET':
            return render_template('widget_creation.html', Widget=Widget, form=form, bid=session.get('id', ''),
                                   erase_form=erase_form)
        if request.method == 'POST':

            bid = session['id']
            if form.type.data == 'game':
                url = 'kek'
                text = 'Игра'
                textpos = 1
                pages = 3
            else:
                if 'photo' in request.files:
                    file = request.files['photo']
                    if file.filename != '':
                        if file and allowed_file(file.filename):
                            pic = Pictures(bid)
                            id_picture = Pictures.save(pic)
                            picture = str(id_picture)
                            filename = secure_filename(file.filename)
                            picture += "." + filename.rsplit('.', 1)[1].lower()
                            # name = 'adv_' + str(picture)
                            name = str(picture)
                            file.save(os.path.join(UPLOAD_FOLDER, name))
                            # url = os.path.join(UPLOAD_FOLDER + '/' + name)
                            url = name
                else:
                    url = "kek"

                if form.title.data is not None:
                    text = form.title.data
                    textpos = int(form.textpos.data)
                else:
                    text = 'no'
                    textpos = -1
            pages = int(form.pages.data)

            if Widget.if_exist(bid) is False:
                w = Widget(bid, form.type.data, url, text, textpos, pages)
                w.save()
            else:
                upd = Widget.query.filter_by(business_id=bid)
                upd.update({'type': form.type.data})

                if form.type.data == 'game':
                    upd.update({'pages': pages})
                else:
                    upd.update({'url': url})
                    upd.update({'pages': pages})
                    upd.update({'textpos': textpos})
                    upd.update({'text': text})

                db.session.commit()

            return redirect('business/business_card/' + str(bid))

    else:
        return redirect('/business/')


@business.route('/widget', methods=['GET'])
def widget():
    return render_template('widget.html')


@business.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)
