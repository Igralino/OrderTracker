# OrderTracker Project

## Introduction

> OrderTracker - сервис по отслеживанию заказов для бизнеса и его клиентов. Позволяет упростить рабочие процессы и 
уменьшить время, которое вы тратите на рутинные процессы, связанные с вашим производством.

## About Code

> Блокчейн, бигдата, VueJS, NodeJS - это не про нас.

> А вот Flask, PostgreSQL и Bootstrap - пожалуйста.


## Installation

> Если вы попытаетесь установить этот ужас, необходимо сделать следующие вещи:
>> 1) Настроить базу данных PostgreSQL с именем OrderTracker
>> 2) Ввести следующие команды:
```
virtualenv --python=python3 venv
source venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade

flask mock
```
