import socket
import subprocess
import sys

#Temporary
domain = "google.com"


def getAddrx(domain): #Finds out number of IPs
    try:
        addr = socket.gethostbyname_ex(domain)
        ipx = repr(addr[2])
        ipx = ipx.strip("[")
        ipx = ipx.strip("]")
        ipx = ipx.replace("'","")

        counter = str(ipx).count(",") + 1

        if str(ipx).find(",") != -1:
            print("Addresses: " + str(ipx))
            print("Number of IPs: " + str(counter))
        else:
            print("Address: " + str(ipx))
            print("Number of IPs: " + str(counter))

        return ipx

    except:
        print("Cannot Resolve to domain: " + domain)
        return False

def getDomain(IP): #Will be utilziing nslookup to resolve ips to domain names
    try:
        proc = subprocess.run(["nslookup", IP], stdout=subprocess.PIPE)
        #print(proc.stdout)
        string = str(proc.stdout)
    
        if string.find('=') != -1:
            offset = string.find('=')
            string2 = string[offset+2:]
        

        if string2.find("\\n") != -1:
            offset2 = string2.find("\\n")
            string3 = string2[:offset2-1]
            print(string3)
        else:
            print("Error")
    except:
        print("Error with nslookup")
        return False

test = getAddrx(domain)
getDomain('172.217.14.206')
