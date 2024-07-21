import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

def send_email_with_template(template_file: str, link: str, recipient_email: str, subject: str, sender_email: str, sender_password: str):
    # Read the HTML template from file
    with open(template_file, 'r', encoding='utf-8') as file:
        html_template = file.read()
    
    # Parse the HTML template
    soup = BeautifulSoup(html_template, 'html.parser')
    a_tag = soup.find('a', {'class': 'es-button'})
    
    # Replace the href attribute with the provided link
    if a_tag and link != None:
        a_tag['href'] = link

    # Convert the modified HTML back to a string
    modified_html = str(soup)
    
    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Attach the modified HTML to the email
    msg.attach(MIMEText(modified_html, 'html'))
    
    # Send the email using smtplib
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!", recipient_email)
    except Exception as e:
        print(f"Failed to send email: {e}")