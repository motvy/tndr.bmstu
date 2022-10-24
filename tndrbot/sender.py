import smtplib
import re

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()

smtpObj.login('abragqwery123@gmail.com','zuusppenzmjcbavk')

re.match(r'^\w*@student.bmstu.ru$', '')

message = MIMEMultipart("alternative")
message["Subject"] = "Код подтверждения BMSTU.TNDR"
message["From"] = 'abragqwery123@gmail.com'
message["To"] = 'tme20u797@student.bmstu.ru'

# text = """\
# Привет!
# Как у Вас дела?"""
 
# html = """\
# <html>
#   <body>
#     <p>Привет!<br>
#        Как у Вас <strong>дела</strong>?
#     </p>
#   </body>
# </html>
# """
html = """\
<html>
    <body style="background-color: #dbc5d5">
        <center>
            <!-- <img src="https://fikiwiki.com/uploads/posts/2022-02/1644855676_21-fikiwiki-com-p-kartinki-khd-kachestva-21.jpg" /> -->
            <strong>Привет, Матвей!</strong>
            <p>Код подтверждения:<br>
                <strong>1234</strong>
            </p>
            <p><i>Этот код используется только для подтверждения регистрации в BMSTU.TNDR. Он не нужен для чего-то еще. 
                Никому не давайте код, даже если его требуюь от имени Telegram.
            </i></p>
            <p>Если вы не запрашивали код подтверждения, проигнорируйте это сообщение.</p>
            <strong>С уважением,<br>Команда BMSTU.TNDR</strong>
        </center>  
    </body>
</html>
"""
 
# Сделать их текстовыми\html объектами MIMEText
# part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# message.attach(part1)
message.attach(part2)

# text = """\
# Subject: Код подтверждения BMSTU.TNDR
 
# Это письмо было отправлено из Python."""

# print(text)
# text = text.encode('utf-8')
# tme20u797@student.bmstu.ru
smtpObj.sendmail("abragqwery123@gmail.com","tme20u797@student.bmstu.ru", message.as_string())

