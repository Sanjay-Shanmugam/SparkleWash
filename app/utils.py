from twilio.rest import Client
import os

def send_sms(to_number, body):
    """
    Sends an SMS using Twilio.
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')

    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials not found. SMS not sent.")
        print(f"Mock SMS to {to_number}: {body}")
        return

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"SMS sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
