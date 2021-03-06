import ROOT
import sys, ctypes, os
from StopsDilepton.tools.helpers import getObjFromFile
#from StopsDilepton.tools.tdrStyle import tdrStyle
#tdrStyle(padRightMargin=0.15)
from StopsDilepton.tools.interpolate import interpolate, rebin
from StopsDilepton.tools.niceColorPalette import niceColorPalette
from StopsDilepton.tools.localInfo import plotDir

#ifile = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test/isOS-nJets2p-nbtag1p-met80-metSig5-dPhiJet0-dPhiJet-mll20/limits/T2tt.root'

limitPosFix='2'
#ifile = "/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test/isOS-nJets2p-nbtag1p-met80-metSig5-dPhiJet0-dPhiJet-mll20/limits/flavSplit_almostAllReg/T2tt_limitResults.root"
#ifile = "/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test/isOS-nJets2p-nbtag1p-met60-metSig3-dPhiJet0-dPhiJet-mll20/limits/flavSplit_almostAllReg/T2tt_limitResults.root"

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--file", dest="filename", default="", type="string", action="store", help="Which file?")
(options, args) = parser.parse_args()

#ofilename = '/afs/hephy.at/user/r/rschoefbeck/www/etc/T2tt_flavSplit_almostAllReg_'+limitPosFix+'_'
ifs = options.filename.split('/')
ofilename = os.path.join(plotDir, 'T2tt', ifs[-4], ifs[-2], 'T2tt_limit')
if not os.path.exists(os.path.dirname(ofilename)):
  os.makedirs(os.path.dirname(ofilename))

T2tt_exp        = getObjFromFile(options.filename, "T2tt_exp")
T2tt_exp_up     = getObjFromFile(options.filename, "T2tt_exp_up")
T2tt_exp_down   = getObjFromFile(options.filename, "T2tt_exp_down")

T2tt_obs        = getObjFromFile(options.filename, "T2tt_exp").Clone('T2tt_obs') #FIXME!!! This is just for now...
T2tt_obs_UL     = T2tt_obs.Clone("T2tt_obs_UL") 
#theory uncertainty on observed limit
T2tt_obs_up   = T2tt_obs.Clone("T2tt_obs_up") 
T2tt_obs_down = T2tt_obs.Clone("T2tt_obs_down") 
T2tt_obs_up  .Reset() 
T2tt_obs_down.Reset() 
from StopsDilepton.tools.xSecSusy import xSecSusy
xSecSusy_ = xSecSusy()
for ix in range(T2tt_obs.GetNbinsX()):
  for iy in range(T2tt_obs.GetNbinsY()):
    mStop = T2tt_obs.GetXaxis().GetBinLowEdge(ix)
    mNeu  = T2tt_obs.GetYaxis().GetBinLowEdge(iy)
    v = T2tt_obs.GetBinContent(T2tt_obs.FindBin(mStop, mNeu))
    if v>0:
      scaleup = xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=1)/xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=0) 
      scaledown = xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=-1)/xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=0) 
      T2tt_obs_UL.SetBinContent(T2tt_obs.FindBin(mStop, mNeu), v*xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=0)) 
      T2tt_obs_up.SetBinContent(T2tt_obs.FindBin(mStop, mNeu), v*scaleup) 
      T2tt_obs_down.SetBinContent(T2tt_obs.FindBin(mStop, mNeu), v*scaledown) 

T2tt_obs_int = interpolate(T2tt_obs)
T2tt_obs_UL_int = interpolate(T2tt_obs_UL)
T2tt_obs_up_int = interpolate(T2tt_obs_up)
T2tt_obs_down_int = interpolate(T2tt_obs_down)
T2tt_exp_int = interpolate(T2tt_exp)
T2tt_exp_up_int = interpolate(T2tt_exp_up)
T2tt_exp_down_int = interpolate(T2tt_exp_down)

T2tt_obs_smooth = T2tt_obs_int.Clone("T2tt_obs_smooth")
T2tt_obs_up_smooth = T2tt_obs_up_int.Clone("T2tt_obs_up_smooth")
T2tt_obs_down_smooth = T2tt_obs_down_int.Clone("T2tt_obs_down_smooth")
T2tt_exp_smooth = T2tt_exp_int.Clone("T2tt_exp_smooth")
T2tt_exp_up_smooth = T2tt_exp_up_int.Clone("T2tt_exp_up_smooth")
T2tt_exp_down_smooth = T2tt_exp_down_int.Clone("T2tt_exp_down_smooth")
for i in range(1):
  T2tt_obs_smooth.Smooth()
  T2tt_obs_up_smooth.Smooth()
  T2tt_obs_down_smooth.Smooth()
  T2tt_exp_smooth.Smooth()
  T2tt_exp_up_smooth.Smooth()
  T2tt_exp_down_smooth.Smooth()

#  T2tt_obs_smooth = rebin(T2tt_obs_smooth)
#  T2tt_obs_up_smooth = rebin(T2tt_obs_up_smooth)
#  T2tt_obs_down_smooth = rebin(T2tt_obs_down_smooth)
#  T2tt_exp_smooth = rebin(T2tt_exp_smooth)
#  T2tt_exp_up_smooth = rebin(T2tt_exp_up_smooth)
#  T2tt_exp_down_smooth = rebin(T2tt_exp_down_smooth)

T2tt_obs_smooth.SetName("T2tt_obs_smooth")
T2tt_obs_up_smooth.SetName("T2tt_obs_up_smooth")
T2tt_obs_down_smooth.SetName("T2tt_obs_down_smooth")
T2tt_exp_smooth.SetName("T2tt_exp_smooth")
T2tt_exp_up_smooth.SetName("T2tt_exp_up_smooth")
T2tt_exp_down_smooth.SetName("T2tt_exp_down_smooth")


def getContours(h):
  _h = h.Clone()
  contlist = [0.5,1.0,1.5]
  idx = contlist.index(1.0)
  c_contlist = ((ctypes.c_double)*(len(contlist)))(*contlist)
  ctmp = ROOT.TCanvas()
  _h.SetContour(len(contlist),c_contlist)
  _h.Draw("contzlist")
  ctmp.Update()
  contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
  graph_list = contours.At(idx)
  contours = []
  np = 0
  idx_graph = 0
  for i in range(graph_list.GetEntries()):
      contours.append( graph_list.At(i).Clone("cont_"+str(i)) )
      if contours[i].GetN()>np:
          np=contours[i].GetN()
          idx_graph = i
  del ctmp
  return contours

ROOT.gStyle.SetPadRightMargin(0.15)
c1 = ROOT.TCanvas()
niceColorPalette(255)

contours_exp      = getContours(T2tt_exp_smooth)
contours_exp_up   = getContours(T2tt_exp_up_smooth)
contours_exp_down = getContours(T2tt_exp_down_smooth)
contours_obs      = getContours(T2tt_obs_smooth)
contours_obs_up   = getContours(T2tt_obs_up_smooth)
contours_obs_down = getContours(T2tt_obs_down_smooth)
  
contour_exp      = max(contours_exp     , key=lambda x:x.GetN()).Clone("contour_exp")   
contour_exp_up   = max(contours_exp_up  , key=lambda x:x.GetN()).Clone("contour_exp_up")
contour_exp_down = max(contours_exp_down, key=lambda x:x.GetN()).Clone("contour_exp_down")
contour_obs      = max(contours_obs     , key=lambda x:x.GetN()).Clone("contour_obs")
contour_obs_up   = max(contours_obs_up  , key=lambda x:x.GetN()).Clone("contour_obs_up")
contour_obs_down = max(contours_obs_down, key=lambda x:x.GetN()).Clone("contour_obs_down")

T2tt_obs.GetZaxis().SetRangeUser(0.02, 99)
T2tt_obs.Draw('COLZ')
c1.SetLogz()

def cleanContour(g):
  x, y = ROOT.Double(), ROOT.Double()
  remove=[]
  for i in range(g.GetN()):
    g.GetPoint(i, x, y)
    if  x>650 or (x<410) or y>250:
      remove.append(i)
  for i in reversed(remove):
    g.RemovePoint(i)
  
cleanContour(contour_exp)
cleanContour(contour_exp_up)
cleanContour(contour_exp_down)
cleanContour(contour_obs)
cleanContour(contour_obs_up)
cleanContour(contour_obs_down)

for g in [contour_exp, contour_exp_up, contour_exp_down, contour_obs_up, contour_obs_down]:
  g.Draw('same')

c1.Print(ofilename+'.png')

from StopsDilepton.PlotsSMS.inputFile import inputFile
from StopsDilepton.PlotsSMS.smsPlotXSEC import smsPlotXSEC
from StopsDilepton.PlotsSMS.smsPlotCONT import smsPlotCONT
from StopsDilepton.PlotsSMS.smsPlotBrazil import smsPlotBrazil

tempfilename = "tmp.root"
temp = ROOT.TFile(tempfilename,"recreate")
T2tt_obs_UL_int.Clone("T2tt_temperature").Write()
contour_exp.Write()
contour_exp_up.Write()
contour_exp_down.Write()
contour_obs.Write()
contour_obs_up.Write()
contour_obs_down.Write()
temp.Close()

# read input arguments
modelname = "T2tt" 
analysisLabel = "SUS-16-NaN" 
outputname = ofilename 

# read the config file
fileIN = inputFile('T2tt_limit.cfg')

# classic temperature histogra
xsecPlot = smsPlotXSEC(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
xsecPlot.Draw()
xsecPlot.Save("%sXSEC" %outputname)

# only lines
contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
contPlot.Draw()
contPlot.Save("%sCONT" %outputname)

# brazilian flag (show only 1 sigma)
brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
brazilPlot.Draw()
brazilPlot.Save("%sBAND" %outputname)

