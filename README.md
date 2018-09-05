# Sites Monitoring Utility

Скрипт анализирует url-адреса из указанного текстового файла и выводит информацию о доступности и статусе истечения доменных имен.

Доступность домена:
```
HTTP-status: OK
```
- **OK** - нормальное состояние адреса. Ресурс доступен по этому адресу и успешно загружается
- **Connection error** - домен недоступен

Статус истечения домена:
```
Domain expiration: Not expired
```
- **Not expired** - истекает более чем через 30 дней
- **Expires** - до конца действия доменного имени осталось менее 30 дней или он уже истёк

# Предварительные настройки

- Установить и запустить [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для Python
- Установить дополнительные пакеты:
```
pip install -r requirements.txt
```
- Подготовить текстовый файл со списком адресов в формате:
```
http://ya.ru
http://yandex.ru/
http://market.yandex.ru/
```

# Как запустить

Скрипт требует для своей работы установленного интерпретатора **Python** версии **3.5**.

**Запуск на Linux**

```bash
$ python check_sites_health.py urls.txt # или python3, в зависимости от настроек системы

# результат выполнения скрипта
Url: http://ya.ru
HTTP-status: OK
Domain expiration: Not expired in 30 days

# если url указан в неверном формате:
Invalid URL: ya.ru

```

Запуск на **Windows** происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
