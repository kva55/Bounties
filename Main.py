from Domain_Time_Saver import getAddrx, \
     DomainGrabber, getDomainNames_DIG, \
     getNameServers_DIG
from scoper import HostCutter, JSONParser
from pprint import pprint
from os import path
import argparse
import csv


parser = argparse.ArgumentParser(description="BOSS - Bounty Osint Sniffer Software.")
parser.add_argument("-j", "--json", metavar='', help="Attach hackerone json file")
parser.add_argument("-f", "--file", metavar='', help="Attach regular file")
parser.add_argument("-ns", "--ns",  metavar='', help="Search names servers (From domain) - Experimental", \
                    action=argparse.BooleanOptionalAction)
parser.add_argument("-o", "--output", metavar='', help="Outputs the results into a spreadsheet.")
parser.add_argument("-se", "--subdomain-enumeration", "--subdomain-enum", type=int, metavar='', help="Subdomain enumeration functionality")
args = parser.parse_args()


#Global Vars (For now)
NS  = False
OUT = False
NStorage = []
NameServers = []
Addresses = []

#This step Sanitizes the domains found in the JSON obj
def SanitizeScope(Scope):
    Temp_Include  = str(Scope)
    Temp_Include = Temp_Include.replace("'",'')
    Temp_Include = Temp_Include.replace(']','')
    Temp_Include = Temp_Include.replace('[','')
    Temp_Include = Temp_Include.replace(' ','')
    Sanitized_Scope = Temp_Include.split(',')
    return Sanitized_Scope

def RegScope(rfile_list):
    rfile_list = []
    if path.exists(rfile):
        print("Hackerone Scope Verifier.\nFile attached is: " + rfile)
        print(rfile)
        fopen = open(rfile)
        for line in fopen:
            if line != '\n' or line != '':
                line = line.strip("\n")
                rfile_list.append(line)
        fopen.close()
    return rfile_list

#This will get the domains (Enumerated ptr domains).
def RegFile(rfile_list):
    New_Domains_List = []
    #This step will take all included scope and find domain names
    print("\nDomains in Scope: ")
    pprint(rfile_list)
    print()
    for domain in rfile_list:
        if str(domain).find('*') != -1: #Searches for wildcards
            cut = str(domain).find('*')
            wDomain = domain[cut+2:] #Domain without wildcard
            #Addresses = getAddrx(str(wDomain))
            Addresses.append(getAddrx(wDomain))
            New_Domains = DomainGrabber(Addresses)
            New_Domains_List.append(New_Domains)

        else: #These do not have wild cards, do not do subdomain enumeration.
            #Addresses = getAddrx(str(domain))
            wDomain = domain
            Addresses.append(getAddrx(wDomain))
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
    print("\n\nDomains Located: ")
    pprint(Domains_Formatted_dups)
    
    return Domains_Formatted_dups
    

def JSONFIle(Saved_Scope):

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
            Addresses.append(getAddrx(wDomain))
            New_Domains = DomainGrabber(Addresses)
            New_Domains_List.append(New_Domains)

        else: #These do not have wild cards, do not do subdomain enumeration.
            Addresses.append(getAddrx(wDomain))
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
    print("\n\nDomains Located: ")
    pprint(Domains_Formatted_dups)
    
    return Domains_Formatted_dups

def remove_wildcard_domains(InScope):
    """
    Remove any initial '*.' wildcards with a period after it in a list of domain names.

    Parameters:
    domains (list): A list of domain names.

    Returns:
    A new list of domain names with the initial '*.' wildcard removed.
    """
    san_InScope = []
    for domain in InScope:
        if domain.startswith('*'):
            domain = domain[2:] if domain.startswith('*.') else domain[1:]
        san_InScope.append(domain)

    return san_InScope

def NameServerSearch(domains):
    print("\n\nName servers Found")
    for domain in domains:
        string = getNameServers_DIG(domain)
        NStorage.append(string) # This stores unformated NS

    unique_entries = set() # Create a unique set
    for entry in NStorage:
        unique_entries.add(tuple(entry))
            
    unique_entries = list(unique_entries) #organize
    ue = str(unique_entries)
    ue = ue.replace('(','')
    ue = ue.replace(')','')
    ue = ue.replace('"','')
    ue = ue.replace("b'",'')
    ue = ue.replace("'",'')
    ue = ue.replace('\n','')
    ue = ue.replace(' ','')
    ue = ue.replace('[','')
    ue = ue.replace(']','')


    ue = ue.split(',') # Seperates everything into a list
    ue4 = list(filter(lambda x: x.strip(), ue)) # Removes empties

    ue4 = [x[:-1] for x in ue4] # Removes '.' at the end

    ue4 = list(set(ue4)) # Removes duplicates

    return ue4
    

if args.ns:
    NS = True

if args.output:
    OUT = True
    name_of_csv = args.output
    #spreadsheet = open (name_of_csv, 'w', newline='') #Open Spreadsheet
    #writer = csv.writer(spreadsheet)

if args.json:
    json_file_var = args.json
    Saved_Scope = JSONParser(json_file_var) 
    Domains = JSONFIle(Saved_Scope)


    if NS == True:
        print("\n\nWarning: You are stepping into an experimental function.")
        NameServers = NameServerSearch(Saved_Scope[1]) # Will output name servers from in-scope domains
        pprint(NameServers)

    Include_Scope = Saved_Scope[1]
    San_Include_Scope = remove_wildcard_domains(Include_Scope)
    #This option here prints only found domains into a spreadsheet
    if NS == False and OUT == True:
        with open(name_of_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Sanitized Domain Names In-Scope","In-Scope Domains Provided","Domains Found", "PTR Addresses"])
            for i in range(max(len(Domains), len(Include_Scope))):
                if i < len(Domains):
                    domain = Domains[i]
                else:
                    domain = ''
                if i < len(Include_Scope):
                    InScope = Include_Scope[i]
                else:
                    InScope = ''
                if i < len(Addresses):
                    Addresses2 = Addresses[i]
                else:
                    Addresses2 = ''
                if i < len(San_Include_Scope):
                    San_Include_Scope2 = San_Include_Scope[i]
                else:
                    San_Include_Scope2 = ''
                    
                writer.writerow([San_Include_Scope2, InScope, domain, Addresses2])


    #This options here prints both domains found and name servers into a spreadsheet
    if NS == True and OUT == True:
        with open(name_of_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Sanitized Domain Names In-Scope", "In-Scope Domains Provided","Domains Found", "PTR Addresses", "Name Servers Found"])
            for i in range(max(len(Domains), len(NameServers), len(Include_Scope))):
                if i < len(Domains):
                    domain = Domains[i]
                else:
                    domain = ''
                if i < len(NameServers):
                    name_server = NameServers[i]
                else:
                    name_server = ''
                if i < len(Include_Scope):
                    InScope = Include_Scope[i]
                else:
                    InScope = ''
                if i < len(Addresses):
                    Addresses2 = Addresses[i]
                else:
                    Addresses2 = ''
                    
                if i < len(San_Include_Scope):
                    San_Include_Scope2 = San_Include_Scope[i]
                else:
                    San_Include_Scope2 = ''
                    
                writer.writerow([San_Include_Scope2, InScope, domain, Addresses2, name_server])

        
elif args.file:
    rfile     = args.file
    In_Scope  = RegScope(rfile)
    rfile_san = RegFile(In_Scope)

    
    print("\n\nWarning: You are stepping into an experimental function.")
    NameServers = NameServerSearch(rfile_san) # Will output name servers from in-scope domains
    pprint(NameServers)

    #This option here prints only found domains into a spreadsheet
    if NS == False and OUT == True:
        print("SEEEEES")
        with open(name_of_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["In-Scope Domains Provided","Domains Found", "PTR Addresses"])
            for i in range(max(len(rfile_san), len(In_Scope))):
                if i < len(rfile_san):
                    domain = rfile_san[i]
                else:
                    domain = ''
                if i < len(In_Scope):
                    InScope = In_Scope[i]
                else:
                    InScope = ''
                if i < len(Addresses):
                    Addresses2 = Addresses[i]
                else:
                    Addresses2 = ''
                writer.writerow([InScope, domain, Addresses2])

    
    #This options here prints both domains found and name servers into a spreadsheet
    if NS == True and OUT == True:
        print("TEEEEET")
        with open(name_of_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["In-Scope Domains Provided","Domains Found", "PTR Addresses", "Name Servers Found"])
    

            for i in range(max(len(In_Scope), len(rfile_san), len(NameServers))):
                if i < len(rfile_san):
                    domain = rfile_san[i]
                else:
                    domain = ''
                if i < len(NameServers):
                    name_server = NameServers[i]
                else:
                    name_server = ''
                if i < len(In_Scope):
                    InScope = In_Scope[i]
                else:
                    InScope = ''
                if i < len(Addresses):
                    Addresses2 = Addresses[i]
                else:
                    Addresses2 = ''
                writer.writerow([InScope, domain, Addresses2, name_server])

