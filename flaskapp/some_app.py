print("Hello world!")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
return " <html><head></head> <body> Hello World! </body></html>"
if __name__ == "__main__":
app.run(host='127.0.0.1',port=5000)
from flask import render_template
#наша новая функция сайта
@app.route("/data_to")
def data_to():
#создаем переменные с данными для передачи в шаблон
some_pars = {'user':'Ivan','color':'red'}
some_str = 'Hello my dear friends!'
some_value = 10
#передаем данные в шаблон и вызываем его
return render_template('simple.html',some_str = some_str, some_value = some_value,some_pars=some_pars)

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdBnmAbAAAAAB0b2mX--VpTO2HXgKsuZ0P7uah0'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdBnmAbAAAAALz1oAGdUHsn6ejg3Z2fOoBR-qni'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
# поле для введения строки, валидируется наличием данных
# валидатор проверяет введение данных после нажатия кнопки submit
# и указывает пользователю ввести данные если они не введены
# или неверны
openid = StringField('openid', validators = [DataRequired()])
# поле загрузки файла
# здесь валидатор укажет ввести правильные файлы
upload = FileField('Load image', validators=[
FileRequired(),
FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
# поле формы с capture
recaptcha = RecaptchaField()
#кнопка submit, для пользователя отображена как send
submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet
# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
# создаем объект формы
form = NetForm()
# обнуляем переменные передаваемые в форму
filename=None
neurodic = {}
# проверяем нажатие сабмит и валидацию введенных данных
if form.validate_on_submit():
# файлы с изображениями читаются из каталога static
filename = os.path.join('./static', secure_filename(form.upload.data.filename))
fcount, fimage = neuronet.read_image_files(10,'./static')
# передаем все изображения в каталоге на классификацию
# можете изменить немного код и передать только загруженный файл
decode = neuronet.getresult(fimage)
# записываем в словарь данные классификации
for elem in decode:
neurodic[elem[0][1]] = elem[0][2]
# сохраняем загруженный файл
form.upload.data.save(filename)
# передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
# сети если был нажат сабмит, либо передадим falsy значения
return render_template('net.html',form=form,image_name=filename,neurodic=neurodic)

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
# метод для обработки запроса от пользователя
@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
neurodic = {}
# проверяем что в запросе json данные
if request.mimetype == 'application/json':
# получаем json данные
data = request.get_json()
# берем содержимое по ключу, где хранится файл
# закодированный строкой base64
#
