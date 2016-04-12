# Reading out CMS pixel testbeam spreadsheets


## prerequisites:
* You will probaby need sudo rights on the mashine (doesn't work on the NAF)
* Make sure Python >= 2.7 is installed

```
pip install --upgrade oauth2client
pip install PyOpenSSL
git clone https://github.com/burnash/gspread.git
git clone https://github.com/clseitz/PixelScripts.git
cd PixelScripts
scp YOURUSERNAME@nafhh-cms05.desy.de:/nfs/dust/cms/user/clseitz/PixelTestbeam/gspread/gspread-test.json .
python ReadCMSPixeSheet.py 
```
The outputfile produced can be read in with the tele-scope package.
For the gain files and the data access create (or use softlinks) directories of the format:
```
calibrations/chipNUM/
data/run*.RAW
```
