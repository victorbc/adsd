import requests
import time
import schedule
import csv
import psutil

num_ensaios = 3
contador_execucoes = 0
registro_tempos = []

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
    

schedule.every(2).seconds.do(job)

#main loop
while True:
    schedule.run_pending()
    time.sleep(1)

    if (contador_execucoes == num_ensaios):
        break


#salvar tempos em arquivo csv
with open('the_file.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in zip(registro_tempos):
        writer.writerow(row)



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