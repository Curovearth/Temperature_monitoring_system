import conf
import json,time
from boltiot import Bolt,Sms

#temperature range in degree celsius
max_limit=38
min_limit=30

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms=Sms(conf.SID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)

while True:
    print('READING THE RESPONSE')
    response=mybolt.analogRead('A0')
    data=json.loads(response)
    print('Sensor Value is '+str(data['value']))

    try:
        sensor_value=int(data['value'])
        temperature=str(sensor_value*100/1024)
        temp=float(temperature)
        print('Sensor Value in degree celsius is',str(temp))


        if temp>max_limit or temp<min_limit:
            print('Making a request to Twilio to send SMS')

            response=sms.send_sms("WARNING! CURRENT TEMPERATURE VALUE IS {0} CELSIUS. Have a look urgently".format(str(temp)))
            print('Response received from Twilio is: '+str(response))
            print('Status of SMS Twilio is: '+str(response.status))

    except Exception as e:
        print('Some error occurred')
        print(e)
    time.sleep(5)