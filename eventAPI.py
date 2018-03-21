import requests
import time
from random import randint

EVENT_API_URL = 'https://logx.optimizely.com/v1/events'

def send_events(payload={}):
    response           = requests.post(EVENT_API_URL, json=payload)
    successful_request = response.status_code >= 200 and response.status_code < 300
    if not successful_request:
        raise Exception('Event request failed. Request code: {:d}'.format(response.status_code))

send_events({
  "account_id": "XXXXXXXXX", # Static value
  "visitors": [ # It's possible to send multiple visitor objects in a single payload. Up to 10MB.
    {
      "snapshots": [
        {
          "decisions": [
            {
              "campaign_id": "XXXXXXXXX", # These values are populated by the client-side APIs.
              "experiment_id": "XXXXXXXXX",
              "variation_id": "XXXXXXXXX"
            }
          ],
          "events": [
            {
              "timestamp": int(time.time() * 1000), # Required: Epoch timestamp in milliseconds.
              "uuid": randint(1, 9999999999999999), # Use any UUID generation library. Used to de-dupe events on Optimizely's backend should multiple be sent.
              "entity_id": "XXXXXXXXX", # Retrieved from Optimizely's interface AFTER an event has been created.
              "value": 5555, # This is an incremental value that could be used to tell Optimizely how long the call lasted. We could answer the question, "Which variation produced the longest sales calls?" It can be negative to decrement.
              "type": "custom" # Don't change this.
            }
          ]
        }
      ],
      "visitor_id": "oeuXXXXXXXXX.XXXXXXXXX", # This ID is the value of the `optimizelyEndUserId` cookie.
      "attributes": [], # This can be an empty array if you don't care about segmentation for server-side events. Not relevant for the integration.
      "session_id": "AUTO" # Don't change this.
    }
  ],
  "client_name": "optly/CTMTracker", # Don't change this. Used for identifying the integration in raw data.
})
