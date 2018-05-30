from flask import render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash

from app import db
from app.models import Process, PossibleProcess, Business, Client, Stage, BusinessCard, Chat, Widget
from . import business_client
from .Forms import OrderForm, StatusEmailForm, CheckBoxForm, RatingForm, FindForm, ForgotPasswordForm


@business_client.route('/', methods=['GET'])
def main():
    return redirect('/business_client/login')


@business_client.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('id', '') != '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    session['id_client'] = ''
    find_form = FindForm()
    business_card_list = BusinessCard.sort_by_rating()[::-1]
    if find_form.submit2.data and find_form.validate_on_submit():
        business_card_list = BusinessCard.find(find_form.words.data)
        if business_card_list[0] == 0:
            find_form.words.errors = ("Ничего не найдено", "")

    form = OrderForm()
    if form.submit.data and form.validate_on_submit():
        number = form.number.data
        password = form.password.data
        if Process.query.all() is None:
            form.password.errors = ('Введён неверный номер заказа или  пароль', '')
        elif Process.query.filter_by(number=number).first() is None:
            form.password.errors = ('Введён неверный номер заказа или  пароль', '')
        elif Process.is_real_number(number) is False:
            form.password.errors = ('Введён неверный номер заказа или  пароль', '')
        else:
            if Process.check_p(Process.get_id(number), password):
                session['id_client'] = Process.get_client_id(Process.get_id(number))
                return redirect(url_for('business_client.status', process_id=Process.get_id(number)))

            else:
                form.password.errors = ('Введён неверный номер заказа или  пароль', '')

    return render_template('business_client_index.html',
                           title='Найти заказ',
                           msg='Введите данные заказа',
                           form=form,
                           find_form=find_form,
                           business_card_list=business_card_list,
                           BusinessCard=BusinessCard,
                           )


@business_client.route('/status/<process_id>', methods=['GET', 'POST'])
def status(process_id):
    if session.get('id', '') != '':
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    elif session.get('id_client', '') == '':
        return redirect('/business_client/login')
    elif Process.get_client_id(process_id) != session.get('id_client', ''):
        return redirect('/business_client/login')

    form_stage = StatusEmailForm()
    form_check = CheckBoxForm()
    form_star = RatingForm()
    starsave = ""
    stagesave = ""
    if form_stage.submit1.data:
        if Process.get_send(process_id):
            rows = Process.query.filter_by(id=process_id).update({'send_all_stages': 0})
            db.session.commit()
        else:
            rows = Process.query.filter_by(id=process_id).update({'send_all_stages': 1})
            db.session.commit()

        stagesave = "Изменения были сохранены"

    if form_star.submit2.data:
        rows = Process.query.filter_by(id=process_id).update({"star": form_star.star.data})
        db.session.commit()
        starsave = "Спасибо за оценку"
    rating = Process.get_star(process_id)
    form_check.checkbox.data = False
    send_stages = Process.get_send(process_id)
    number = Process.get_number(process_id)
    client_email = Client.get_email(Process.get_client_id(process_id))
    business_name = Business.get_name(Process.get_business(process_id))
    data = Process.get_data(process_id).strftime("%B %d, %Y")
    type = PossibleProcess.get_type(Process.get_type_id(process_id))
    desc_type = PossibleProcess.get_desc(Process.get_type_id(process_id))
    desc = Process.get_desc(process_id)

    percent = Process.get_percent(process_id)
    current_stage = Process.get_stages(process_id)
    current_stage_name = Process.get_stage_name(current_stage)
    client_id = Process.get_client_id(process_id)
    price = Process.get_price(process_id)

    business_id = Process.get_business(process_id)

    business_card_exists = BusinessCard.is_real(Process.get_business(process_id))

    # получение всех стадий процесса
    stages = Stage.sort_by_id_for_business(Process.get_type_id(process_id))

    chat = Chat.get_by_proc(process_id).id
    is_picture = (PossibleProcess.get_picture(Process.get_type_id(process_id)) != "-1")
    picture = PossibleProcess.get_picture(Process.get_type_id(process_id))
    return render_template('Status.html',
                           title='Статус заказа',
                           number=number,
                           client_email=client_email,
                           business_name=business_name,
                           type=type,
                           desc=desc,
                           desc_type=desc_type,
                           percent=percent,
                           data=data,
                           current_stage=current_stage,
                           current_stage_name=current_stage_name,
                           stages=stages,
                           price=price,
                           business_id=business_id,
                           form_stage=form_stage,
                           form_check=form_check,
                           send_stages=send_stages,
                           form_star=form_star,
                           rating=rating,
                           starsave=starsave,
                           stagesave=stagesave,
                           business_card_exists=business_card_exists,
                           client_id=client_id,
                           chat=chat,
                           is_picture=is_picture,
                           picture=picture,
                           Widget=Widget)


@business_client.route('/client_process_list/<client_id>', methods=['GET', 'POST'])
def client_process_list(client_id):
    if session.get('id', '') != '':
        if Business.query.filter_by(id=session.get('id', '')).first() is None:
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    elif session.get('id_client', '') == '':
        return redirect('/business_client/login')
    elif int(client_id) != int(session.get('id_client', '')):
        return redirect('/business_client/login')
    process_list = Client.get_processes(client_id)
    form = FindForm()
    if form.validate_on_submit():
        process_list = Process.find_for_client(form.words.data, client_id)
        if process_list[0] == 0:
            form.words.errors = ("Ничего не найдено", "")
    return render_template('client_process_list.html',
                           title='Ваши заказы',
                           form=form,
                           processes=process_list[::-1],
                           client_id=client_id,
                           PossibleProcess=PossibleProcess,
                           Business=Business,
                           Process=Process)


@business_client.route('/bot_handle/<process_number>', methods=['GET', 'POST'])
def get_st(process_number):
    if session.get('id', '') != '':
        if Business.query.filter_by(id=session.get('id', '')).first() is None:
            session['id'] = ''
        return redirect('/business/profile_business')
    print(process_number)
    try:
        current_stage = Process.get_stages(Process.get_id(process_number))
    except:
        return ("Заказ с данным номером не существует")
    current_stage_name = Process.get_stage_name(current_stage)

    return ("Заказ " + "находится в стадии \"" + str(current_stage_name) + "\"")


@business_client.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@business_client.route('/forgot_password_client', methods=['GET', 'POST'])
def forgot_password_client():
    if session.get('id', '') != '':
        if not Business.check_confirmed(session.get('id', '')):
            session['id'] = ''
        return redirect(url_for('business.business_card', business_id=session.get('id', '')))
    session['id_client'] = ''

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        if Process.query.filter_by(number=form.number.data).first():
            client_password = Client.random_password(10)
            rows = Process.query.filter_by(id=Process.get_id(form.number.data)).update(
                {'password': generate_password_hash(client_password)})
            db.session.commit()

            Business.send_password_client(Client.get_email(Process.get_client_id(Process.get_id(form.number.data))),
                                          form.number.data, client_password)

            return redirect(
                "/business/feedback/Мы отправили вам новый пароль на почту! Если вы не получили письмо, \
                проверьте, что вы написали номер правильно!")

        else:
            form.number.errors = ('Неправильный номер', '')

    return render_template('forgot_password_client.html', title='Забыли пароль?', form=form)
