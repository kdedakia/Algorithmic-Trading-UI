import socket
import sys
import json
import random as r
import time
import datetime
import re
import pdb
import os

HOST, PORT = "codebb.cloudapp.net", 17429

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

data = "AmateurSpec_TCK" + " " + "letsmakeitrain" + "\n" + "MY_CASH" + "\n"
sock.sendall(data)
sfile = sock.makefile()
rline = sfile.readline()


def run(*commands):
    data="\n" + "\n".join(commands) + "\n"

    sock.sendall(data)
    sfile = sock.makefile()
    rline = sfile.readline()
    
    return rline.strip()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def mine():
    iteration = 0;
    cash = {}
    ALL = {}

    while iteration < 30000:
        t1 = time.time()
        data = {}
        
        #FAKE DATA
        fake_asks = [{"vol":10,"price":r.randint(0,30)},{"vol":40,"price":r.randint(0,30)},{"vol":100,"price":r.randint(0,30)},{"vol":360,"price":r.randint(0,30)},{"vol":190,"price":r.randint(0,30)},{"vol":420,"price":r.randint(0,30)}]
        fake_bids = [{"vol":120,"price":r.randint(0,100)},{"vol":400,"price":r.randint(0,100)},{"vol":30,"price":r.randint(0,100)},{"vol":90,"price":r.randint(0,30)},{"vol":505,"price":r.randint(0,30)},{"vol":204,"price":r.randint(0,30)}]
        
        #CASH
        cash = run("MY_CASH").split(" ")[-1]
        print cash

        #MY SECURITIES
        my_sec_string = run("MY_SECURITIES")
        my_sec_string = my_sec_string.replace("MY_SECURITIES_OUT ","")
        my_sec_hash = {}
        reg = "[\w]+\s[\d]+\s\d+\.\d+"
        
        while True:
            m = re.search(reg,my_sec_string)
            if m:
                # pdb.set_trace()
                sec_info = m.group().split(' ')
                my_sec_string = my_sec_string.replace(m.group(),"")
                my_sec_hash[sec_info[0].lower()] = {"shares":sec_info[1],"div":sec_info[2]}
            else:
                break

        #MY ORDERS
        myorders = run("MY_ORDERS")
        # print myorders

        bid_reg = "BID.[\w]+.[0-9]+\.[0-9]+.[0-9]+"
        ask_reg = "ASK.[\w]+.[0-9]+\.[0-9]+.[0-9]+" 
        bids = []
        asks = []
        bids_hash = {}
        asks_hash = {}
        
        #Find Bids
        while True:
                m = re.search(bid_reg,myorders)
                if m:
                    bids.append(m.group())
                    myorders = myorders.replace(m.group(),"")
                else:
                    break
        #Find Asks
        while True:
                m = re.search(ask_reg,myorders)
                if m:
                    asks.append(m.group())
                    myorders = myorders.replace(m.group(),"")
                else:
                    break

        for b in bids:
            bids_hash[b.split(' ')[1]] = {"price":b.split(' ')[2],"shares":b.split(' ')[3]}
        for b in asks:
            asks_hash[b.split(' ')[1]] = {"price":b.split(' ')[2],"shares":b.split(' ')[3]}


        #ALL SECURITIES
        all_sec_str = run("SECURITIES")
        # print all_sec_str
        all_sec_str = all_sec_str.replace("SECURITIES_OUT","")
        all_sec_reg = "\w+\s\d+\.\d+\s\d+\.\d+E?-?\d+\s\d+\.\d+"
        all_sec_hash = {}

        while True:
            m = re.search(all_sec_reg,all_sec_str)
            if m:
                sec_info = m.group().split(' ')
                all_sec_str = all_sec_str.replace(m.group(),"")
                all_sec_hash[sec_info[0].lower()] = {"net_worth":sec_info[1],"div":sec_info[2],"volatility":sec_info[3]}
            else:
                break
        
        data = {"aapl": {"asks":fake_asks,"bids":fake_bids},"cash":cash,"my_securities":my_sec_hash,'my_bids':bids_hash,'my_asks':asks_hash,'all_sec':all_sec_hash}
        
        ALL[iteration] = data
        data = json.dumps(data)
        
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        # with open(os.getcwd() + '/json2/data-' + str(iteration) + '.json', 'w') as outfile:
        #     json.dump(data, outfile)
        
        iteration += 1
        diff = (time.time() - t1)*1000.0
        # print diff
        time.sleep(1)

    with open('ALL2.json', 'w') as outfile:
            json.dump(ALL, outfile)




# test()
mine()
# t2()
# print run("MY_SECURITIES")