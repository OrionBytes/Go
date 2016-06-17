# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import smtplib
from email.mime.text import MIMEText

from tornado.template import Loader
from weiqi import settings

_loader = Loader(os.path.join(settings.BASE_DIR, 'templates', 'mails'))
console_mails = []


def send_mail(to_mail, to_name, subject, template, context):
    subject += ' - weiqi.gs'

    context['recipient_name'] = to_name
    body = _loader.load(template).generate(**context).decode()

    backend = globals()[settings.MAILER['backend'] + '_mailer']
    backend(to_mail, subject, body, template)


def console_mailer(to, subject, body, template=None):
    print('To: %s\nSubject: %s\nBody:\n%s' % (to, subject, body))

    console_mails.append({
        'to': to,
        'subject': subject,
        'body': body,
        'template': template,
    })


def smtp_mailer(to, subject, body, template=None):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.MAILER['from']
    msg['To'] = to

    with smtplib.SMTP(settings.MAILER['smtp_host'], settings.MAILER['smtp_port']) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(settings.MAILER['smtp_user'], settings.MAILER['smtp_password'])
        smtp.sendmail(settings.MAILER['from'], [to], msg.as_string())
