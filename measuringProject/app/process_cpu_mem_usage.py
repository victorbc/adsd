import psutil
pids = psutil.pids()
p = psutil.Process(pids[-1])
print("\nNome do processo: %s\n\nUso de memoria: \n%s\n\nUso de CPU: \n%s" % (p.name(), p.memory_percent(), p.cpu_percent(interval=1.0)))

