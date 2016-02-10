#!/usr/bin/env python
from ROOT import *
import glob, os, sys
from array import array


gROOT.SetBatch(kTRUE) 
outdir = "QuickCheckRetest"
postfix = ".png"

def _makelabel(text):
    pt = TPaveText(0.3507014,0.9013333,0.6012024,0.9573333,"br")
    pt.SetFillColor(0)
    pt.SetFillStyle(0)
    pt.SetLineColor(0)
    pt.SetShadowColor(0)
    pt.SetTextColor(1)
    pt.AddText(text);
    return pt


def _modmap(rocs, colors, logy=False, distthr=False):
    if len(colors) > 1:
        color = array('i', colors)
        gStyle.SetPalette( 4, color);
    else:
        gStyle.SetPalette(1)

    c = TCanvas("modmap","modmap",2200,800)

    c.cd()
    gPad.SetMargin(0.3,0.3,0.2,0.3)
    c.Divide(8,2,0,0)    

    #modmap.Divide(8,2)

    gStyle.SetOptStat(0)
    for i,roc in enumerate(rocs):
        if not distthr:
            roc.SetTitle("ROC "+ str(i))
        if distthr:
            roc.SetTitle("ROC "+ str(i)+"    RMS={:.3f}".format(roc.GetRMS()))


        if (i<8):
            c.cd(8-i)
            if (roc.GetNbinsY() > 1):
                h2 = roc.Clone()
                for col in range(0, 52):
                    for row in range(0, 80):
                        roc.SetBinContent(col+1, row+1, h2.GetBinContent(52-col, 80-row))
        else:
            c.cd(i+1)


        roc.GetXaxis().SetTickSize(0.00001)
        roc.GetYaxis().SetTickSize(0.00001)
        roc.GetZaxis().SetTickSize(0.00001)
        roc.GetXaxis().SetLabelSize(0.08)
        roc.GetYaxis().SetLabelSize(0.05)

        if ((i!=8) & (i!=7)):
            roc.GetYaxis().SetLabelSize(0.)

        if (i<8):
            roc.GetXaxis().SetLabelSize(0.0)




#        c.cd(i+1)

        if logy:
            gPad.SetLogy()




        roc.Draw("col")


    return c
    
def PixelAlive(tfile, testName, modName):
    rocs = []
    colors=[0, 1, 2, 3, 4, 5, 6]
    for i in range (0,16):
        hist = tfile.Get("PixelAlive/PixelAlive_C"+ str(i) + "_V0")
        rocs.append(hist)
    
    c = _modmap( rocs , colors)
    pt = _makelabel(testName +" "+ modName +" Pixel Alive map")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_Alive" + postfix)
    return c

def BB2(tfile, testName, modName):
    thrwidth_rocs = []
    bb2_rocs = []
    colors=[0, 1, 3, 2]
    for i in range (0,16):
        hist = tfile.Get("BB2/BBtestMap_C"+ str(i) + "_V0")
        bb2_rocs.append(hist)
        hist = tfile.Get("BB2/CalsVthrPlateauWidth_C"+ str(i) + "_V0")
        thrwidth_rocs.append(hist)


    c = _modmap( bb2_rocs , colors)
    pt = _makelabel(testName +" "+ modName +" BB2 Map")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" +modName+ "/" + testName+ "_BB2" + postfix)

    c = _modmap( thrwidth_rocs , colors, True)
    pt = _makelabel(testName +" "+ modName + " BB2 ThrWidth Distribution")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" +modName+ "/" + testName+ "_BB2_ThrWidth" + postfix)

    return 0

def Trim(tfile, testName, modName):
    thrfinal = []
    thrfinal = []
    distthrfinal = []
    thrinitial = []    
    
    colors=[0]
    for i in range (0,16):
        hist = tfile.Get("Trim/thr_TrimThrFinal_vcal_C"+ str(i) + "_V0")
        hist.SetMinimum(0)
        hist.SetMaximum(45)
        thrfinal.append(hist)
        
        hist = tfile.Get("Trim/dist_thr_TrimThrFinal_vcal_C"+ str(i) + "_V0")
        hist.GetXaxis().SetRangeUser(0,60)
        hist.SetStats(0)
        distthrfinal.append(hist)

        hist = tfile.Get("Trim/thr_TrimThr0_vthrcomp_C"+ str(i) + "_V0")
        hist.SetMinimum(0)
        hist.SetMaximum(150)
        thrinitial.append(hist)

    c = _modmap( thrinitial , colors)
    pt = _makelabel(testName +" "+ modName +" Threshold Map before Trimming Range 0 - 150")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrMapInitial" + postfix)    
    c = _modmap( thrfinal , colors)
    pt = _makelabel(testName +" "+ modName +" Threshold Map after Trimming Range 0 - 45")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrMapFinal" + postfix)

    c = _modmap( distthrfinal , colors, True, True)
    pt = _makelabel(testName +" "+ modName +" Threshold Dist after Trimming")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrDistFinal" + postfix)



    return c


def PhHeighOpt(tfile, testName, modName):
    PhLow = []
    PhHigh = []
    PhLowDist = []
    PhHighDist = []

    
    colors=[0]
    for i in range (0,16):
        hist = tfile.Get("PhOptimization/PH_mapLowVcal_C"+ str(i) + "_V0")
        hist.SetMinimum(0)
        hist.SetMaximum(100)
        PhLow.append(hist)
        
        hist = tfile.Get("PhOptimization/PH_mapHiVcal_C"+ str(i) + "_V0")
        hist.SetMinimum(150)
        hist.SetMaximum(255)
        PhHigh.append(hist)

        hist = tfile.Get("PhOptimization/dist_PH_mapLowVcal_C"+ str(i) + "_V0")
        PhLowDist.append(hist)
        
        hist = tfile.Get("PhOptimization/dist_PH_mapHiVcal_C"+ str(i) + "_V0")
        PhHighDist.append(hist)


    c = _modmap( PhLow, colors)
    pt = _makelabel(testName +" "+ modName +" PulseHeight map low Vcal Range 0 - 100")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_PhLow" + postfix)    

    c = _modmap( PhHigh, colors)
    pt = _makelabel(testName +" "+ modName +" PulseHeight map high Vcal Range 150 - 255")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_PhHig" + postfix)    

    c = _modmap( PhLowDist, colors)
    pt = _makelabel(testName +" "+ modName +" PulseHeight Dist low Vcal")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_PhLowDist" + postfix)

    c = _modmap( PhHighDist, colors)
    pt = _makelabel(testName +" "+ modName +" PulseHeight Dist high Vcal")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_PhHigDist" + postfix)        


    return c


def IVCurve(ivFile,testName,  modName):
    from array import array
    V = []
    A = []
    for line in ivFile.readlines():
        if not '#' in line:
            (Vi, Ai) = line.split("\t")[0:2]
            V.append(-1 * float(Vi))
            A.append(-1 * float(Ai)* pow(10,6))
    x = array("d", V) 
    y = array("d", A) 
    g =  TGraph(len(x), x, y)
    c = TCanvas("bla","bla", 800,600)
    gPad.SetLogy()
    g.Draw("ac")
    g.SetTitle("IV curve")
    g.GetYaxis().SetTitle("Current in #mu A")
    g.GetXaxis().SetTitle("Voltage in V")
    c.SaveAs(outdir + "/" + modName+ "/" +testName+"_IVcurve" + postfix)
    return
def HtmlMod(modName, plots):
    f = open(outdir + "/"+modName + ".html",'w')
    f.write("<html> \n")
    f.write("<head> \n")
    f.write("<title>Quick Module Qualification</title> \n")
    f.write("</head> \n")
    f.write("<body> \n")
    width = '600'
    height = '200'
#    plots = {}
#    plots.update( "000_Pretetes_17": [  x for x in plots if "000" in x  })

    pretest =  [  x for x in plots if "000" in x ]
    fulltest1 =  [  x for x in plots if "001" in x ]
    fulltest2 =  [  x for x in plots if "003" in x ]
    fulltest3 =  [  x for x in plots if ("005_F" in x or "004_F" in x) ]
    IV_p17 =  [  x for x in plots if "006" in x ]
    IV_m20 =  [  x for x in plots if "004" in x ]
    f.write("<h1> 000_Pretest_p17</h1> <br>")
    for plot in pretest:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="'+ height + '" width="'+ width +'"> </a> \n' )

    f.write("<h1> 001_Fulltest_m20</h1> <br>")
    for plot in fulltest1:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="'+ height + '" width="'+ width +'"> </a> \n' )

    f.write("<h1> 003_Fulltest_m20</h1> <br>")
    for plot in fulltest2:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="'+ height + '" width="'+ width +'"> </a> \n' )

    f.write("<h1> 004_Fulltest_p17</h1> <br>")
    for plot in fulltest3:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="'+ height + '" width="'+ width +'"> </a> \n' )

    f.write("<h1> 006_IVCurve_p17</h1> <br>")
    for plot in IV_p17:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="300" width="400"> </a> \n' )

    f.write("<h1> 003_IVCurve_m20</h1> <br>")
    for plot in IV_m20:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="300" width="400"> </a> \n' )

    f.write("</body> \n")
    f.write("</html> \n")



def HtmlIndex(modules):
    f = open(outdir + "/index.html",'w')
    f.write("<html> \n")
    f.write("<head> \n")
    f.write("<title>Quick Module Qualification</title> \n")
    f.write("</head> \n")
    f.write("<body> \n")
    
    for mod in modules:
        f.write('<a href="' + mod +'.html">Module ' + mod +' </a> <br> \n' )

    f.write("</body> \n")
    f.write("</html> \n")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        inDir = sys.argv[1]
    else:
	print "Will stop, give input Dir"
        quit()


    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)
    modules = []
    for fileName in glob.glob(inDir+'/*/*/pxar.root'):
        
        tfile = TFile(fileName,"READ")
        modName = fileName[fileName.find("M"):fileName.find("M") + 5 ]
        modules.append(modName)
        testName = fileName[ fileName.find("/0") +1 : fileName.find("/pxa")]
        try:
            os.stat(outdir + "/"+modName)
        except:
            os.mkdir(outdir + "/"+modName)
        print fileName
        if 'Timing' in fileName:
            continue
        if not "IV" in fileName:
            PixelAlive(tfile, testName, modName)
            BB2(tfile, testName, modName)
            if "Fulltest" in fileName:   
                BB2(tfile, testName, modName)
                Trim(tfile, testName, modName)
                PhHeighOpt(tfile, testName, modName)
        elif "IV" in fileName:
            ivFileName = fileName.replace("pxar.root","ivCurve.log")
            ivFile = open(ivFileName, 'r')
            IVCurve(ivFile, testName,modName)
    modules = set(modules)
    plots = []

    for mod in modules:
        plots = sorted(glob.glob(outdir + "/" + mod +"/*" + postfix))
        plots = [ x.replace(outdir + "/", "") for x in plots ]

        HtmlMod(mod, plots)

    HtmlIndex(modules)
