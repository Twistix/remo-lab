import requests

# ========================================== HTTP POST AND GET REQUESTS =================================================
def httpPost(postUrl, payload) :
    r = requests.post(postUrl, data=payload) # sending a POST request to the url with the data
    print("Data sent successfully")

def httpGet(getUrl) :
    r = requests.get(getUrl) # sending a GET request to the url
    print("Data recieved successfully")
    return r.text   # returning the response from the server in string format
