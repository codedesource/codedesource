#!/usr/bin/env bash

ffff_01="get_data_bnpe"
ffff_02="get_data_hubeau"
ffff_03="get_data_omm"

#clean screen
clear
#clean exec environment
echo "1- clear the repository"
sleep 2
rm scripts/$ffff_02.py
rm scripts/$ffff_03.py
rm *.log
#clean 'data' folder
rm -r data
rm -r .venv

echo "2- create venv and install library for each script"
sleep 2

python3 -m venv .venv
. .venv/bin/activate
pip install -r scripts/requirements.txt

# execute
echo "3-execute the scripts"
sleep 2

echo "3.1 - Convert"
jupyter nbconvert --to python scripts/$ffff_02.ipynb
jupyter nbconvert --to python scripts/$ffff_03.ipynb

echo "3.2 - Exec"
python3 scripts/$ffff_01.py &
python3 scripts/$ffff_02.py &
python3 scripts/$ffff_03.py &
wait
deactivate
echo "-- Everything is complete --"