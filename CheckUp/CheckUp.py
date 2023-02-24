import sys
import csv
import socket

def check_domain(domain):
  try:
    # get the IP address for the domain
    ip_address = socket.gethostbyname(domain)
    # if we were able to get an IP address, the domain is active
    return True
  except:
    # if an exception was raised, the domain is not active
    return False

# get the file name and output file name from the command line arguments
file_name = sys.argv[1]
output_file_name = sys.argv[2]

# create an empty set to store the domain names we have already seen
seen_domains = set()

# open the input file and output file
with open(file_name, 'r') as file, open(output_file_name, 'w', newline='') as output_file:
  # create a CSV writer for the output file
  writer = csv.writer(output_file)

  # write the header row to the output file
  writer.writerow(['Domain', 'Status'])

  # read each line of the input file
  for line in file:
    domain = line.strip() # remove leading and trailing whitespace from the line
    status = 'UP' if check_domain(domain) else 'DOWN'
    
    # check if the domain has already been seen
    if domain in seen_domains:
      # if the domain has already been seen, skip it and continue to the next line
      continue
    else:
      # if the domain has not been seen, add it to the set of seen domains
      seen_domains.add(domain)
    
    if status == 'UP':
      # print the status and domain in green
      print(f"\033[32m{status}\033[0m: {domain}")
      status_color = 'GREEN'
    else:
      # print the status and domain in red
      print(f"\033[31m{status}\033[0m: {domain}")
      status_color = 'RED'
    writer.writerow([domain, status_color]) # write the domain and colored status to the output file
