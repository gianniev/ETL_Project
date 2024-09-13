import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow.models import Variable 


def send_email(**context): 
    subject = Variable.get("subject_mail")
    from_address = Variable.get("email")
    password = Variable.get("email_password")
    to_address = Variable.get("to_address").split(", ") # Seprar la lista de correos

    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ", ".join(to_address) # Unir direcciones
    msg['Subject'] = subject

    # Create HTML content
    html_content = f"""
    <html>
    <body>
        <p>Hola!</p>
        <p>El proceso de extración de datos desde la API de Coinmarketcap ha sido cargada en la tabla dentro de Redshift exitosamente</p>
    </body>
    </html>
    """

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Create an SMTP SESSION
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to the server
        server.login(from_address, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email enviado correctamente.")
    except Exception as e:
        print(f"Faileed to send email: {str(e)}")
        

