# BOSS - Bounty Osint Sniffer Software (Names a work-in-progress)
Currently this code enumerates all the domains / ptr names based on a hackerone includes/excludes json file

```python3 Main.py --json <hackerone.json>```

For custom input files, make sure to seperate each entry with a new line

```python3 Main.py --file <input.ext>```

To enumerate the name servers

```python3 Main.py --file or --json <input.ext> --ns``` **Note:** --ns is True by default, use --no-ns for no name server enumeration. Or just leave it out.
