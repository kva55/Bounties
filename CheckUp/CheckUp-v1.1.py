import sys
import csv
import asyncio

async def main(file_name, output_file_name):
  # create an empty set to store the domain names we have already seen
  seen_domains = set()

  # open the input file and output file
  with open(file_name, 'r') as file, open(output_file_name, 'w', newline='') as output_file:
    # create a CSV writer for the output file
    writer = csv.writer(output_file)

    # write the header row to the output file
    writer.writerow(['Domain', 'Status'])

    # create a list of tasks to check each domain
    tasks = []
    for line in file:
      domain = line.strip() # remove leading and trailing whitespace from the line

      # check if the domain has already been seen
      if domain in seen_domains:
        # if the domain has already been seen, skip it and continue to the next line
        continue
      else:
        # if the domain has not been seen, add it to the set of seen domains
        seen_domains.add(domain)

      # create a task to check the domain using asyncio
      tasks.append(asyncio.create_task(check_domain(domain)))

    # wait for all the tasks to complete
    results = await asyncio.gather(*tasks)

    # loop through the results and write them to the output file
    for domain, status in zip(seen_domains, results):
      if status:
        # print the status and domain in green
        print(f"\033[32mUP\033[0m: {domain}")
        status_color = 'GREEN'
      else:
        # print the status and domain in red
        print(f"\033[31mDOWN\033[0m: {domain}")
        status_color = 'RED'
      writer.writerow([domain, status_color]) # write the domain and colored status to the output file

if __name__ == '__main__':
  file_name = sys.argv[1]
  output_file_name = sys.argv[2]

  asyncio.run(main(file_name, output_file_name))
