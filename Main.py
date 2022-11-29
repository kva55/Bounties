from Domain_Time_Saver import getAddrx, \
     DomainGrabber, getDomainNames_DIG
from scoper import HostCutter, JSONParser
from pprint import pprint


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



def Main():

    Exclude_Scope = SanitizeScope(Saved_Scope[0])
    Include_Scope = SanitizeScope(Saved_Scope[1])
    New_Domains_List = []
    
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
            New_Domains_List.append(New_Domains)

        else: #These do not have wild cards, do not do subdomain enumeration.
            Addresses = getAddrx(domain)
            New_Domains = DomainGrabber(Addresses)
            New_Domains_List.append(New_Domains)


    #Basic Formatting - Should be moved to another function later
    Domains_Formatted = []
    Domains = str(New_Domains_List).replace("'",'')
    Domains = Domains.replace("[", "")
    Domains = Domains.replace("]", "")
    Domains = Domains.strip("'")
    Domains = Domains.split(',')
    for entry in Domains:
        test = entry.strip("'")
        test = entry.strip('"')
        test = entry.strip('"b')
        test = test.replace('"','')
        test = test.replace('\n','')
        test = test.replace(' ','')
        
        if str(test) != 'None':
            if str(test).endswith('.'):
                test = test.rstrip('.')
    
            if str(test) != '':
                Domains_Formatted.append(test)

        
            
    Domains_Formatted_dups = list(dict.fromkeys(Domains_Formatted))

    return Domains_Formatted_dups

Domains = Main()
##Domains_Formatted = []

print("\n\nName Servers Located: ")

##Domains = str(Domains).replace("'",'')
##Domains = Domains.replace("[", "")
##Domains = Domains.replace("]", "")
##Domains = Domains.strip("'")
##Domains = Domains.split(',')
###pprint(Domains)
###pprint(Domains)
##for entry in Domains:
##    test = entry.strip("'")
##    test = entry.strip('"')
##    test = entry.strip('"b')
##    test = test.replace('"','')
##    test = test.replace('\n','')
##    test = test.replace(' ','')
##    if str(test).endswith('.'):
##        test = test.rstrip('.')
##    
##    if str(test) != '':
##        Domains_Formatted.append(test)
#print("Final result:\n\n" + str(Domains))

#Quickly see duplicates and remove them
##Domains_Formatted_dups = list(dict.fromkeys(Domains_Formatted))
pprint(Domains)

    
