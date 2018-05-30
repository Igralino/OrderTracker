import datetime
import re

from flask import render_template, abort, request, session, jsonify

from app import db
from app.models import Chat as chat_model, Letter
from . import Chat


@Chat.route('/')
def testchat():
    return render_template('chat_mail.html', chat_id=1)


@Chat.route('/<chat_id>')
def chat(chat_id):
    return render_template('chat_mail.html', chat_id=chat_id)


@Chat.route('/get', methods=['POST'])
def get_messages():
    chat_id = request.form['chat_id']
    if not chat_model.can_write(chat_id):
        abort(400)
    try:
        last_msg_id = int(request.form['letter_id'])
    except ValueError:
        abort(400)

    letters = sorted(chat_model.get_messages(chat_id), key=lambda x: x.create_time)
    ans = [{'id': msg.id, 'text': msg.text, 'is_business': msg.is_business} for msg in letters if msg.id > last_msg_id]
    chat_model.see_all(chat_id, is_business=(not bool(session.get('id', False))))
    return jsonify(new_messages=ans)


@Chat.route('/get_unread', methods=['POST'])
def get_unread():
    if not bool(session.get('id', False)):
        abort(400)
    business_id = request.form['business_id']
    letters = chat_model.get_unread_messages(business_id)

    ans = []

    for msg in letters:
        if msg.create_time + datetime.timedelta(minutes=5) > datetime.datetime.now() and msg.chat.business_id == int(
                business_id):
            msg.is_delivered = True
            ans.append({'text': msg.text, 'chat': msg.chat_id, 'process': msg.chat.process_id})
    db.session.commit()

    return jsonify(new_messages=ans)


@Chat.route('/post', methods=['POST'])
def post_message():
    chat_id = request.form['chat_id']

    if not chat_model.can_write(chat_id):
        abort(400)

    msg = str(request.form['letter_id'])
    is_business = bool(session.get('id', False))

    regexp = re.compile('\<[^>]*\>')
    if len(re.findall(regexp, msg)) > 0:
        msg = '&#9731;' + msg

    msg = msg.replace('<', '&lt;')
    msg = msg.replace('>', '&gt;')

    letter = Letter(int(chat_id), msg, is_business)
    letter.save()

    return jsonify(id=letter.id)
