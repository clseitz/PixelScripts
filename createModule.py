import datetime
import time
import sys, os


###### name the qualificiation procedure and module settings
quali = 'FullQualification'
tbm = 'TBM08c'
roc = 'digv21respin'

###### Define your tests and temperature (extended pretest with pixel alive map)
tests = ['Pretest_p17','Fulltest_m20','Cycle','Fulltest_m20','IV_m20','Fulltest_p17','IV_p17']
#tests = ['Pretest_p17_prod12','Timingtest_p17_prod12','Fulltest_p17_prod12','Pretest_p17_prod11','Timingtest_p17_prod11','Fulltest_p17_prod11']
#Official sequence, not ours
#tests = ['Fulltest_m20','Cycle','Fulltest_m20','IV_m20','Fulltest_p17','IV_p17']
temps = ['17','-25']
ncycles = '10'

#dtb list
#old exchange C
#dtbs = {'A':'DTB_WS6C22','B':'DTB_WS913S','C':'DTB_WS6OKA','D':'DTB_WS6K9F'}
dtbs = {'A':'DTB_WS6C22','B':'DTB_WS913S','C':'DTB_WS8ZAW','D':'DTB_WS6K9F'}


ts = time.time()
d = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%Hh%Mm')
stamp = str ( int( ts ) )


if len(sys.argv) >= 2:
    inFile = open(sys.argv[1],'r')
else:
    print 'Please give text file input in table format with module number and DTB (A, B, C, D) \n'
    print '0000 A \n'
    print '0001 B \n'

#read in modules from textfile
modules = {}
for line in inFile.readlines():
    text =  line.strip().split(' ')
    modules[text[0]] = text[1]

#create folder of the day
testday = 'Testing_'+d
cmd = 'mkdir '+testday
print cmd
os.popen(cmd)

#create log file to document what is in the test folder
logF = open(testday+ '/Log.txt','a')
logF.write('Timestamp: ' + dt + '_' + stamp + ' \n')
for mod in modules:
    logF.write(mod + ' ')
    logF.write(modules[mod]+'\n')

for i,test in enumerate(tests):
    logF.write(str(i) + '  ' + test)
    logF.write(' \n')
logF.write('\n')
logF.close()

# create one dummy folder for testing
folder = 'dummy' + testday + '_' + dt+ '_' + stamp
cmd = '/home/cmspix/pxar/main/mkConfig -d ' + folder + ' -t ' + tbm + ' -r ' + roc + '  -m'
print cmd
os.popen(cmd)

##Creat the necessary test structure
###########################
FolderList=[]

for mod in modules:
    print mod, modules[mod]
    FolderList.append('M' + mod + '_' + quali + '_' + dt+ '_' + stamp)
    folder = testday+ '/M' + mod + '_' + quali + '_' + dt+ '_' + stamp

    cmd = 'mkdir '+folder
    print cmd
    os.popen(cmd)
    cfgfolder =  folder + '/configfiles'
    cmd = 'mkdir -p '+ cfgfolder 
    print cmd
    os.popen(cmd)

    for i,test in enumerate(tests):
        if test == 'Cycle':
            cmd = 'mkdir ' + folder + '/' + str ( i ).zfill(3) + '_' + test
            print cmd
            os.popen(cmd)
        else:
            cmd = '/home/cmspix/pxar/main/mkConfig -d ' + folder + '/' + str ( i ).zfill(3) + '_' + test + ' -t ' + tbm + ' -r ' + roc + ' -c ' + dtbs[modules[mod]] + ' -m'
            print cmd
            os.popen(cmd)
        

        cmd = cfgfolder+ '/Tests.ini'
        print cmd
        f = open(cfgfolder+ '/Tests.ini','w')
        f.write('[Tests] \n')
        f.write('TestDescription: ' + quali + '\n')
        f.write('Test: ')
        for test in tests:
            test = test.replace('_m','@-')
            test = test.replace('_p','@')
            f.write(test + ',')
        f.write('\n')
        if 'Cycle' in tests:
            f.write('[Cycle] \n')
            f.write('highTemp: ' + temps[0] + ' \n')
            f.write('lowTemp: ' + temps[1] + ' \n')
            f.write('nCycles: ' + ncycles + ' \n')

        f.close()

###############
##Make shell scripts for executing all the tests simultanesouly
for i,test in enumerate(tests):
    fsh = open(testday +'/' +str ( i ).zfill(3)+'_'+test + '_' + stamp + '.sh','w')
    for folder in FolderList:
        #Pretest and Fulltest can be done in parallel
        if 'Pretest' in test:
            #fsh.write('cat /home/cmspix/pxar/main/mPretest | /home/cmspix/pxar/bin/pXar -d '+ folder + '/' + str ( i ).zfill(3) + '_' + test + ' &\n')
            fsh.write('mate-terminal --tab --title=\"' + folder + '\" -e \"/bin/bash -c \'cat /home/cmspix/pxar/main/mPretest | /home/cmspix/pxar/bin/pXar -d '+ folder + '/' + str ( i ).zfill(3) + '_' + test + ';  exec /bin/bash -i\'\" \n')
        if 'Fulltest' in test:
            fsh.write('mate-terminal --tab --title=\"' + folder + '\" -e \"/bin/bash -c \'cat /home/cmspix/pxar/main/mtest | /home/cmspix/pxar/bin/pXar -d '+ folder + '/' + str ( i ).zfill(3) + '_' + test + ';  exec /bin/bash -i\'\" \n')
            #fsh.write('cat /home/cmspix/pxar/main/mtest | /home/cmspix/pxar/bin/pXar -d '+ folder + '/' + str ( i ).zfill(3) + '_' + test + ' &\n')
        #IV curve needs to be done sequentially
        if 'IV' in test:
            fsh.write('/home/cmspix/pxar/bin/pXar -d '+ folder + '/' + str ( i ).zfill(3) + '_' + test + ' -t IV \n')
    fsh.close()
    cmd = "chmod +x "+testday +'/' +str ( i ).zfill(3)+'_'+test + '_' + stamp + '.sh'
    print cmd
    os.popen(cmd)
#############################

##################
## creat script to tar everything in the end
ftar = open(testday +'/' +str ( i +1).zfill(3)+'_tarFolders_' + stamp + '.sh','w')
for folder in FolderList:
    ftar.write('tar cvzf '+ folder +'.tgz '+folder+' \n')
ftar.close()
cmd = "chmod +x "+testday +'/'  +str ( i +1 ).zfill(3)+'_tarFolders_' + stamp + '.sh'
print cmd
os.popen(cmd)
###################
