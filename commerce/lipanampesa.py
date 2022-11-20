# import base64
# from datetime import datetime
# import requests
# from requests.auth import HTTPBasicAuth
# import json
# import pdb


# def getAccessToken():
#     time = datetime.now()
#     now = time.strftime("%Y%m%d%H%M%S")
#     print(now)
#     passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
#     encode_data = "{0}{1}{2}".format(
#         str(174379), passkey, now)

#     encoded = base64.b64encode(encode_data.encode())
#     # print(encoded)
#     decoded_password = encoded.decode('utf-8')
#     print(decoded_password)
#     consumer_key = "O37TejJH9jA7uKTKrwRCtLRSYf9siMAJ"
#     consumer_secret = "A0INR9Vtevz1MgiJ"
#     api_URL ="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#     r = requests.request("GET",api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     print(r.json())
#     json_response = r.json()

#     my_access_token = json_response['access_token']

#     return my_access_token