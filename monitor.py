import requests

services = [
    "https://www.google.com",
    "https://youtube.com",
    "https://invalid-tester.com",
    "https://www.notion.com"
]
#service_url = "https://www.google.com"
#service_url = "https://invalid-tester.com"# << error checking
print("network+service monitor")

for service_url in services:
    print("checking: ", service_url)

    #error checking w/ try except
    try:
        response = requests.get(service_url, timeout=5) #http request to google
        print("HTTP status code: ", response.status_code) #http response code
        #fix 
        #response_time = response.elapsed.total_seconds()
        response_time = round(response.elapsed.total_seconds(), 3) #round 3dp
        
        #decide based on status code
        if (200 <= response.status_code < 300):
            print("service status: online")
        else:
            print("service status: error")

        #time to respond // returns an ugly number tho.....
        #print("Response Time:", response.elapsed.total_seconds(), "seconds") 
        print("Response Time:", response_time, "seconds")
        

    except requests.exceptions.RequestException:
        print("service status: unreachable")




'''
print("HTTP status code: ", response.status_code) #http response code

#fix 
#response_time = response.elapsed.total_seconds()
response_time = round(response.elapsed.total_seconds(), 3) #round 3dp

#decide based on status code
if response.status_code == 200:
    print("service status: online")
else:
    print("service status: error")

#time to respond // returns an ugly number tho.....
#print("Response Time:", response.elapsed.total_seconds(), "seconds") 
print("Response Time:", response_time, "seconds")
'''