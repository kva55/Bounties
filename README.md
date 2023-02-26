# BOSS - Bounty Osint Sniffer Software (Names a work-in-progress)
Currently this code enumerates all the IPs/ptr IPs, and name servers, based on a hackerone includes/excludes json file.
Custom domains can be added instead of hackerone yaml scope file with --file arg.

```python3 Main.py --json <hackerone.json>```

For custom input files, make sure to seperate each entry with a new line

```python3 Main.py --file <input.ext>```

To enumerate the name servers

```python3 Main.py --file or --json <input.ext> --ns``` **Note:** --ns is True by default, use --no-ns for no name server enumeration. Or just leave it out.

For saving your results in a csv file

```python3 Main.py --file or --json <input.ext> --output /path/to/file.csv```

Basic subdomain enumeration
```python3 CheckUp/assetfinder.py --input <input.txt> --output <path/to/file.csv>

Basic domain up test
```python3 CheckUp/CheckUp.py <Input: input.txt> <Output: path/to/file.csv>```
