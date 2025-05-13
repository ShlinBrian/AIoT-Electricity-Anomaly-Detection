# Standard Library
import smtplib
from dataclasses import dataclass, field
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import List

# Third Party Library
from loguru import logger

# Local Module
from scheduler.config import COMMON


@dataclass
class MailReport:
    subject: str
    subtype: str
    content: str
    attachment_paths: List[str] = field(default_factory=list)
    image: List[str] = field(default_factory=list)


def multi_mail_report(results: List[MailReport], **kwargs):
    """send multi email report

    Arguments:
        result list[{dict}] -- email results: subject and content

    Keyword Arguments:
        recipient {list} -- email recipients
    """

    for result in results:
        mail_report(result, **kwargs)


def mail_report(result: MailReport, **kwargs):
    """send email report

    Arguments:
        result {dict} -- email results: subject and content

    Keyword Arguments:
        recipient {list} -- email recipients
    """
    if not result.content:
        logger.info('[EMAIL] No result, quit')
        return
    if not kwargs.get('recipient'):
        logger.info('[EMAIL] No recipients, quit')
        logger.info(f'[EMAIL] Results: {result}')
        return
    logger.info('[EMAIL] Generating email')
    recipients = [str(email) for email in kwargs.get('recipient', [])]
    msg = generate_mime(result, recipients)
    logger.info('[EMAIL] Sending email')
    send_mail(msg)
    logger.info('[EMAIL] End')


def generate_mime(result: MailReport, recipient: List[str]) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['Subject'] = result.subject
    msg['From'] = COMMON.mail_account
    msg['To'] = COMMON.mail_account
    msg['BCC'] = ','.join(recipient)

    text = MIMEText(result.content, result.subtype, 'utf-8')
    msg.attach(text)
    for image in result.image:
        f_p = open(image, 'rb')
        msg_image = MIMEImage(f_p.read())
        msg_image.add_header('Content-ID', f'<{image.split("/")[-1]}>')
        msg.attach(msg_image)
        f_p.close()

    for file_path in result.attachment_paths:
        try:
            attachment = build_attachment(file_path)
            msg.attach(attachment)
        except FileNotFoundError as error:
            logger.error(error)
    return msg


def build_attachment(file_path: str) -> MIMEApplication:
    with open(file_path, "rb") as read_file:
        attachment = MIMEApplication(
            read_file.read(), Name=basename(file_path)
        )
    attachment[
        'Content-Disposition'
    ] = f'attachment; filename="{basename(file_path)}"'
    return attachment


def send_mail(msg):
    server = smtplib.SMTP_SSL(COMMON.smtp_host, COMMON.smtp_port)
    server.ehlo()
    server.login(COMMON.mail_account, COMMON.mail_password)
    server.send_message(msg)
    server.quit()
