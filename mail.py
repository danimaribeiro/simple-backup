'''
Created on 14/10/2013

@author: Danimar
'''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_email(from_, to_ , subject, html):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to_

    content = MIMEText(html, 'html')
    msg.attach(content)
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("", "")
    server.sendmail(from_, to_, msg.as_string())
    server.quit()
    