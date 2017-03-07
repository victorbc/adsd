import psutil
import sys

if(len(sys.argv) == 1):
	print "Passe o nome do processo como argumento"
else:
	pids = psutil.pids()

	PROCNAME = str(sys.argv[1])
	procdata = [0,0]

	for proc in psutil.process_iter():
	    if proc.name() == PROCNAME:
	    	procdata[0] += proc.memory_percent();
	    	procdata[1] += proc.cpu_percent(interval=1.0);



	print("\nNome do processo: %s\n\nUso de memoria: \n%s\n\nUso de CPU: \n%s" % 
	        	(PROCNAME, procdata[0], procdata[1]))



