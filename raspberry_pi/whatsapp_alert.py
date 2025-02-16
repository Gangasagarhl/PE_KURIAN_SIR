from twilio.rest import Client

def send_whatsapp_alert(body="Hi sagu"):


    account_sid = "AC138c0035f0e1f14a5c4f0bcce8eb123d"
    auth_token  =  "f4167296caea44528ac4be2800153d6a"
    client = Client(account_sid, auth_token)


    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Twilio Sandbox WhatsApp number
        body=body,
        to='whatsapp:+918105114611'        # Destination WhatsApp number (update accordingly)
    )
    
    
    print(message.sid)
    
    return message.sid


