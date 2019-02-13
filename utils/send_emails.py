import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(fromAdd, toAdd, subject, attachfile, htmlText):
    strFrom = fromAdd;
    strTo = toAdd;
    msg = MIMEText(htmlText);
    msg['Content-Type'] = 'Text/HTML';
    msg['Subject'] = Header(subject, 'gb2312');
    msg['To'] = strTo;
    msg['From'] = strFrom;

    smtp = smtplib.SMTP('smtp.qq.com');
    smtp.login('501257367@qq.com', 'password');
    try:
        smtp.sendmail(strFrom, strTo, msg.as_string());
    finally:
        smtp.close;


if __name__ == "__main__":
    SendEmail("501257367@qq.com", "501257367@qq.com", "", "hello", "hello world");
