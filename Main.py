from Domain_Time_Saver import getAddrx, getDomainNames, DomainGrabber
from scoper import HostCutter, JSONParser


#Addresses = getAddrx(domain)
#New_Domains = DomainGrabber(Addresses)

Saved_Scope = JSONParser() #First element Exclude list
#print(Saved_Scope[0])     #Second element Include List
#print(Saved_Scope[1])

#This step Sanitizes the domains found in the JSON obj

def SanitizeScope(Scope):
    Temp_Include  = str(Scope)
    Temp_Include = Temp_Include.replace("'",'')
    Temp_Include = Temp_Include.replace(']','')
    Temp_Include = Temp_Include.replace('[','')
    Temp_Include = Temp_Include.replace(' ','')
    Sanitized_Scope = Temp_Include.split(',')
    return Sanitized_Scope

Exclude_Scope = SanitizeScope(Saved_Scope[0])
Include_Scope = SanitizeScope(Saved_Scope[1])


print("\nIncluded Scope Domains: ")
for domain in Include_Scope:
    print(domain)


print("\nExcluded Scope Domains: ")
for domain in Exclude_Scope:
    print(domain)

#This step will take all included scope and find domain names
print("\nDomains in Included Scope: ")
for domain in Include_Scope:
    if str(domain).find('*') != -1: #Searches for wildcards
        cut = str(domain).find('*')
        wDomain = domain[cut+2:] #Domain without wildcard
        Addresses = getAddrx(wDomain)
        New_Domains = DomainGrabber(Addresses)

    else: #These do not have wild cards, do not do subdomain enumeration.
        Addresses = getAddrx(domain)
        New_Domains = DomainGrabber(Addresses)
        




    
