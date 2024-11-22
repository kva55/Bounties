import subprocess, re, argparse, os


def runNmap(nargs, iL, command, debug, input_name, output_name):
    # append all args
    for arg in nargs:
        command += " "
        command += arg

    if debug == True:
        print(command)

    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    if debug == True:
        print(output.stdout)
        print("[+] livecheck complete")
    else:
        print("[+] livecheck complete")

def checkports(output_name):
    output_name += ".gnmap"
    result_dict = {}
    with open(output_name, 'r') as file:
        for line in file:
            # Only process lines starting with "Host:"
            if line.startswith("Host:"):
                parts = line.split()
                host = parts[1]  # Extract the IP address
                ports = []

                # Check if the line contains a "Ports:" section
                if "Ports:" in line:
                    # Extract the Ports section
                    port_info = line.split("Ports:")[1].strip()
                    port_entries = port_info.split(",")  # Split individual ports
                    for port_entry in port_entries:
                        if '/' in port_entry:
                            port_parts = port_entry.split("/")
                            port_num = port_parts[0]
                            port_state = port_parts[1]
                            service = port_parts[4] if len(port_parts) > 4 else "unknown"
                            ports.append({
                                #"port": port_num,
                                #"state": port_state,
                                #"service": service
                            })

                # Add data to the dictionary
                result_dict[host] = ports
    #print(result_dict)
    
    # The dictionary to traverse

    # Traverse the dictionary
    r = []
    for ip, ports in result_dict.items():
        # Print the IP address
        #print(f"IP Address: {ip}")
        r.append(ip)
    
        # Print the ports
        #for port_dict in ports:
        #    print(f"  Port: {port_dict['port'].strip()}")
    return r
    
def main():
    
    epilog="""
    sudo python3 livecheck.py --infile list.txt --outfile out.txt --outhost output.txt    
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
        output_name = "livecheck/" + output_name
        
    if args.outhost:
        host_name = args.outhost
        
    # Create dir
    os.system("mkdir livecheck")

    #output_name = "list.out.gnmap" 
    nargs       = ["-sn"]
    nargs.append("-oA " + output_name)
    iL          = input_name
    command     = "sudo nmap -iL" + " " + str(iL)
    debug       = False

    print("[*] Running livecheck")
    runNmap(nargs, iL, command, debug, input_name, output_name)
    r = checkports(output_name)
    #print(r)
    
    
    
    with open("livecheck/" + host_name, 'w') as file:
        for ip in r:
            file.write(ip + "\n")
    
    print("[+] Created " + host_name + " with up hosts")
        
if __name__ == "__main__":
    main()
