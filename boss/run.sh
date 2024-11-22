# test
sudo python3 livecheck.py --infile list.txt --outfile list.txt --outhost livecheck_output.txt
sudo python3 portcheck.py --infile livecheck/livecheck_output.txt --outfile portcheck.txt --outhost portcheck_output.txt
python3 webcheck.py -i portcheck/portcheck_output.txt.csv
