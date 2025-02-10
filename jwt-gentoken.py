import jwt
import datetime
import os

# Get current timestamp
timestamp = datetime.datetime.now().timestamp() 
# Convert timestamp to datetime object
dt_object = datetime.datetime.fromtimestamp(timestamp)
# Add 25 hours
new_dt_object = dt_object + datetime.timedelta(days=365)
# Convert back to timestamp
new_timestamp = new_dt_object.timestamp()

username = os.environ['USERNAME']
secret = os.environ['JWT_SECRET']

payload = {
  "username": username,
  "exp": new_timestamp
}

encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
print(encoded_jwt)
#print(jwt.decode(encoded_jwt, secret, algorithms=["HS256"]))
 