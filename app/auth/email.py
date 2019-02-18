from flask import render_template, current_app

from app.mail import send_email


def send_password_reset_email(user):
    token = user.get_user_id_token()
    send_email('[Pew!] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_email_activate_email(user):
    token = user.get_user_id_token(60 * 60 * 24)
    send_email('[Pew!] Confirm Your Email',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, token=token))
