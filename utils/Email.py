import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.charset import Charset, BASE64
from email.mime.nonmultipart import MIMENonMultipart
from email import charset

from models.Billing import Billing as BillingModel

class Email:
    """ Email Class """

    def __init__(self):
        self.sender = 'secret.sasquatch.society1@gmail.com'
        self.name = 'NTU Inventory Store'
        self.recipients = None
        self.subject = 'Inventory Store'
        self.credentials = {
            'username': 'username',
            'password': 'password',
            'host': 'email-smtp.eu-west-1.amazonaws.com',
            'port': 587
        }

    def set_recipients(self, recipients):
        self.recipients = recipients
        return self

    def set_subject(self, subject):
        self.subject = subject
        return self

    def send_finance_report(self, month, year):
        month_name = BillingModel.get_billing_month_name(month)
        self.set_subject(f'Monthly Finance Report {month_name} {year}')
        BODY_HTML = f"""<html>
                    <body>
                    <h1>Finance Report</h1>
                    <p>Please find attached the finance report for {month_name} {year}</p>
                    </body>
                    </html>
                    """
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = email.utils.formataddr((self.name, self.sender))
        if isinstance(self.recipients, list):
            msg['To'] = ', '.join(self.recipients)
        else:
            msg['To'] = self.recipients
        msg.attach(MIMEText(BODY_HTML, 'html'))

        results = BillingModel.get_department_billing(year, month)
        department_billing ='Department,Total\n'
        for row in results:
            department_billing += '{},{}\n'.format(
                row.get_department_code(), row.get_total()
            )
        
        attachment = MIMENonMultipart('text', 'csv', charset='utf-8')
        attachment.add_header('Content-Disposition', 'attachment', 
            filename=f'finance_report_{month_name}_{year}.csv')
        cs = Charset('utf-8')
        cs.body_encoding = BASE64
        attachment.set_payload(department_billing.encode('utf-8'), charset=cs)
        msg.attach(attachment)

        info = self.send_email(msg.as_string())
        return info
        
    def send_email(self, message):
        info = ''
        try:  
            server = smtplib.SMTP(
                self.credentials['host'],
                self.credentials['port'])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(
                self.credentials['username'], 
                self.credentials['password'])
            server.sendmail(self.sender, self.recipients, message)
            server.close()
        except Exception as e:
            info = f'Error sending email: {e}'
        else:
            info = 'Successfully sent email'
        return info