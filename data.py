import random as r
import json

import os
from Pubnub import Pubnub

PUBNUB_PUBLISH_KEY = os.environ['pub-c-39e01c3f-2068-40cc-90a3-abcffd8d54da']
PUBNUB_SUBSCRIBE_KEY = os.environ['sub-c-b4d2f71e-cf66-11e4-95a3-0619f8945a4f']
PUBNUB_SECRET_KEY = os.environ['sec-c-MDIyYjE4YjEtMDRhMy00ZjFhLWE0Y2ItOWZmODQ3ZGFlZTky']

CHANNEL = "k_channel"

if __name__ == "__main__":
    pubnub = Pubnub(publish_key=PUBNUB_PUBLISH_KEY,
                    subscribe_key=PUBNUB_SUBSCRIBE_KEY,
                    secret_key=PUBNUB_SECRET_KEY,
                    cipher_key='',
                    ssl_on=False
                    )
    pubnub.publish(CHANNEL, "Hello world")


'''    
data = json.dumps({"vol":10,"price":r.randint(0,30)})

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
'''