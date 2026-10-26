#reports.py
#will use sql to retrieve record data and return it as a report
#from database import get_all_checks
from database import (
    get_total_checks, get_status_count, get_avg_response_times, get_latest_check, get_services
)



#return number of check records
checks = get_total_checks()
online_checks = get_status_count("online")
error_checks = get_status_count("error")
unreachable_checks = get_status_count("unreachable")
average_times = get_avg_response_times()

#availability calculator -> % of recorded checks that come back as 'online'
#availability = round((online_checks / checks * 100), 1) if checks > 0 else 0
if checks > 0:
    availability = round((online_checks / checks * 100), 1)
else:
    availability = 0


print("\nSERVICE MONITOR REPORT\n")
print("----------------------\n")
print("\ntotal checks: ", checks, "\n")
print("online checks: ", online_checks, "\n")
print("error checks: ", error_checks, "\n")
print("unreachable checks: ", unreachable_checks, "\n")
print("availability: ", availability, "%\n")

#avg response times
print("AVERAGE RESPONSE TIMES\n")
print("----------------------\n")

for row in average_times:
    URL = row[0]
    avg_time = round(row[1], 3)
    print( URL, " -> " , avg_time , "\n")


#current service health
print("\nCURRENT SERVICE HEALTH")
print("----------------------")

services = get_services()
print(services)
for row in services:
    print("\n")
    service_url = row[0]
    latest = get_latest_check(service_url)
    url = latest[1]
    status = latest[2]
    #response_time = round(latest[3], 3)
    if latest[4] is not None:
        response_time = (round(latest[4], 3), " seconds")
    else:
        response_time = "n/a"
    print(url, " -> ", status, " -> ", response_time, "\n")
    #test
    #print("DEBUG latest:", latest)

#latest checks
#latest = get_latest_check("https://www.google.com")

#print(latest)



#notes
#round() -> int a = round(int c, b) -> int a is int c to b dp