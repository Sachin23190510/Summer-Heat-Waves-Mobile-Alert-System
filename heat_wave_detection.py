import pandas as pd
from twilio.rest import Client

def detect_heatwaves(data, temp_column='Data.Temperature.Max Temp', date_column='Date.Full', threshold=30, consecutive_days=3):
    data['heatwave'] = False
    count = 0

    for i in range(len(data)):
        if data[temp_column].iloc[i] > threshold:
            count += 1
        else:
            count = 0

        if count >= consecutive_days:
            data.loc[i, 'heatwave'] = True

    return data

def send_sms(to, message):
    account_sid = 'Your Sid_Account_Number'
    auth_token = 'Your Auth_Token_Number'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='Your Verified Twilio Number',
        to='Sending Number')

    print(f"Message sent to {to}: {message.sid}")

data = pd.read_csv('historical_temperature_data.csv')
data.columns = data.columns.str.strip()
print("Cleaned columns:", data.columns.tolist())

data = detect_heatwaves(data)

for index, row in data.iterrows():
    if row['heatwave']:
        print(f"Heatwave detected on {row['Date.Full']} with temperature {row['Data.Temperature.Max Temp']} °C.")
        # send_sms('Sending Number', f"Heatwave detected on {row['Date.Full']} with temperature {row['Data.Temperature.Max Temp']} °C.")
