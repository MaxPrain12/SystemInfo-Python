import os
import psutil
import time
import datetime



#after execute this script we can save all output information on external file 

# example now we have a crontab task like this 
# 0 20 * * * root python3 rutaScript >  rutaDestino/dato_$(date -d"-0 days" +\%Y\%m\%d).log
# ---------------------------------------------------------------------------------------------


# Looks CPU info and CPU times
if __name__ == '__main__':
    for i in range(5):
        perc_cpu = psutil.cpu_percent(interval=0.5)
        time_cpu = psutil.cpu_times(percpu=False)


        systemTime = str(datetime.timedelta(seconds=time_cpu.system))
        IdleTime = str(datetime.timedelta(seconds=time_cpu.idle))

        print(f'''CPU estado:
        Uso de CPU: {perc_cpu}%
        Tiempos: 
            system: {systemTime.split(".")[0]}
            idle: {IdleTime.split(".")[0]}
        ''')
        print('''-------------------------------------------------------------''')
        time.sleep(4)
# Look RAM memori
for i in range(3):
    # save all infomation about used memori
    mem_virt = float(psutil.virtual_memory().used / (1024 ** 3))
    # save all info about available memori
    avail_mem = float(psutil.virtual_memory().available *
                      100 / psutil.virtual_memory().total)
    mem_total = float(psutil.virtual_memory().total / (1024 ** 3))
    # print in cosole all text saved in varibles 
    print(f'''Informacion de Memoria RAM:
       Memoria Total: {"{:.2f}".format(mem_total)}GB
       Memoria En Uso: {"{:.2f}".format(mem_virt)}GB
       Memoria Disponible: {"{:.2f}".format(avail_mem)}%
       ''')
    print('''-------------------------------------------------------------''')
    time.sleep(2)
# Look DisK
rName = []
rSize = []
rRuta = []
Dname = os.popen("lsblk -a -p -o NAME").readlines()
Dsize = os.popen("lsblk -a -p -o SIZE").readlines()
Druta = os.popen("lsblk -a -p -o MOUNTPOINT").readlines()
for line in Dname:
    line = line.strip()
    line = line.lstrip("└─├─")
    line = line.rstrip("\n")
    rName.append(line)
for line in Dsize:
    line = line.strip()
    line = line.rstrip("\n")
    rSize.append(line)
for line in Druta:
    line = line.rstrip("\n")
    rRuta.append(line)
for i in range(len(rName)):
    if i != 0 :
        
        ruta = rRuta[i]
        if ruta != '' and ruta != "[SWAP]":
            infoS = "{:.2f}".format(psutil.disk_usage(ruta).used / (1000**3))
            print(f'''Disco/Particion {rName[i]} : {infoS}/{rSize[i]} Total''')
        else :
            if ruta != "[SWAP]":
                print(f'''Disco/Particion {rName[i]} : {rSize[i]} Total''')
            else: 
                 print(f'''SWAP {rName[i]} : {rSize[i]} Total''')
print('''-------------------------------------------------------------''')
time.sleep(2)
# Look all proces 
def checkIfProcessRunning(processName):
    
    #Check if there is any running process that contains the given name processName.
    
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                if proc.is_running:
                    estado = " Activo "
                else:
                    estado = " Inactivo "

                print(f'''Process {proc.name()}:
                PID: {proc.ppid()}
                Estado:{estado}
                Conexiones:
                    
                 ''')
                for pccon in proc.connections():
                    print(f'''  {pccon}''')

                return True
                # Catching all excepts 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
if checkIfProcessRunning("NameProcess"):
    print('')
else:
    print('NameProcess no esta Disponible')
print('''-------------------------------------------------------------''')

