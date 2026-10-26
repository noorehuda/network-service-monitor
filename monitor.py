#monitor.py
#checking service status
import requests
from database import create_database, save_check, get_latest_check  #import this function from db.py



def check_service_status(service_url):
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
            status = "online" #makes status a variable that can be returned
            #print("service status: online")
        else:
            status = "error"
           # print("service status: error")
        
        #time to respond // returns an ugly number tho.....
        #print("response time:", response.elapsed.total_seconds(), "seconds") 

        print("service status:", status)
        print("response time:", response_time, "seconds")
        print("\n") #new line for readability
        #return response_time #temp will output time 2x but returning info is needed 4future
        return {
            "url" : service_url,
            "status" : status,
            "http_status_code" : response.status_code,
            "response_time" : response_time
        }
    
    except requests.exceptions.RequestException:
        print("service status: unreachable") #return value for except part
        print("\n") #new line for readability
        return{
            "url" : service_url,
            "status" : "unreachable",
            "http_status_code" : None,
            "response_time" : None
        }


#service_url = "https://www.google.com"
#service_url = "https://invalid-tester.com"# << error checking

def detect_status_change(previous_status, current_status):
    if previous_status == "online" and current_status != "online":
        #print(f"incident detected:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
        return "incident"
    elif previous_status != "online" and current_status == "online":
        #print(f"service recovery:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
        return "recovery"
    elif previous_status != current_status:
        #print(f"status change:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
        return "change"
    else:
        return None
    



services = [
    "https://www.google.com",
    "https://youtube.com",
    "https://invalid-tester.com",
    "https://www.notion.com"
]

def main():
    print("network+service monitor \n")

    create_database()

    for service_url in services:
        result = check_service_status(service_url)
        previous = get_latest_check(service_url)

        #compare prev n curr 
        # //put in function detect_status_change() 
        #if previous is not None and previous[2] != result["status"]:
        if previous is not None:
            previous_status = previous[2]
            current_status = result["status"]

            status_change = detect_status_change(previous_status, current_status)

            if status_change == "incident":
                print(f"incident detected:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
            elif status_change == "recovery":
                print(f"service recovery:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
            elif status_change == "change":
                print(f"status change:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")


        save_check(result) #monitoring results -> database.py -> save_check() -> monitor.db



if __name__ == "__main__":
    main()




'''
COMMENTED OUT CODE, DONT DELETE YET!!!


print("network+service monitor \n")

create_database()

for service_url in services:
    result = check_service_status(service_url)
    previous = get_latest_check(service_url)

    #compare prev n curr 
    # //put in function detect_status_change() 
    #if previous is not None and previous[2] != result["status"]:
    if previous is not None:
        previous_status = previous[2]
        current_status = result["status"]

        status_change = detect_status_change(previous_status, current_status)

        if status_change == "incident":
            print(f"incident detected:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
        elif status_change == "recovery":
            print(f"service recovery:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")
        elif status_change == "change":
            print(f"status change:\nservice: {service_url} \nprevious:  {previous_status} \ncurrent: {current_status}\n")


    save_check(result) #monitoring results -> database.py -> save_check() -> monitor.db






'''





'''
        #debugging
        print(detect_status_change("online", "error", "https://www.google.com"))
        print(detect_status_change("error", "online", "https://www.google.com"))
        print(detect_status_change("error", "unreachable", "https://www.google.com"))


'''


        #print(f"STATUS CHANGE: {service_url} \nprevious:  {previous[2]} \ncurrent: {result['status']}\n")


#save_check(result) #monitoring results -> database.py -> save_check() -> monitor.db
    #print("returned value: ", result) #temp print ret value for testing
#status_change = detect_status_change(previous_status, current_status, service_url)
'''
#debugging
print(detect_status_change("online", "error", "https://www.google.com"))
print(detect_status_change("error", "online", "https://www.google.com"))
print(detect_status_change("error", "unreachable", "https://www.google.com"))
print(detect_status_change("unreachable", "error", "https://www.google.com"))
print(detect_status_change("unreachable", "online", "https://www.google.com"))
print(detect_status_change("online", "unreachable", "https://www.google.com"))
print(detect_status_change("online", "online", "https://www.google.com"))
'''















''' OLD CODE DONT DELETE JIC!!! '''
'''
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