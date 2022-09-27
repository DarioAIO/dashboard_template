import smtplib

def send_email(email, email_code): 
    try:
        body = 'Subject: Password Reset\n' + f'\nhttp://127.0.0.1:8000/reset?code={email_code}&email={email}'
        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception as e:
            print(e)
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('dashboard.api@outlook.com', "Password4567?!") 
        smtpObj.sendmail('dashboard.api@outlook.com', email, body)

        smtpObj.quit()
        return True
    except Exception:
        return False    