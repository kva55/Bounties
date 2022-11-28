import socket
import subprocess
import sys

def getAddrx(domain): #Finds out number of IPs
    print("Domain: " + domain)
    print("Getting hostname by domain...")
    try:
        addr = socket.gethostbyname_ex(domain)
        ipx = repr(addr[2])
        ipx = ipx.strip("[")
        ipx = ipx.strip("]")
        ipx = ipx.replace("'","")

        #Only for printing
        ipx_temp = ipx
        ipx_temp = ipx_temp.replace(',','')
        ipx_temp = ipx_temp.split(' ')
        
        counter = str(ipx).count(",") + 1
        
        if str(ipx).find(",") != -1:
            print("Addresses: ")
            for step in range(len(ipx_temp)):
                print(ipx_temp[step])
            print("Number of IPs: " + str(counter))
        else:
            print("Address: " + str(ipx))
            print("Number of IPs: " + str(counter))

        return ipx

    except:
        print("Cannot Resolve to domain: " + domain)
        return False

def getDomainNames(IP): #Will be utilizing nslookup to resolve ips to domain names
                        #Will need to also utilize dig because nslookup sucks

    #nslookup search
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
                return string3
        else:
            print("Error with nslookup")
    except:
        print("Error with nslookup")
        return False

    #Dig search may be implemented as a second check
    """

    Add dig check here


    """

def DomainGrabber(IPList): #Function will split all the IPs from a string
                    #And turn it into a list
    if IPList != False:
        try:
            counter = str(IPList).count(",") + 1
            IPList_Sorted = IPList.replace(',','')
            IPList_Sorted = IPList_Sorted.split(' ')
      
            #Call getDomain() Function to do domain name resolution
            print("\nNew Domains listed below: ")
            nDomain_List = []
            for IP in IPList_Sorted:
                nDomain = getDomainNames(IP) #New Domain
                nDomain_List.append(nDomain)
            print()
        
        #Return list of new domains
            return nDomain_List
        except Exception:
            print("Error with domain resolution...")




