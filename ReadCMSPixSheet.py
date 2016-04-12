#!/usr/bin/env python
#import gspread
import glob, os, sys
from oauth2client.service_account import ServiceAccountCredentials
import datetime
sys.path.insert(0, '../gspread')
import gspread

today = datetime.date.today()

def getSheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-test.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1W6qWHNanVM5SdUNaChfGVxdaGxb56xMxQIBOchOFdxs/edit#gid=0').sheet1
    return sheet



def getGlobalSettings(setups):
    Settings = []
    for setup in setups:
        cells = rl.range(rl.get_addr_int(setup.row, setup.col + 2)+":"+rl.get_addr_int(setup.row+5, setup.col + 2))
        cells = list(x.value for x in cells)
        cells.append(int(setup.row))
        print cells
        s = globalSettings(cells)
        Settings.append(s)
        
    return Settings


def getLocalSettings(setups):
    Settings = []
    for setup in setups:
        cells = rl.range(rl.get_addr_int(setup.row, setup.col + 1)+":"+rl.get_addr_int(setup.row, setup.col + 2))
        cells = list(x.value for x in cells)
        cells.append(int(setup.row))
        print cells
        s = localSettings(cells)
        Settings.append(s)
        
    return Settings


def getAllRuns(runs):
    AllRuns = []
    for run in runs:
        cells = rl.range(rl.get_addr_int(run.row, run.col + 3)+":"+rl.get_addr_int(run.row, run.col + 4))
        cells = list(x.value for x in cells)
        cells.append(int(run.row))
        r = cmsrun(cells)
        AllRuns.append(r)
        
    return AllRuns


class globalSettings:

    def __init__(self, (chip, refchip, geo, gain, refgain, gev, row)):
        self.chip = chip
        self.refchip = refchip
        self.geo = self.createGeoFile(geo)
        self.gain = 'calibrations/chip'+chip+'/'+gain
        self.refgain = 'calibrations/chip'+refchip+'/'+refgain
        self.gev = gev
        self.row = row

    def __repr__(self):
        return "\nchip %s\nrefchip %s\ngeo %s\ngain %s\nrefgain %s\nGeV %s\n" % ( self.chip, self.refchip, self.geo, self.gain, self.refgain, self.gev)

    def createGeoFile(self,geo):

        geoPositions =  [x for x in geo.split( ) if x.replace(".", "", 1).isdigit()]
        replacements = dict()
        for i in xrange(0,6):
            replacements['ZPOS'+str(i)] = geoPositions[i]

        inputFileName = 'geo_tmp.dat'
        outputFileName = 'geo'

        for elem in list(geo.split( )):
            outputFileName += '_'+elem
        outputFileName += '.dat'

        infile = open(inputFileName).read()

        if not os.path.isfile(outputFileName):
            outfile = open(outputFileName, 'w')
            outfile.write('# geometry ' + outputFileName.replace('.dat',''))
            for i in replacements.keys():
                infile = infile.replace(i, replacements[i])
            outfile.write(infile)   
            outfile.close

        return outputFileName



class localSettings:
    def __init__(self, (setting, value, row)):
        self.setting = setting
        self.value = value
        self.row = row
    def __repr__(self):
        if 'gain' in self.setting: 
            return "\n%s calibrations/chip%s/%s" % ( self.setting, self.value[1:4], self.value)
        else:
            return "\n%s %s" % ( self.setting, self.value)

class cmsrun:

    def __init__(self, (tilt, runnumber, row)):
        self.runnumber = runnumber
        self.tilt = tilt
        self.row = row

    def __repr__(self):
        if self.tilt is not "":
            return "\ntilt %s\nrun %s" % ( self.tilt, self.runnumber)
        else:
            return "run %s" % ( self.runnumber)



if __name__ == "__main__":
    rl = getSheet()

    GlobalSettings = getGlobalSettings( rl.findall("Global") )
    LocalSettings = getLocalSettings( rl.findall("Local") )
    allRuns = getAllRuns(rl.findall("#"))

    all = GlobalSettings + LocalSettings + allRuns 
    dictAll = {}
    for obj in all:
        dictAll[obj.row] = obj

    filename = "runs_"+"{:%d_%b_%Y}".format(today)+".dat"
    f = open(filename,"w")
    print >> f, 'weib 3 # gain file format for 2015'
    for key in sorted(dictAll):
        print >> f, dictAll[key]

    print "created output file: ",filename
    f.close()

