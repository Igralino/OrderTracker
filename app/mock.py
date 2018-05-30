from app.models import Business, PossibleProcess, Stage, Client, Process, BusinessCard, Comments, Pictures, Widget
from . import app, db


# noinspection PyArgumentList
@app.cli.command()
def mock():
    db.drop_all()
    db.create_all()

    # Первый бизнес

    business = Business(name="Туристическое агенство Маленький Принц", password="qweqwe",
                        email="qwe@gmail.com", confirmed=True)
    Business.save(business)

    # возможная услуга для первого бизнеса
    process = PossibleProcess("Помощь выбора путёвки", "Подбор идеального места для отдыха", 1, "10000")
    pr_id = process.save()

    stage_not_started = Stage("Не начат", 1)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 1)
    stage_finished.save()

    # стадии для этой услуги
    stage = Stage("Анкетирование", 1)
    stage.save()

    stage = Stage("Диалог с клиентом", 1)
    stage.save()

    stage = Stage("Покупка путёвки", 1)
    stage.save()

    Stage.fix_not_finished(1)

    # созданный заказ для первой услуги
    client = Client('client1@gmail.com')
    client.save()

    process = Process(1, 'Подбор идеального места для отдыха', 1, 1, "AAAAAA-AAAAAA", "10000", "qweqwe")
    process.save()

    # вторая возможная услуга для первого бизнеса
    process = PossibleProcess("Собственная экскурсия",
                              "Создание экскурсии спецально по персональным требованиям клиента", 1, "20000")
    pr_id = process.save()

    # стадии для этой услуги
    stage_not_started = Stage("Не начат", 2)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 2)
    stage_finished.save()

    stage = Stage("Диалог с клиентом", 2)
    stage.save()

    stage = Stage("Поиск экукурсоводов", 2)
    stage.save()

    stage = Stage("Создание программы экскурсии", 2)
    stage.save()

    Stage.fix_not_finished(2)

    pic = Pictures(1)
    id_picture = Pictures.save(pic)
    picture = "2.jpeg"
    rows = Pictures.query.filter_by(id=id_picture).update({'picture': picture})
    rows = PossibleProcess.query.filter_by(id=2).update({'picture': picture})
    db.session.commit()

    # созданный заказ для второй услуги
    client = Client('client2@gmail.com')
    client.save()

    process = Process(2, 'Предпочитает картинные галереи', 1, 2, "BBBBBB-BBBBBB", "20000", "asdasd")
    process.save()

    rows = Process.query.filter_by(id=2).update({'current_stage': 9})
    rows = Process.query.filter_by(id=2).update({'percent': round(45)})
    db.session.commit()

    # создать страницу первого бизнеса
    card = BusinessCard("Туристическое агенство Маленький Принц",
                        "Поможем Вам найти место для идеального препровождения", "Телефон: +7(924)732-90-65",
                        "метро Добрынинская", 1)
    BusinessCard.save(card)

    pic = Pictures(1)
    id_picture = Pictures.save(pic)
    picture = "1.jpg"
    rows = Pictures.query.filter_by(id=id_picture).update({'picture': picture})
    rows = BusinessCard.query.filter_by(business_id=1).update({'picture': picture})
    db.session.commit()

    # создать комментарии к бизнесу
    comments = Comments(
        "Очень доволен фирмой! Крайне приятный персонал: были вежливы и очень быстро мне подобрали место для отдыха", 1,
        1, "Александр", 5)
    Comments.save(comments)
    # еще один
    comments = Comments("Всё, конечно, хорошо, но с местом немного прогадали. Но никаких особых претензий нет", 2, 1,
                        "Анастасия", 1)
    Comments.save(comments)

    rating = BusinessCard.get_new_rating(1)
    rows = BusinessCard.query.filter_by(business_id=1).update(
        {'rating': rating})
    db.session.commit()

    # Второй бизнес

    business = Business(name="Общество историков 1984", password="asdasd",
                        email="asd@gmail.com", confirmed=True)
    Business.save(business)

    # возможная услуга для второго бизнеса
    process = PossibleProcess("Подготовка к ЕГЭ", "Курсы по подготовке к ЕГЭ по истории", 2, "30000")
    pr_id = process.save()

    stage_not_started = Stage("Не начат", 3)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 3)
    stage_finished.save()

    # стадии для этой услуги
    stage = Stage("Первый триместр", 3)
    stage.save()

    stage = Stage("Второй триместр", 3)
    stage.save()

    stage = Stage("Третий триместр", 3)
    stage.save()

    Stage.fix_not_finished(3)

    # созданный заказ для первой услуги
    client = Client('client3@gmail.com')
    client.save()

    process = Process(3, 'Курсы по подготовки к ЕГЭ по истории', 2, 3, "CCCCCC-CCCCCC", "30000", "zxczxc")
    process.save()

    # вторая возможная услуга для второго бизнеса
    process = PossibleProcess("Консультирование", "Помощь в написании курсовой/докторской и прочих работ", 2, "40000")
    pr_id = process.save()

    stage_not_started = Stage("Не начат", 4)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 4)
    stage_finished.save()

    # стадии для этой услуги
    stage = Stage("Первая встреча", 4)
    stage.save()

    stage = Stage("Поиск информации", 4)
    stage.save()

    stage = Stage("Консультирование", 4)
    stage.save()

    Stage.fix_not_finished(4)

    # созданный заказ для второй услуги

    process = Process(4, 'Помощь в написании курсовой/докторской и прочих работ', 2, 1, "DDDDDD-DDDDDD", "40000",
                      "werwer")
    process.save()

    business = Business(name="Как у бабушки", password="zxczxc",
                        email="zxc@gmail.com", confirmed=True)
    Business.save(business)

    w = Widget(-1, 'game', 'http://0.0.0.0:8080/business/widget', 'game', 1, 3)
    w.save()

    # возможная услуга для 3 бизнеса
    process = PossibleProcess("Домашняя пицца", "Сделанная дома пицца по рецепту моей бабушки", 3, "50000")
    pr_id = process.save()

    stage_not_started = Stage("Не начат", 5)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 5)
    stage_finished.save()

    # стадии для этой услуги
    stage = Stage("Приготовление пиццы", 5)
    stage.save()

    stage = Stage("Упаковка пиццы", 5)
    stage.save()

    stage = Stage("Доставка", 5)
    stage.save()

    Stage.fix_not_finished(5)

    process = Process(5, 'Сделанная дома пицца', 3, 1, "EEEEEE-EEEEEE", "30000", "sdfsdf")
    process.save()

    # вторая возможная услуга для второго бизнеса
    process = PossibleProcess("Домашняя шаурма", "Сделанная дома шаурма по-моему рецепту", 3, "40000")
    pr_id = process.save()

    stage_not_started = Stage("Не начат", 6)
    stage_not_started.save()
    stage_finished = Stage("Закончен", 6)
    stage_finished.save()

    # стадии для этой услуги
    stage = Stage("Приготовление шаурмы", 6)
    stage.save()

    stage = Stage("Упаковка", 6)
    stage.save()

    stage = Stage("Доставка", 6)
    stage.save()

    Stage.fix_not_finished(6)

    process = Process(6, 'Сделанная дома шаурма', 3, 1, "FFFFFF-FFFFFF", "40000", "xcvxcv")
    process.save()

    process = Process(2, 'Детская экскурсия', 1, 2, "GGGGGG-GGGGGG", "25000", "ertert")
    process.save()

    rows = Process.query.filter_by(id=7).update({'current_stage': 7})
    rows = Process.query.filter_by(id=7).update({'percent': round(100)})
    db.session.commit()

    print('Success')
