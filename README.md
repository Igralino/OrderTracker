# OrderTracker

## Introduction

 - OrderTracker - сервис по отслеживанию заказов для бизнеса и его клиентов. Позволяет упростить рабочие процессы и уменьшить время, которое вы тратите на рутинные процессы, связанные с вашим производством.

## About Code
Python+Flask+SQLAlchemy+JS+VK.API+Alice.Dialogs+Bootstap = __OrderTracker__

## Installation

> Если вы попытаетесь установить этот ужас, необходимо сделать следующие вещи:
1) Настроить базу данных PostgreSQL с именем OrderTracker
2) Настроить файл */config.py*
3) Настроить файл */bots/vk_callback/views.py* (VK API)
4) Ввести следующие команды:
``` sh
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade
flask mock
```
___

Данный проект был создан в качестве выпуской работы группы учеников [Московской Школы Программистов] при Яндексе.
Made by:
[QwertygidQ], [Igralino], [А. Соболев], [GareevaAlice], [Arnoir], [karpp], [Floly], [Sid51], [itsvlas], [Saagilat], [AntonyBazin]

[Московской Школы Программистов]: <https://informatics.ru>
[QwertygidQ]: <https://gihub.com/QwertygidQ>
[Igralino]: <https://gihub.com/Igralino>
[А. Соболев]: <https://vk.com/id_alexey2000>
[GareevaAlice]:<https://github.com/GareevaAlice>
[Arnoir]:<https://github.com/Arinoir>
[karpp]:<https://github.com/karpp>
[Floly]:<https://github.com/Floly>
[Sid51]:<https://github.com/Sid51>
[itsvlas]:<https://github.com/itsvlas>
[Saagilat]:<https://vk.com/mkatargin>
[AntonyBazin]:<https://github.com/AntonyBazin>
