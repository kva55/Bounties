import socket
import subprocess
import sys
from pprint import pprint

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

    except Exception as e:
        print("Cannot Resolve to domain: " + domain)
        print(e)
        return False


#Not required since dig is used. If required, uncomment and format results (GLHF)
##def getDomainNames_NSLOOKUP(IP): #Will be utilizing nslookup to resolve ips to domain names
##
##    tmpDomainList = []
##
##    #nslookup search
##    try:
##        proc = subprocess.run(["nslookup", IP], stdout=subprocess.PIPE)
##        #print(proc.stdout)
##        string = str(proc.stdout)
##        string_format = string.split('\n')
##        
##        #print("Recieved at least 1 domain")
##        pprint(string_format)
##        return string_format
##
##    except:
##        print("Error with nslookup")
##        return False



def getDomainNames_DIG(IP): #Will need to also utilize dig because nslookup sucks
    try:
        proc = subprocess.run(["dig","-x", IP, "+short"], stdout=subprocess.PIPE)
        string = str(proc.stdout)

        #print("Recieved at least 1 domain")
        string_format = string.split('\\n')

        if string_format != None:
            return string_format
    #for entry in string_format:
        #nDomain_List.append(entry)
        #string_format = string_format.replace('\\','')
        #pprint(string_format)
        #return entry
        
    except:
        print("Error with dig")

def getNameServers_DIG(domain): #Experimental, searches for all name servers which may or may not be in scope
                                #This function is strictly domains to ns, not IPs
    try:
        #Sanitize input
        if str(domain).find('*') != -1:
            cut = str(domain).find('*')
            domain = domain[cut+2:] #Domain without wildcard

        proc = subprocess.run(["dig","-t", "ns", domain, "+short"], stdout=subprocess.PIPE)
        string = str(proc.stdout)

        #print("Recieved at least 1 domain")
        string_format = string.split('\\n')
        string_format = string[:-1]
        #print(domain)
        print(string_format)

        if string_format != None:
            return string_format
        
    except:
        print("Error with dig ns")


def DomainGrabber(IPList): #Function will split all the IPs from a string
                    #And turn it into a list
    if IPList != False:
        try:
            counter = str(IPList).count(",") + 1
            IPList_Sorted = IPList.replace(',','')
            IPList_Sorted = IPList_Sorted.split(' ')
            nDomain_List = []
      
            #Call getDomain() Function to do domain name resolution
            print("\nNew Domains listed below: ")
            
            for IP in IPList_Sorted:
                #nDomain  = getDomainNames_NSLOOKUP(IP) #New Domain from nslookup
                nDomain = getDomainNames_DIG(IP)        #New Domain from dig
            
                for entry in nDomain:
                    #print(entry)
                    #entry = entry.replace('[','')
                    #entry = entry.replace(']','')
                    #entry = entry.replace("'",'')
                
                    nDomain_List.append(entry)

        
            #Return list of new domains
            return nDomain_List
        except Exception:
            print("Error with domain resolution...")




