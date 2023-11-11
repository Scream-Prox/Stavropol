 # Кейс распознавание действий человека по видео

> Разработать модель для предсказания действий человека по видео с интеграцией ее в веб-сервис.

## Команда: QuasWexExort


**Мы предлагаем:**

- MVP продукт в виде функционирующего веб-сервиса
- Высокую точность работы модели
- Адаптивность обучающего кода

**Основной функционал:**

- Выбор видео на своем устройстве
- Обработка видео с помощью обученной модели
- Предсказание метки о действиях человека на видео

**Краткое описание**: 

Веб-сервис позволяет выбрать видео с вашего устройства, обработать его с помощью обученной модели и вывести на экран результат о действиях человека на видео 

**Инструкция использования**:

Нажимаем на кнопку выбрать файл 

<img src="rzdai\static\images\first.png" height="300">

Выбираем видео из директории
<img src="rzdai\static\images\second.png" height="300">

Нажимаем кнопку обработать видео и ждем пока модель отработает
<img src="rzdai\static\images\third.png" height="300">

И наблюдаем результат
<img src="rzdai\static\images\fourth.png" height="300">


Для тестирования веб-сервиса:

```
    git clone https://github.com/Scream-Prox/Stavropol.git
    
    Скачайте веса модели по ссылке:
    https://disk.yandex.ru/d/qKf0BJQQnfBi6g

    Добавьте файл весов моделей в папку qwehacks

    Для запуска сервера наберите в терминал:
    python manage.py runserver
    
    
```
