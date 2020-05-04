from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl

app = Flask(__name__)


@app.route('/')
def top():
    return render_template('home.html')


@app.route('/myself')
def myself():
    return render_template('self.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        if (not name) or (not email) or (not content):
            message = "必須項目に入力がありません。"
            return render_template('form.html', name=name, email=email,
                                   content=content, message=message)
        else:
            FROM_ADDRESS = 'kanauchi.form@gmail.com'
            MY_PASSWORD = 'mysite_password123'
            TO_ADDRESS = 'thwkana@gmail.com'
            BCC = ''
            SUBJECT = 'お問い合わせ'
            BODY = name + "さん\n" + "email:" + email + '\n' + content
            msg = MIMEText(BODY)
            msg['Subject'] = SUBJECT
            msg['From'] = FROM_ADDRESS
            msg['To'] = TO_ADDRESS
            msg['Bcc'] = BCC
            msg['Date'] = formatdate()

            smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
            smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
            smtpobj.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_string())
            smtpobj.close()

            BODY = f'{name}様、お問い合わせありがとうございます。\n\n東京情報クリエイター工学院専門学校の叶内です。' \
                   '\n' \
                   '\n内容を確認次第、3日以内に追ってこちらから連絡いたします。\n' \
                   '\n' \
                   '以下お問い合わせ内容\n' + '"""\n' +content + '\n"""'
            TO_ADDRESS = email
            msg = MIMEText(BODY)
            msg['Subject'] = SUBJECT
            msg['From'] = FROM_ADDRESS
            msg['To'] = email
            msg['Bcc'] = BCC
            msg['Date'] = formatdate()
            smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
            smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
            smtpobj.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_string())
            smtpobj.close()
            return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)