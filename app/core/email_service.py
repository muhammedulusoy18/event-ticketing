import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings
from app.models.tickets import Tickets


def send_reset_password_email(email_to:str,token:str):
    msg = MIMEMultipart()
    msg["From"] = settings.MAIL_FROM
    msg["To"] = email_to
    msg["Subject"] = "Şifre sıfırlama isteği 🔒 "
    link=f"http://localhost:8000/auth/resetpassword?token={token}"
    html=f"""
    <html>
        <body>
            <p>Merhaba,<p>
            <p>Şifrenizi sıfırlamak için aşağıdaki butona tıklayın:</p>
            <a href="{link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none;">Şifremi Sıfırla</a>
            <p>Bu link 15 dakika geçerlidir.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))
    with  smtplib.SMTP(settings.MAIL_SERVER,settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_FROM,settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM,email_to,msg.as_string())
def send_ticket_confirmation_mail(email_to:str,ticket_data:dict):
    msg = MIMEMultipart()
    msg["From"] = settings.MAIL_FROM
    msg["To"] = email_to
    msg["Subject"]=f"biletiniz onaylandı 🎫 -{ticket_data['event_name']}"
    html=f"""
<html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
                <h2 style="color: #4CAF50; text-align: center;">Biletiniz Hazır!</h2>
                <hr>
                <p>Merhaba,</p>
                <p><b>{ticket_data['event_name']}</b> etkinliği için biletiniz başarıyla oluşturuldu.</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><b>Bilet Numarası:</b> #{ticket_data['ticket_id']}</p>
                    <p style="margin: 5px 0;"><b>Adet:</b> {ticket_data['quantity']} Kişilik</p>
                    <p style="margin: 5px 0;"><b>Tarih:</b> {ticket_data['purchase_date']}</p>
                </div>

                <p style="text-align: center; color: #888; font-size: 12px;">
                    Bu bilet otomatik olarak oluşturulmuştur. Lütfen etkinlik girişinde bu e-postayı yanınızda bulundurun.
                </p>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP(settings.MAIL_SERVER,settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_FROM,settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM,email_to,msg.as_string())
