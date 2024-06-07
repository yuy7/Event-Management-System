from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
from __init__ import db
from Dao.User import User

app = Flask(__name__)

def send_email(receivers, random_code):
    """发送邮件

    Args:
        receivers (list): 收件人邮箱地址列表
        random_code (int): 生成的验证码

    Returns:
        bool: 邮件是否发送成功
    """
    subject = '验证码'
    content = f'验证码为：{random_code}'
    sender = '1586723707@qq.com'
    password = 'cmgoqhfhkvgojcca'
    try:
        # 构造邮件对象
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(['From nicead.top', sender])
        msg['Subject'] = subject

        # 连接邮箱服务器并登录
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, password)

        # 发送邮件
        for receiver in receivers:
            msg['To'] = formataddr(['FK', receiver])
            server.sendmail(sender, [receiver], msg.as_string())

        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_code():
    data = request.get_json()
    code = data.get('code')
    email = data.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400

    random_code = str(random.randint(100000, 999999))
    user = User.query.filter_by(Email=email).first()

    if user:
        user.VerificationCode = random_code
        # print(user.VerificationCode)
        # print(random_code)
        db.session.commit()
        if send_email([email], random_code):
            return jsonify({'status': 'Email sent successfully',
                            'code': random_code})
        else:
            return jsonify({'error': 'Failed to send email'}), 500
    else:
        return jsonify({'error': 'Email not found'}), 404

