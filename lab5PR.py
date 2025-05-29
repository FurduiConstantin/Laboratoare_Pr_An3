import poplib
import imaplib
import email
from email.parser import BytesParser
from email.message import EmailMessage
import smtplib
import os

GMAIL_USER = "furduicostel04@gmail.com"
GMAIL_APP_PASSWORD = "jbrbifemxtnjgpfv"

# --- POP3 cu recent mode ---
def list_emails_pop3():
    print("Conectare POP3...")
    pop_conn = poplib.POP3_SSL('pop.gmail.com', 995)
    pop_conn.user('recent:' + GMAIL_USER)  # recent mode activat
    pop_conn.pass_(GMAIL_APP_PASSWORD)
    numMessages = len(pop_conn.list()[1])
    print(f"Număr emailuri în POP3: {numMessages}")
    for i in range(min(numMessages, 5)):
        response, lines, octets = pop_conn.retr(i+1)
        msg_data = b"\r\n".join(lines)
        msg = BytesParser().parsebytes(msg_data)
        print(f"Email {i+1}: From: {msg['From']}, Subject: {msg['Subject']}")
    pop_conn.quit()

# --- IMAP listare emailuri ---
def list_emails_imap():
    print("Conectare IMAP...")
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    imap_conn.select('INBOX')

    typ, data = imap_conn.search(None, 'ALL')
    mail_ids = data[0].split()
    print(f"Număr emailuri în IMAP: {len(mail_ids)}")

    for i in mail_ids[-5:]:
        typ, msg_data = imap_conn.fetch(i, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                print(f"Email ID {i.decode()}: From: {msg['From']}, Subject: {msg['Subject']}")
    imap_conn.logout()

# --- Descărcare email cu atașamente ---
def download_attachments():
    print("Descărcare atașamente de la ultimul email...")
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    imap_conn.select('INBOX')
    typ, data = imap_conn.search(None, 'ALL')
    mail_ids = data[0].split()
    if not mail_ids:
        print("Inbox gol.")
        imap_conn.logout()
        return

    latest_id = mail_ids[-1]
    typ, msg_data = imap_conn.fetch(latest_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            for part in msg.walk():
                content_disposition = part.get("Content-Disposition")
                if content_disposition and "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filepath = os.path.join(".", filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Salvat atașament: {filename}")
    imap_conn.logout()

# --- Trimitere email simplu ---
def send_simple_email(to_address):
    msg = EmailMessage()
    msg['From'] = GMAIL_USER
    msg['To'] = to_address
    msg['Subject'] = "Test Email Simplu"
    msg.set_content("Acesta este un email trimis din Python, fără atașamente.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    print("Email simplu trimis.")

# --- Trimitere email cu atașament ---
def send_email_with_attachment(to_address, filepath):
    msg = EmailMessage()
    msg['From'] = GMAIL_USER
    msg['To'] = to_address
    msg['Subject'] = "Test Email cu Atașament"
    msg['Reply-To'] = GMAIL_USER
    msg.set_content("Acesta este un email trimis din Python cu atașament.")

    with open(filepath, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(filepath)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    print("Email cu atașament trimis.")

# --- Program principal ---
if __name__ == "__main__":
    list_emails_pop3()
    list_emails_imap()
    download_attachments()
    send_simple_email("ion.gatman1@isa.utm.md") 
    if os.path.exists("test.txt"):
        send_email_with_attachment("ion.gatman1@isa.utm.md", "test.txt")  
    else:
        print("Fișierul test.txt nu există, nu s-a trimis email cu atașament.")
