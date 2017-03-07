import requests
import time
import schedule
import csv
import psutil
import json

num_ensaios = 50
num_ensaios2 = 50
contador_execucoes = 0
contador_execucoes2 = 0
registro_tempos = []
num_req = 0
def job():
    global contador_execucoes
    pids = psutil.pids()
    p = psutil.Process(pids[-1])
    contador_execucoes += 1;
    
    start_time = time.time()
    r = requests.get('https://api.github.com/events')
    registro_tempos.append(('', contador_execucoes, p.name(), time.time() - start_time, p.memory_percent(), p.cpu_percent(interval=1.0), ''))
    
##    print r.status_code
##    print r.headers['content-type']    
##    print("\nNome do processo: %s\n\nUso de memoria: \n%s\n\nUso de CPU: \n%s" % (p.name(), p.memory_percent(), p.cpu_percent(interval=1.0)))    


def job():
	global contador_execucoes
	pids = psutil.pids()
	p = psutil.Process(pids[-1])
	contador_execucoes += 1;
	
	start_time = time.time()
	r = requests.get('https://api.github.com/events')
	registro_tempos.append(('', contador_execucoes, p.name(), time.time() - start_time, p.memory_percent(), p.cpu_percent(interval=1.0), ''))
	
def job2():
	global contador_execucoes
	contador_execucoes += 1;
	start_time = time.time()
	r = requests.post('http://10.0.0.7:5000/benchmark/write',json={"title":"test", "text":"lorem ipsum"})
	json =  r.json();
	registro_tempos.append(['POST',contador_execucoes, json['cpu_usage'], time.time() - start_time, json['db_time'], json['memory_usage'] , json['total_time']])



def job3():
	global contador_execucoes2
	contador_execucoes2 += 1;
	start_time = time.time()
	r = requests.get('http://10.0.0.7:5000/benchmark/read/test')
	json =  r.json();
	registro_tempos.append(['GET',contador_execucoes2, json['cpu_usage'], time.time() - start_time, json['db_time'], json['memory_usage'] , json['total_time']])

def post():
	for x in xrange(1,num_req):
		job2()

def get():
	for x in xrange(1,num_req):
		job3()	
	

#schedule.every(2).seconds.do(job2)


import sys

if(len(sys.argv) < 4):
	print "<type><req_num><script name>"
else:
	num_req = int(sys.argv[2])
	if(str(sys.argv[1]) == 'get'):
		schedule.every(1).seconds.do(get)
	elif(str(sys.argv[1]) == 'post'):
		schedule.every(1).seconds.do(post)


#main loop
while True:
	global num_req
	schedule.run_pending()
	#time.sleep(1)
	#print(contador_execucoes2)
	#print(num_req)

	if (contador_execucoes >= num_req-1):
		break
		#job2()
		#schedule.every(2).seconds.do(job3)

	#if (contador_execucoes >= num_ensaios):
	#	job3()

	if(contador_execucoes2 >= num_req-1):
		break

#salvar tempos em arquivo csv
with open(str(time.time())+'_'+str(sys.argv[2])+'_'+str(sys.argv[1])+'_'+str(sys.argv[3])+'.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
	writer.writerow(['type','#', 'cpu_usage', 'request_time', 'db_time', 'memory_usage' , 'total_time'])
	for row in zip(registro_tempos):
		#print(row)
		writer.writerow(row[0])




# exemplos de outros requests
# r = requests.post('http://httpbin.org/post', data = {'key':'value'})
# r = requests.put('http://httpbin.org/put', data = {'key':'value'})
# r = requests.delete('http://httpbin.org/delete')
# r = requests.head('http://httpbin.org/get')
# r = requests.options('http://httpbin.org/get')   

# exemplos de outros schedules
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
