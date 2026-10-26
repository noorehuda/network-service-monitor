Network+ Service Monitor

I built a small monitoring system that could automatically check multiple services, record the results and notice when the state of a service changes.

The basic idea became:
    1. monitor - the network/list of services
    2. store - data from monitoring like response time, http status code etc, stored in the database
    3. compare - previous and current data, values like availability based on historical data pulled from the database
    4.  report - summarise data comparisions and changes to the user.

The monitor classifies services as online, error, or unreachable, and compares current results with previous checks to detect incidents and recoveries. Stored monitoring data can then be used to generate a health report containing availability, status counts, average response times and the latest status of each service.

I built this project to develop my practical understanding of Python, HTTP/networking, SQL databases, error handling and automated testing.

Features:  
- Monitors multiple web service URLs  using HTTP GET requests
- Measures response time for successful HTTP connections
- Uses a request time out to prevent slow services from blocking the monitor
- Classifies results as online, error or unreachable
- Stores monitoring history in a SQLite database
- Generates service-health statistics from historical data
- Calculates average response times for individual services
- Compares previous and current states to detect incidents and recoveries and changes
- Handles failed network requests without crashing the monitor
- Uses automated unit tests and mocked HTTP responses to test behaviour without relying on live websites

How it works +project structure:

For each configured service, the monitor sends an HTTP GET request with a timeout.

1. The HTTP response is classified as:
   - `online` — HTTP status code is in the 200–299 range
   - `error` — the service responds, but with a non-2xx HTTP status code
   - `unreachable` — the request fails, for example because of a connection error or timeout

2. The result, HTTP status code and response time are recorded in SQLite.

3. Before saving the new result, the monitor retreives the service's previous check and compares its status with the current status.

4. A change can then be identified as an incident, recovery or other status change.

5. Historical results can be analysed by the reporting script to show overall availability, status counts, average response times and the latest health of each service.

Project Structure:
network-service-monitor/
│
├── monitor.py          # Performs service checks and detects status changes
├── database.py         # Creates and interacts with the SQLite database
├── reports.py          # Generates health statistics from stored results
├── test_monitor.py     # Automated tests for monitoring and status detection
├── requirements.txt    # Python dependency list
├── .gitignore          # Files excluded from version control
└── README.md           # Project documentation

Technologies:
- Python — core application logic
- Requests — HTTP requests and connection error handling
- SQLite / SQL — persistent storage and querying of monitoring history
- unittest — automated testing
- unittest.mock — mocked HTTP responses and request failures
- Git / GitHub — version control and project hosting