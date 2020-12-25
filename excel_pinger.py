import subprocess,os,threading,time
from queue import Queue
import pandas as pd
import ipaddress, re

def check(ip):
    with open(os.devnull, "wb") as limbo:
                result=subprocess.Popen(["ping", "-c", "1", "-W", "2",ip[0]],stdout=limbo, stderr=limbo).wait()
#                result = subprocess.Popen(["ping", "-c", "1", "-W", "1", ip[0]]).wait()
                with lock:
                    if not result:
                        df['Other'][ip[2]] = 'Ping Successful'
#                        print (ip[1],ip[0], "active")
#                        df.iat["Action"][ip[2]].replace(None,"Active",inplace=True)
                    else:
                        df['Other'][ip[2]] = 'Ping Failed'
#                        print (ip[1],ip[0], "failed")
                        pass

def threader():
    while True:
        worker=q.get()
        check(worker)
        q.task_done()

def write_excel(df2):
    with pd.ExcelWriter('/Users/ts01mjl/Downloads/outfile_nfv_workbook.xlsx') as writer:
        df2.to_excel(writer)
        return

if __name__ == "__main__":
    _start = time.time()
    IP_List = []

    filename = r'/Users/ts01mjl/Downloads/nfv_workbook.xlsx'
#    print(type(filename), filename)
    df = pd.read_excel(filename)
    for x in range(len(df['IP Address'])):
#        print(type(df['IP Address'][x]), end=' ')
        try:
            address = ipaddress.ip_address(df["IP Address"][x])
        except ValueError as err:
            df['Other'][x] = ''
#            pass
        else:
            IP_List.append((str(address), df['DNSNAME'][x], x))
#            print df.iloc()


    lock = threading.Lock()

    q = Queue()

    for x in range(16):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()


    for worker in IP_List:
        q.put(worker)

    q.join()


    write_excel(df)

    print("Process completed in: ", time.time() - _start)