# Bounties
Currently this code enumerates all the domains / ptr names based on a hackerone includes/excludes json file

```python3 Main.py --json <hackerone.json>```

For custom input files, make sure to seperate each entry with a new line

```python3 Main.py --file <input.ext>```

To enumerate the name servers

```python Main.py --file or --json <input.ext> --ns``` ***Note:*** The --ns is False by default
