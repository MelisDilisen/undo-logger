import time

filePath = 'transactions.txt'

#functions and error handling
def t_lines(tline):
    if tline[1] != 'T':
        print("INPUT ERROR: transactions should start either with C or T")
        exit()
    return tline[1:3]

#covering checkpointing and crash
def other_operations(tline):
    if tline[1] != 'C':
        print("INPUT ERROR: transactions should start either with C or T")
        exit()
    print("wait for CKPT...")
    time.sleep(3)
    r = tline[tline.find("{")+1:tline.find("}")]
    r = "".join(r.split())
    return r.split(',')

def DBelement(tline):
    if tline.count(',')<2:
        return None

    tline = tline[tline.find(',') + 1:]
    tline = tline[:tline.find(',')]
    tline = "".join(tline.split())
    return tline

def initial_value(tline):
    if len(tline)==0:
        return None
    tline = tline[tline.find(DBelement(tline)) + 2:]
    v=tline.find(',')

    if v==-1:
        tline = tline[:tline.find('>')]
    else:
        tline = tline[:tline.find(',')]
    tline = "".join(tline.split())
    return tline

def value_afterop(tline):
    if len(tline)==0:
        return None
    tline = tline[tline.rfind(',')+1:tline.rfind('>')]
    tline = "".join(tline.split())
    return tline

def scan(lines, search_item, top=0):
    #start scanning from the end index
    bottom = len(lines) - 1
    while lines[bottom].find(search_item) == -1:
        bottom -= 1
        if bottom - top == -1:
            return None
    return bottom

f = open(filePath,'r')
lines = f.readlines()

for i in range(len(lines)):
    lines[i]=lines[i].upper()

#lines making to checkpoint
CKPTlog = scan(lines, "CKPT")

log_mem = list(other_operations(lines[CKPTlog]))
print("\nTHE TRANSACTIONS CAUGHT IN THE CHECKPOINTING = ", end= " ")
for i in range(len(log_mem)):
    print(log_mem[i], end="    ")



#TRANSACTION HANDLING
for i in range(CKPTlog+1,len(lines)):
    if lines[i].find("START")!=-1:
        log_mem.append(t_lines(lines[i]))
    elif lines[i].find("COMMIT")!=-1:
        log_mem.remove(t_lines(lines[i]))
    elif lines[i].find("ABORT")!=-1:
        log_mem.remove(t_lines(lines[i]))
    else:pass

print("\n-------------")
print("\nUNDO LOGGING")
print("-------------")
i=len(lines)-1
log=[]
duplicate = log_mem.copy()
while 1:
    for t in duplicate:
        if t not in log_mem:
            continue
        if lines[i].find(t) != -1:
            if lines[i].count(',')>1:
                print("DB elemenent " + DBelement(lines[i]) + " is restored to its initial value " + initial_value(lines[i]))
                log.append("<" + t_lines(lines[i]) + ", " + DBelement(lines[i]) + ", " + initial_value(lines[i]) + ">")

            elif lines[i].find("START") != -1:
                log_mem.remove(t_lines(lines[i]))
                print((t_lines(lines[i])) + " is being removed from the Log")
                log.append("<" + t_lines(lines[i]) + " ABORT>")

            else:
                pass
    if len(log_mem) == 0:
        #no items left
        print("\nUndo Log:")

        for j in log:
            print(j)
        break

    i -= 1
    if i==0:
        break

f.close()


# Find committed transactions
committed_transaction = []
with open(filePath) as f:
    for line in f:
        if "commit" in line:
            mylist = line.split(" ")
            # print(mylist)
            transactionName = mylist[0][1:]
            committed_transaction.append(transactionName)
            # print(committedTransaction)
f.close()

#DISK LOG (NON-VOLATILE)
# Open a disk log file to write all
fw = open("diskLogFile.txt", "a")

# Log respective lines of committed transactions
for cmt in committed_transaction:
    with open(filePath) as f:
        for line in f:
            line = line.rstrip('\r\n')

            if str(cmt) in line and "ckpt" not in line:

                mylist = line.split(",")
                if len(mylist) >= 3:
                    transactionLine= ""
                    for  i in range (0,3):
                        transactionLine += mylist[i] + ","

                    listTransLine = list(transactionLine)
                    lastInd = len(listTransLine) - 1
                    listTransLine[lastInd] = '>'
                    transactionLine = ''.join(listTransLine)

                    fw.write(transactionLine + "\n")
                else:
                    upperLine = line.upper()
                    strList = upperLine.split(" ")
                    startEndLine = ""
                    startEndLine = "<" + strList[1][0:-1] + " " + strList[0][1:] + ">"

                    fw.write(startEndLine + "\n")

fw.close()
f.close()