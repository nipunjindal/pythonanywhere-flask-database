mv ~/Downloads/Data.mdb Data.mdb
mdb-export Data.mdb Info > Info.csv
mdb-export Data.mdb FILE > FILE.csv
python playground.py
cp data.csv ../data/data.csv
