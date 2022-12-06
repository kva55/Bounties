import sys
import json
import os.path
from os import path
from pprint import pprint

#variables that will hold the allowed domains
Exclude = []
Include = []
Exclude_Sorted = []
Include_Sorted = []

def HostCutter(Input):
    if str(Input).find('host') != -1:
        cut1 = str(Input).find('host')
        Input2 = str(Input)[cut1+8:]

        if(str(Input2).find(',')) != -1:
            cut2 = str(Input2).find(',')
            Input3 = str(Input2)[:cut2-2]
            

            Input3 = Input3.strip('^')
            Input3 = Input3.replace('\\','')

            if (str(Input3)).find('*') != -1:
                cut3 = (str(Input3)).find('*')
                Input4 = str(Input3)[cut3:]
                #print(Input4)
                return Input4
            
            #print(Input3)
            return Input3

def JSONParser(json_file_var):
    
    #Basic logic to see if file is attached.
    if len(sys.argv) > 1:

        scopef = json_file_var #sys.argv[1]
        if path.exists(scopef):
            print("Hackerone Scope Verifier.\nFile attached is: " + scopef)

            #open the json file
            fopen = open(scopef)
            jdata = json.load(fopen)
            for key, value in jdata.items():
                if isinstance(value, dict):
                    for key1, value1 in value.items():
                        if isinstance(value1, dict):
                            for key2, value2 in value1.items():
                                if key2 == "exclude":
                                    #print("\nExclude: ")
                                    for step in value2:
                                        Exclude.append(HostCutter(step))
                                        
                                        
                                        
                                if key2 == "include":
                                    #print("\nInclude: ")
                                    for step in value2:
                                        HostCutter(step)
                                        Include.append(HostCutter(step))

            fopen.close()
            Include_Sorted = list(dict.fromkeys(Include)) 
            Exclude_Sorted = list(dict.fromkeys(Exclude))
            #print("\n\nInclude List")
            #pprint(Include_Sorted)
            #print("Exclude List")
            #pprint(Exclude_Sorted)

            return Exclude_Sorted, Include_Sorted # Will return tuple
            
        else:
            print("Hackerone Scope Verifier.\nFile not found: " + scopef)

    else:
        print("Hackerone Scope Verifier.\n***No file attached***")
        exit(0) #Remove later


#JSONParser()
#print(Include_Sorted, Exclude_Sorted)
