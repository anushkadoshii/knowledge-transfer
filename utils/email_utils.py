import os
import re
from dotenv import load_dotenv
from imap_tools import MailBox, AND, OR
import getpass

load_dotenv()

def get_official_email_id(person_name: str, mapping: dict) -> str:
    """
    Fetch the official email ID for a person from a mapping.
    mapping: dict of {name: email}
    """
    return mapping.get(person_name.lower())

def get_email_credentials():
    """
    Securely get email and password (app password for 2FA).
    """
    email = os.getenv('EMAIL_USER') or input("Enter your official email: ")
    password = os.getenv('EMAIL_PASS') or getpass.getpass("Enter your app password (after 2FA): ")
    return email, password

def fetch_company_emails(mailbox, user_email, company_domain):
    """
    Fetch emails sent from company emails to user and from user to company emails.
    """
    # From company to user
    from_company = list(mailbox.fetch(AND(from_=f"@{company_domain}", to=user_email)))
    # From user to company
    to_company = list(mailbox.fetch(AND(from_=user_email, to=f"@{company_domain}")))
    return from_company, to_company

def fetch_emails_with_attachments(mailbox, user_email):
    """
    Fetch all emails to/from user with attachments.
    """
    emails_with_attachments = []
    for msg in mailbox.fetch(OR(from_=user_email, to=user_email)):
        if msg.attachments:
            emails_with_attachments.append(msg)
    return emails_with_attachments

def get_all_relevant_emails(person_name, mapping, company_domain):
    """
    Main function to get all relevant emails as per requirements.
    """
    user_email = get_official_email_id(person_name, mapping)
    if not user_email:
        raise ValueError("Official email not found for this person.")

    email, password = get_email_credentials()

    with MailBox('imap.gmail.com').login(email, password, 'INBOX') as mailbox:
        from_company, to_company = fetch_company_emails(mailbox, user_email, company_domain)
        attachments = fetch_emails_with_attachments(mailbox, user_email)
        return {
            "from_company": from_company,
            "to_company": to_company,
            "with_attachments": attachments
        } 
