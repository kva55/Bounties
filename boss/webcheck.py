import subprocess, re, argparse, os, csv, glob
import pandas as pd
import requests



def gowitness(ip, port):
    print("Taking screenshot")
    os.system("gowitness scan single --screenshot-path webcheck/" + ip + " -u http://" + ip + ":" + port +" --write-db")
    os.system("gowitness scan single --screenshot-path webcheck/" + ip + " -u https://" + ip + ":" + port +" --write-db")

def curl(ip, port):
    url = "http://" + ip + ":" + port
    url2 = "https://" + ip + ":" + port
    http_status_code = ""
    https_status_code = ""
    response  = ""
    response2 = ""

    with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ip","port","http-resp","https-resp","http-status","https-status","http-headers","https-headers"])        

    try:
        response = requests.get(url, timeout=30, verify=False)
        http_status_code = response.status_code
        http_headers = response.headers

    except Exception as e:
        e1 = e
        #with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerow([ip,port,e,"/","/","/","/","/"])
    try:
        
        response2 = requests.get(url2, timeout=30, verify=False)
        https_status_code = response2.status_code
        https_headers = response2.headers


        #with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerow([ip,port,response,response2,http_status_code, https_status_code, http_headers, https_headers])  
        
    except Exception as e:
        e2 = e
        #print(e)
        #with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerow([ip,port,"/",e,"/","/","/","/"])

    if http_status_code != "" and https_status_code != "":
        with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip,port,response,response2,http_status_code, https_status_code, http_headers, https_headers])

    elif http_status_code == "" and https_status_code != "":
        with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip,port,e1,response2,"/", https_status_code, "/", https_headers])
        
    elif http_status_code != "" and https_status_code == "":
        with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip,port,response,e2,http_status_code, "/", http_headers, "/"])

    elif http_status_code == "" and https_status_code == "":
        with open("webcheck/" + ip + "/" + "curling_" + ip + "-" + port + ".csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip,port,e1,e2,"/", "/", "/", "/"])
    

def main():
    
    epilog="""
    sudo python3 webcheck.py --infile list.txt --outfile out.txt --outhost output.txt    
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", help="in file", type=str)
    parser.add_argument("-o", "--outfile", help="out file (nmap)", type=str)
    parser.add_argument("-oh", "--outhost", help="outfile (hosts)", type=str)
    
    args = parser.parse_args()

    if args.infile:
        input_name = args.infile

    if args.outfile:
        output_name = args.outfile
        output_name = "webcheck/" + output_name
        
    if args.outhost:
        host_name = args.outhost

    os.system("mkdir webcheck")
    
    with open(input_name, 'r') as file:
        for line in file:
            
            a = line
            a = a.replace("\'","")
            a = a.replace("[","")
            a = a.replace("]","")
            a = a.replace('"',"")
            a = a.replace('\n',"")
            a = a.replace(' ',"")
            a = a.split(',')
            #print(a)



            b = a[0]    # ip
            a.remove(b) # all ports

            # create dir
            os.system("mkdir " + "webcheck/" + b)

            for port in a:
                curl(b, port)
                # merge all csv

                # Take screenshots
                gowitness(b, port)

            csv_files = glob.glob("webcheck/" + b + "/" + "*.csv")
            combined_csv = pd.concat([pd.read_csv(file) for file in csv_files])
            output_file = "webcheck/" + b + "/curling_ports.csv"
            combined_csv.to_csv(output_file, index=False)
                
        
if __name__ == "__main__":
    main()
