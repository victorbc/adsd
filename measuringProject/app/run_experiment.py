import sys
import time
import requests
import csv

BASE_URL = "http://127.0.0.1:5000/"
POST_URL = BASE_URL + "benchmark/write"
GET_URL = BASE_URL + "benchmark/read/"
GET_QUERY = "test"
CSV_HEADER = ['type', 'cpu_usage', 'response_time', 'bd_time', 'memory_usage' , 'total_server_time']
SAMPLES = []


def run_experiment(test_type, requests_per_min, duration):
    start_time = time.time()
    for i in range(duration):
        if test_type == 'POST':
            run_post_experiment(requests_per_min)
        elif test_type == 'GET':
            run_get_experiment(requests_per_min)
        else:
            print (test_type +" Is an invalid experiment type")
            break
        time.sleep(60)

    save_to_csv(test_type, duration, requests_per_min)

def run_post_experiment(requests_per_min):
    global SAMPLES
    for i in range(requests_per_min):
        start_time = time.time()
        r = requests.post(POST_URL,json={"title":"test", "text":"lorem ipsum"})
        response_time = time.time() - start_time
        json = r.json()
        SAMPLES.append(['POST', json['cpu_usage'], response_time, json['db_time'], json['memory_usage'] , json['total_time']])

def run_get_experiment(requests_per_min):
    global SAMPLES
    for i in range(requests_per_min):
        start_time = time.time()
    	r = requests.get(GET_URL + GET_QUERY)
        response_time = time.time() - start_time
    	json =  r.json()
    	SAMPLES.append(['GET', json['cpu_usage'], response_time, json['db_time'], json['memory_usage'] , json['total_time']])

def save_to_csv(test_type, duration, requests_per_min):
    file_name = "{timestamp}-{test_type}_{requests}_requests_per_minute_for_{duration}.csv".format(timestamp=time.time(), test_type=test_type, requests=requests_per_min, duration=duration)
    with open(file_name, 'wb') as csvfile:
    	writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
    	writer.writerow(header)
    	for row in zip(registro_tempos):
    		#print(row)
    		writer.writerow(row[0])


if __name__ == "__main__":
    if(len(sys.argv) < 4):
    	print "Run with: <test_type> <requests per min> <duration in min>"
    else:
        test_type = str(sys.argv[1]).upper()
        requests_per_min = int(sys.argv[2])
        duration = int(sys.argv[3])

        # Run Experiments with provided configuration
        run_experiment(test_type, requests_per_min, duration)
