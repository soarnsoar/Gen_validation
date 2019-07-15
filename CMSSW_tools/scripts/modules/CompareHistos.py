import ROOT
import math
import os
from decimal import Decimal

ROOT.gROOT.SetBatch(ROOT.kTRUE)


#ROOT.TGraphAsymmErrors

##--No Graphical Window

#ROOT.gROOT.SetBatch(ROOT.kTRUE)




def Ratio(A,B):


    if B==0.:
        return 0.
    else:
        return A/B
#        CompareTGraphAsymmErrorsWithStat(xaxis,yaxis,yaxis_ratio,title,h1,h1stat,label1,color1,h0,h0stat,label0,color0,store_filepath,True)

def SetStyleStat(h1stat,color1,h2stat,color2):
    h1stat.SetLineColor(color1)
    h1stat.SetFillColor(0)
    h1stat.SetLineStyle(1)

    h2stat.SetLineColor(color2)
    h2stat.SetFillColor(0)
    h2stat.SetLineStyle(1)

    
def SetStyleSys(h1,color1,h2,color2):
    h1.SetLineColor(color1)
    h1.SetFillColorAlpha(color1,0.5)
    h1.SetFillStyle(3001)
    h1.SetLineStyle(1)

    h2.SetLineColor(color2)
    h2.SetFillColorAlpha(color2,0.5)
    h2.SetFillStyle(3001)
    h2.SetLineStyle(1)

def SetStyleTotal(h1__total,color1,h2__total,color2):
    h1__total.SetLineColor(color1)
    h1__total.SetFillColorAlpha(color1,0.5)
    h1__total.SetFillStyle(3004)
    h1__total.SetLineStyle(1)
    
    h2__total.SetLineColor(color2)
    h2__total.SetFillColorAlpha(color2,0.5)
    h2__total.SetFillStyle(3004)
    h2__total.SetLineStyle(1)
    




def ErrorCombineSqrtSumTGraphAsymmErrors(h1,h2):
    ##--Combine graphs with the same value but different error(stat, sys graphs)
    nbin=h1.GetN()

    if h1.GetX()!=h2.GetX():
        print "[CompareHistos.GetRatioTGraphAsymmErrors] x binning is not equal"
    if h1.GetY()!=h2.GetY():
        print "[CompareHistos.GetRatioTGraphAsymmErrors] y value is not equal"

    h__combine=ROOT.TGraphAsymmErrors(nbin)

    for iBin in range(0,nbin):
        x1=h1.GetX()[iBin]
        ex1_up=h1.GetErrorXhigh(iBin)
        ex1_dn=h1.GetErrorXlow(iBin)

        x2=h2.GetX()[iBin]
        ex2_up=h2.GetErrorXhigh(iBin)
        ex2_dn=h2.GetErrorXlow(iBin)


        y1=h1.GetY()[iBin]

        ey1_up=h1.GetErrorYhigh(iBin)
        ey1_dn=h1.GetErrorYlow(iBin)


        y2=h2.GetY()[iBin]
        ey2_up=h2.GetErrorYhigh(iBin)
        ey2_dn=h2.GetErrorYlow(iBin)

        h__combine.SetPoint(iBin, x1, y2)
        h__combine.SetPointError(iBin,(ex1_dn),(ex1_up), math.sqrt(ey1_dn**2 + ey2_dn**2), math.sqrt(ey1_up**2 + (ey2_up)))

    return h__combine

def GetYZeroTGraphAsymmErrors(h):
    #-- multiply scale to y values    
    nbin=h.GetN()
    hzero=h.Clone()
    for iBin in range(0,nbin):
        hzero.SetPoint(iBin,h.GetX()[iBin], 0)
        hzero.SetPointError(iBin, h.GetErrorXlow(iBin),h.GetErrorXhigh(iBin), h.GetErrorYlow(iBin), h.GetErrorYhigh(iBin)   )
        #print '[h.GetErrorYlow(iBin)]=',h.GetErrorYlow(iBin)
    #print 'h.GetErrorXhigh(0)=',h.GetErrorXhigh(0)

    return hzero


def ScaleTGraphAsymmErrors(h,scale):
    #-- multiply scale to y values
    nbin=h.GetN()

    for iBin in range(0,nbin):
        h.SetPoint(iBin,h.GetX()[iBin], scale*h.GetY()[iBin])
        h.SetPointError(iBin, h.GetErrorXlow(iBin),h.GetErrorXhigh(iBin), scale*h.GetErrorYlow(iBin), scale*h.GetErrorYhigh(iBin)   )

        

def TGraphAsymmErrorsToTH1D(h,name):
    
    #print h.GetN()+1
    print "[TGraphAsymmErrorsToTH1D]"
    
    IsSym=True
    for iBin in range(0,   h.GetN()  ):
        if h.GetErrorYhigh(iBin)!=h.GetErrorYlow(iBin):
            print "Error high/low are not equal"
            IsSym=False
            break

    th1d=ROOT.TH1D()
    if IsSym:
        th1d=ROOT.TH1D(name,name,h.GetN()+1,h.GetX()[0],h.GetX()[h.GetN()-1])
        for iBin in range(0, h.GetN()):
            th1d.SetBinContent(iBin+1,h.GetY()[iBin])
            th1d.SetBinError(iBin+1,h.GetErrorYhigh(iBin))
            #print "h.GetY()[iBin]=",h.GetY()[iBin]
            #print "h.GetErrorYhigh(iBin)=",h.GetErrorYhigh(iBin)
        return th1d
    else:

        print "[TGraphAsymmErrorsToTH1D] not matched Error High/Low"

        

def GetRatioTGraphAsymmErrors(h1,h2):
    ##h1/h2
    nbin=h1.GetN()
    
    if h1.GetX()!=h2.GetX():
        print "[]CompareHistos.GetRatioTGraphAsymmErrors] x binning is not equal"

    tgr_h1_over_h2=ROOT.TGraphAsymmErrors(nbin)

    for iBin in range(0,nbin):
        x1=h1.GetX()[iBin]
        ex1_up=h1.GetErrorXhigh(iBin)
        ex1_dn=h1.GetErrorXlow(iBin)

        x2=h2.GetX()[iBin]
        ex2_up=h2.GetErrorXhigh(iBin)
        ex2_dn=h2.GetErrorXlow(iBin)


        y1=h1.GetY()[iBin]

        ey1_up=h1.GetErrorYhigh(iBin)
        ey1_dn=h1.GetErrorYlow(iBin)


        y2=h2.GetY()[iBin]
        ey2_up=h2.GetErrorYhigh(iBin)
        ey2_dn=h2.GetErrorYlow(iBin)

        tgr_h1_over_h2.SetPoint(iBin, x1, Ratio(y1,y2))
        tgr_h1_over_h2.SetPointError(iBin, ex1_dn,ex1_up, Ratio(ey1_dn,y2), Ratio(ey1_up,y2 )   )
        #print '[Ratio(ey1_dn,y2)]=',Ratio(ey1_dn,y2)
    return tgr_h1_over_h2

    

def StatTestCentralValueTGraphAsymmErrors(test_stat,h1stat,h2stat):
    th1d_stat1=TGraphAsymmErrorsToTH1D(h1stat,'hstat1')
    th1d_stat2=TGraphAsymmErrorsToTH1D(h2stat,'hstat2')

    run_stat_test=getattr(th1d_stat1,test_stat)
    pvalue=run_stat_test(th1d_stat2,'WW P')
    print "p-value="+str(pvalue)
    return pvalue
    #pass_stat_central=False
    #if pvalue > pvalue_threshold:
    #    pass_stat_central=True
    '''
    else:
        print "[CompareHistos] Run alternative test method :: KolmogorovTest"
        run_stat_test=getattr(th1d_stat1,'KolmogorovTest')
        pvalue=run_stat_test(th1d_stat2,'WW P')
        print "p-value="+str(pvalue)
    '''
    del th1d_stat1
    del th1d_stat2


def StatTestErrorValueTGraphAsymmErrors(test_stat,h1,h1stat,h2,h2stat):

    IsSymErr=True
    
    for iBin in range(0, h1.GetN()):
        if h1.GetErrorYhigh(iBin)!=h1.GetErrorYlow(iBin):
            IsSymErr=False
        if h2.GetErrorYhigh(iBin)!=h2.GetErrorYlow(iBin):
            IsSymErr=False
    print "IsSymErr=",IsSymErr
    if IsSymErr:
        #--- Set TH1D whose y is sys err
        th1d_1=ROOT.TH1D('1','1',h1.GetN()+1,h1.GetX()[0],h1.GetX()[h1.GetN()-1])
        th1d_2=ROOT.TH1D('2','2',h2.GetN()+1,h2.GetX()[0],h2.GetX()[h2.GetN()-1])

        for iBin in range(0, h1.GetN()):
            y1=h1.GetErrorYhigh(iBin)
            ey1=y1*Ratio(h1stat.GetErrorYhigh(iBin),h1stat.GetY()[iBin])  ##y1 * staterr in percent /100
            th1d_1.SetBinContent(iBin+1,y1)
            th1d_1.SetBinError(iBin+1,ey1)

            y2=h2.GetErrorYhigh(iBin)
            ey2=y2*Ratio(h2stat.GetErrorYhigh(iBin),h2stat.GetY()[iBin])  ##y1 * staterr in percent /100
            th1d_2.SetBinContent(iBin+1,y2)
            th1d_2.SetBinError(iBin+1,ey2)


    else:
        th1d_1=ROOT.TH1D('1','1',2*h1.GetN()+1,h1.GetX()[0],2*h1.GetX()[h1.GetN()-1])
        th1d_2=ROOT.TH1D('2','2',2*h2.GetN()+1,h2.GetX()[0],2*h2.GetX()[h2.GetN()-1])
        for iBin in range(0, h1.GetN()):
            y1_high=h1.GetErrorYhigh(iBin)
            y1_low=h1.GetErrorYlow(iBin)
            ey1_high=y1_high*Ratio(h1stat.GetErrorYhigh(iBin),h1stat.GetY()[iBin])  ##y1 * staterr in percent /100
            ey1_low=y1_low*Ratio(h1stat.GetErrorYlow(iBin),h1stat.GetY()[iBin])  ##y1 * staterr in percent /100

            th1d_1.SetBinContent(2*iBin+1,y1_high)
            th1d_1.SetBinError(2*iBin+1,ey1_high)
            th1d_1.SetBinContent(2*iBin+2,y1_low)
            th1d_1.SetBinError(2*iBin+2,ey1_low)

            

            y2_high=h2.GetErrorYhigh(iBin)
            y2_low=h2.GetErrorYlow(iBin)
            ey2_high=y2_high*Ratio(h2stat.GetErrorYhigh(iBin),h2stat.GetY()[iBin])  ##y2 * staterr in percent /200
            ey2_low=y2_low*Ratio(h2stat.GetErrorYlow(iBin),h2stat.GetY()[iBin])  ##y2 * staterr in percent /100

            th1d_2.SetBinContent(2*iBin+1,y2_high)
            th1d_2.SetBinError(2*iBin+1,ey2_high)
            th1d_2.SetBinContent(2*iBin+2,y2_low)
            th1d_2.SetBinError(2*iBin+2,ey2_low)
            
            #print "y1_high=",y1_high," y2_high=",y2_high
            #print "ey1_high=",ey1_high," ey_high=",ey2_high

    run_stat_test=getattr(th1d_1,test_stat)
    pvalue=run_stat_test(th1d_2,'WW P')
    print "p-value="+str(pvalue)
    return pvalue

def GetStatErrToSysErrGraph(hsys,hstat):


    nbin=hsys.GetN()
    herr=ROOT.TGraphAsymmErrors(nbin)

    for iBin in range(0,nbin):
        x=hsys.GetX()[iBin]
        ex_up=hsys.GetErrorXhigh(iBin)
        ex_dn=hsys.GetErrorXlow(iBin)

        y=hsys.GetY()[iBin]
        ey_up=hsys.GetErrorYhigh(iBin) ##
        ey_dn=hsys.GetErrorYlow(iBin)

        ystat=hstat.GetY()[iBin]
        eystat=hstat.GetErrorYhigh(iBin)
        err_in_ratio=Ratio(eystat,ystat) ## stat err in ratio
        #print "err_in_ratio=",err_in_ratio
        #print 'y=',y
        herr.SetPoint(iBin, x, y)
        herr.SetPointError(iBin, ex_dn,ex_up, ey_dn*err_in_ratio, ey_up*err_in_ratio   )
        
        
    return herr





def CompareTGraphAsymmErrorsWithStat(xaxis,yaxis,yaxis_ratio,title,h1,h1stat,label1,color1,h2,h2stat,label2,color2,store_file_path,test_stat,pvalue_threshold,do_norm=True):



    ##---Stat Test of central value---##
    print "##---Stat Test of central value---##"
    pass_stat_central=False
    pvalue=StatTestCentralValueTGraphAsymmErrors(test_stat,h1stat,h2stat)
    if pvalue > pvalue_threshold:
        pass_stat_central=True


    ##---Stat Test of sys errors ---##
    print "##---Stat Test of sys errors ---##"
    pass_stat_syserr=False
    pvalue_syserr=StatTestErrorValueTGraphAsymmErrors(test_stat,h1,h1stat,h2,h2stat)
    if pvalue_syserr > pvalue_threshold:
        pass_stat_syserr=True



    nbin=h1.GetN()

    prefix='jhchoi'
    print prefix
    print '[xaxis]',xaxis,' [title]',title,' label1',label1,' label2',label2

    #def ScaleTGraphAsymmErrors(h,scale):
    #def ErrorCombineSqrtSumTGraphAsymmErrors(h1,h2):
    #def GetRatioTGraphAsymmErrors(h1,h2):
    y1sum=sum(h1.GetY())
    y2sum=sum(h2.GetY())


    if do_norm:
        norm1=y1sum/y2sum
        #norm2=y2sum/y1sum
        norm2=1
    else:
        norm1=1
        norm2=1
    print 'norm1=',norm1
    print 'norm2=',norm2

    if do_norm:
        ScaleTGraphAsymmErrors(h1,1/norm1)
        ScaleTGraphAsymmErrors(h2,1/norm2)
        ScaleTGraphAsymmErrors(h1stat,1/norm1)
        ScaleTGraphAsymmErrors(h2stat,1/norm2)
        
    h1__total=ErrorCombineSqrtSumTGraphAsymmErrors(h1,h1stat)
    h2__total=ErrorCombineSqrtSumTGraphAsymmErrors(h2,h2stat)


    tgr_h1_over_h1=GetRatioTGraphAsymmErrors(h1,h1)
    tgr_h1_over_h2=GetRatioTGraphAsymmErrors(h1,h2)
    tgr_h2_over_h2=GetRatioTGraphAsymmErrors(h2,h2)


    tgr_h1stat_over_h1stat=GetRatioTGraphAsymmErrors(h1stat,h2stat)
    tgr_h1stat_over_h2stat=GetRatioTGraphAsymmErrors(h1stat,h2stat)
    tgr_h2stat_over_h2stat=GetRatioTGraphAsymmErrors(h2stat,h2stat)

    tgr_h1_over_h2__total=GetRatioTGraphAsymmErrors(h1__total,h2__total)
    tgr_h2_over_h2__total=GetRatioTGraphAsymmErrors(h2__total,h2__total)
    
    ##compare percentage err##
    #print "tgr_h1_over_h1.GetErrorXhigh(1)=",tgr_h1_over_h1.GetErrorXhigh(1)
    #print "tgr_h1_over_h2.GetErrorXhigh(0)=",tgr_h1_over_h2.GetErrorXhigh(0)
    #print "tgr_h2_over_h2.GetErrorXhigh(0)=",tgr_h2_over_h2.GetErrorXhigh(0)
    tgr_syserr1=GetYZeroTGraphAsymmErrors(tgr_h1_over_h1)
    ScaleTGraphAsymmErrors(tgr_syserr1,100)

    tgr_syserr_staterr1=GetStatErrToSysErrGraph(tgr_syserr1,h1stat)

    #print 'tgr_syserr1.GetErrorXhigh(0)=',tgr_syserr1.GetErrorXhigh(0)

    tgr_syserr2=GetYZeroTGraphAsymmErrors(tgr_h2_over_h2)
    ScaleTGraphAsymmErrors(tgr_syserr2,100)
    tgr_syserr_staterr2=GetStatErrToSysErrGraph(tgr_syserr2,h2stat)
    

    ymax  =max(h1.GetY())
    ymin  =max(h1.GetY())

    syserrmax=0


    for iBin in range(0,nbin):



        if tgr_syserr1.GetErrorYhigh(iBin)>syserrmax :
            syserrmax=tgr_syserr1.GetErrorYhigh(iBin)
        if tgr_syserr2.GetErrorYhigh(iBin)>syserrmax :
            syserrmax=tgr_syserr2.GetErrorYhigh(iBin)
        if tgr_syserr1.GetErrorYlow(iBin)>syserrmax :
            syserrmax=tgr_syserr1.GetErrorYlow(iBin)
        if tgr_syserr2.GetErrorYlow(iBin)>syserrmax :
            syserrmax=tgr_syserr2.GetErrorYlow(iBin)




        #print "[tgr_syserr1.GetErrorXhigh(iBin)]=",tgr_syserr1.GetErrorXhigh(iBin)

        y1=h1.GetY()[iBin]
        y2=h2.GetY()[iBin]
        #print 'y1=',y1
        #print 'y2=',y2
        if y1 > ymax : ymax=y1
        if y2 > ymax : ymax=y2
        if y1 < ymin and y1!=0 : ymin=y1
        if y2 < ymin and y2!=0 : ymin=y2

    print "syserrmax=",syserrmax
    print "ymin=",ymin
    #--Set Color--#
    SetStyleStat(h1stat,color1,h2stat,color2)
    SetStyleStat(tgr_h1stat_over_h2stat,color1,tgr_h2stat_over_h2stat,color2)
    SetStyleStat(tgr_syserr_staterr1,color1,tgr_syserr_staterr2,color2)
    

    print 'tgr_syserr1.GetErrorYlow(0)=',tgr_syserr1.GetErrorYlow(0)
    print 'tgr_syserr_staterr1.GetErrorYlow(0)=',tgr_syserr_staterr1.GetErrorYlow(0)
    print 'tgr_syserr2.GetErrorYlow(0)=',tgr_syserr2.GetErrorYlow(0)
    print 'tgr_syserr_staterr2.GetErrorYlow(0)=',tgr_syserr_staterr2.GetErrorYlow(0)

    SetStyleSys(h1,color1,h2,color2)
    SetStyleSys(tgr_h1_over_h2,color1,tgr_h2_over_h2,color2)
    SetStyleSys(tgr_syserr1,color1,tgr_syserr2,color2)


    SetStyleTotal(h1__total,color1,h2__total,color2)
    SetStyleTotal(tgr_h1_over_h2__total,color1,tgr_h2_over_h2__total,color2)


    ##--Legend
    tlegend = ROOT.TLegend(0.12, 0.65, 0.88, 0.88)#x1,y1,x2,y2 
    tlegend.SetFillColor(0)
    tlegend.SetTextFont(42)
    tlegend.SetTextSize(0.035)
    tlegend.SetLineColor(0)
    #tlegend.SetLineColor(stat_test_color)
    tlegend.SetShadowColor(0)



    

    canvas_name=prefix+'__'+label1+"_over_"+label2+'__'+xaxis+'__'+title
    tcanvas = ROOT.TCanvas(canvas_name,canvas_name,800,800)
    tcanvas.cd()
    #print 'tcanvas.GetX1()',tcanvas.GetX1()
    #print 'tcanvas.GetX2()',tcanvas.GetX2()
    #print 'tcanvas.GetY1()',tcanvas.GetY1()
    #print 'tcanvas.GetY2()',tcanvas.GetY2()
    #tbox=ROOT.TBox(tcanvas.GetX1(),tcanvas.GetY1(),tcanvas.GetX2(),tcanvas.GetY2())
    tbox_red=ROOT.TLegend(0.01,0.01,0.99,0.99) #TBox (Double_t x1, Double_t y1, Double_t x2, Double_t y2)
    tbox_red.SetLineWidth(3)
    tbox_red.SetLineColor(ROOT.kRed)
    tbox_red.SetFillStyle(0)                                                                                                         


    tbox_blue=ROOT.TLegend(0.01,0.01,0.99,0.99) #TBox (Double_t x1, Double_t y1, Double_t x2, Double_t y2)
    tbox_blue.SetLineWidth(3)
    tbox_blue.SetLineColor(ROOT.kBlue)
    tbox_blue.SetFillStyle(0)



    
    pad1 = ROOT.TPad('pad1_'+canvas_name,'pad1_'+canvas_name, 0, 1-0.72,1,1)
    pad1.SetTopMargin(0.098)
    pad1.SetBottomMargin(0.04)
    pad1.Draw()
    pad1.cd()
    
    
    
    pad1_tmr=ROOT.TMultiGraph()
    #pad1_tmr.Add(h1,'2')
    #pad1_tmr.Add(h2,'2')
    #pad1_tmr.Add(h1__total,'2')
    #pad1_tmr.Add(h2__total,'2')
    pad1_tmr.Add(h1stat,'p')
    pad1_tmr.Add(h2stat,'p')
    pad1_tmr.SetTitle(title)

    pad1_tmr.Draw('A2')
    pad1_tmr.GetYaxis().SetTitle(yaxis)
    #pad1_tmr.GetYaxis().SetTitleOffset( .4)
    
    #pad1.SetLogy()
    #tcanvas.SaveAs('1log_1.pdf')

    tlegend.AddEntry(h1__total,label1,'L')
    #tlegend.AddEntry(h1__total,'Sys.+Stat.','F')  
    #tlegend.AddEntry(h1,'Sys.Err.','F')
    tlegend.AddEntry(h1stat, ' Stat.Err.','LE')

    tlegend.AddEntry(h2__total,label2,'L')
    #tlegend.AddEntry(h2__total,'Sys.+Stat.','F')
    #tlegend.AddEntry(h2,'Sys.Err.','F')
    tlegend.AddEntry(h2stat, ' Stat.Err.','LE')
    
    tlegend.AddEntry(test_stat,test_stat,'')
    #'%.2E' % Decimal(pvalue)

    #tlegend.AddEntry('p-value','p-value='+str(round(pvalue,2)),'')
    tlegend.AddEntry('p-value','p-value='+str('%.2E' % Decimal(pvalue)),'')
    tlegend.SetNColumns(2)
    tlegend.Draw()

    tcanvas.cd()



    pad2 = ROOT.TPad('pad2_'+canvas_name,'pad2_'+canvas_name,0,0,1, 1-0.72)
    pad2.SetTopMargin(0.000)
    pad2.SetBottomMargin(0.39)
    pad2.Draw()
    pad2.cd()

    pad2_tmr=ROOT.TMultiGraph()
    #pad2_tmr.Add(tgr_h1_over_h2,'2')
    #pad2_tmr.Add(tgr_h2_over_h2,'2')
    #pad2_tmr.Add(tgr_h1_over_h2__total,'2')
    #pad2_tmr.Add(tgr_h2_over_h2__total,'2')
    pad2_tmr.Add(tgr_h1stat_over_h2stat,'p')
    pad2_tmr.Add(tgr_h2stat_over_h2stat,'p')
    pad2_tmr.Draw('a2')
    

    pad2_tmr.SetMaximum(1.5)
    pad2_tmr.SetMinimum(0.5)
    
    pad2_tmr.GetYaxis().SetTitle(yaxis_ratio)

    pad2_tmr.GetYaxis().SetLabelFont ( 42)
    pad2_tmr.GetYaxis().SetLabelOffset( 0.01)
    pad2_tmr.GetYaxis().SetLabelSize ( 0.1)
    pad2_tmr.GetYaxis().SetNdivisions ( 505)
    pad2_tmr.GetYaxis().SetTitleFont ( 42)
    pad2_tmr.GetYaxis().SetTitleOffset( .4)
    pad2_tmr.GetYaxis().SetTitleSize ( 0.1)

    pad2_tmr.GetXaxis().SetLabelFont ( 42)
    pad2_tmr.GetXaxis().SetLabelOffset( 0.01)
    pad2_tmr.GetXaxis().SetLabelSize ( 0.1)
    pad2_tmr.GetXaxis().SetNdivisions ( 505)
    pad2_tmr.GetXaxis().SetTitleFont ( 42)
    pad2_tmr.GetXaxis().SetTitleOffset( 1.)
    pad2_tmr.GetXaxis().SetTitleSize ( 0.1)

    pad2_tmr.GetXaxis().SetTitle(xaxis)


    pad1_tmr.SetMaximum(ymax*2)
    tcanvas.cd()
    if pass_stat_central:
        tbox_blue.Draw()
    else:
        tbox_red.Draw()
        
    tcanvas.Update()
    statdir='/'.join(store_file_path.split('/')[:-1])+'/'+test_stat+'/'
    statfile=store_file_path.split('/')[-1]
    os.system('mkdir -p '+statdir)
    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'.pdf')
    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'.png')
    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'.root')

    #tcanvas.SaveAs(store_file_path+'__'+test_stat+'.png')
    #tcanvas.SaveAs(store_file_path+'__'+test_stat+'.root')

    
    pad1_tmr.SetMaximum(ymax*1000)
    pad1_tmr.SetMinimum(ymin*0.1)
    pad1.SetLogy()



    tcanvas.cd()



    tcanvas.Update()



    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'_log.pdf')
    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'_log.png')
    tcanvas.SaveAs(statdir+statfile+'__'+test_stat+'_log.root')

    #tcanvas.SaveAs(store_file_path+'__'+test_stat+'_log.pdf')
    #tcanvas.SaveAs(store_file_path+'__'+test_stat+'_log.png')
    #tcanvas.SaveAs(store_file_path+'__'+test_stat+'_log.root')

    ##--add sys. total err
    tlegend.Clear()

    tlegend.AddEntry(h1__total,label1,'L')
    tlegend.AddEntry(h1__total,'Sys.+Stat.','F')
    tlegend.AddEntry(h1,'Sys.Err.','F')
    tlegend.AddEntry(h1stat, ' Stat.Err.','LE')

    tlegend.AddEntry(h2__total,label2,'L')
    tlegend.AddEntry(h2__total,'Sys.+Stat.','F')
    tlegend.AddEntry(h2,'Sys.Err.','F')
    tlegend.AddEntry(h2stat, ' Stat.Err.','LE')
    tlegend.SetNColumns(4)
    

    pad1_tmr.SetMaximum(ymax*2)
    pad1_tmr.SetMinimum(0)
    pad1.SetLogy(0)


    pad1_tmr.Add(h1,'2')
    pad1_tmr.Add(h2,'2')
    pad1_tmr.Add(h1__total,'2')
    pad1_tmr.Add(h2__total,'2')

    pad2_tmr.Add(tgr_h1_over_h2,'2')
    pad2_tmr.Add(tgr_h2_over_h2,'2')
    pad2_tmr.Add(tgr_h1_over_h2__total,'2')
    pad2_tmr.Add(tgr_h2_over_h2__total,'2')

    if pass_stat_central:
        tbox_blue.SetLineStyle(0)
        tbox_blue.SetLineColor(-1)
        tbox_blue.SetLineWidth(0)
    else:
        tbox_red.SetLineColor(-1)
        tbox_red.SetLineStyle(0)
        tbox_red.SetLineWidth(0)
    tcanvas.Update()
    tcanvas.SaveAs(store_file_path+'.pdf')
    tcanvas.SaveAs(store_file_path+'.png')
    tcanvas.SaveAs(store_file_path+'.root')

    pad1_tmr.SetMaximum(ymax*1000)
    pad1_tmr.SetMinimum(ymin*0.1)
    pad1.SetLogy(1)

    tcanvas.SaveAs(store_file_path+'_log.pdf')
    tcanvas.SaveAs(store_file_path+'_log.png')
    tcanvas.SaveAs(store_file_path+'_log.root')




    ##---Error Comparison--##
    canvas_name2=prefix+'__'+label1+"_over_"+label2+'__'+xaxis+'__'+title+'__percent_error'
    tcanvas2 = ROOT.TCanvas('pad1_'+canvas_name,'pad1_'+canvas_name,800,600)
    tcanvas2.cd()
    tlegend2 = ROOT.TLegend(0.50, 0.65, 0.88, 0.88)#x1,y1,x2,y2
    tlegend2.SetFillColor(0)
    tlegend2.SetTextFont(42)
    tlegend2.SetTextSize(0.035)
    tlegend2.SetLineColor(0)
    tlegend2.SetShadowColor(0)

    tlegend2.AddEntry(tgr_syserr1,label1,'F')
    tlegend2.AddEntry(tgr_syserr_staterr1, ' Stat.Err. of Sys.Err','LE')
    tlegend2.AddEntry(tgr_syserr2,label2,'F')
    tlegend2.AddEntry(tgr_syserr_staterr2, ' Stat.Err. of Sys.Err','LE')
    #tlegend2.AddEntry('p-value','p-value='+str(round(pvalue_syserr,2)),'')
    tlegend2.AddEntry(test_stat,test_stat,'')
    tlegend2.AddEntry('p-value','p-value='+str('%.2E' % Decimal(pvalue_syserr)),'')

    sys_tmr=ROOT.TMultiGraph()
    sys_tmr.Add(tgr_syserr1,'2')
    sys_tmr.Add(tgr_syserr2,'2')
    #print 'tgr_syserr_staterr2.GetErrorYhigh(0)=',tgr_syserr_staterr2.GetErrorYhigh(0)
    sys_tmr.Add(tgr_syserr_staterr1,'p')
    sys_tmr.Add(tgr_syserr_staterr2,'p')
    sys_tmr.SetTitle(title)

    sys_tmr.Draw('A2')
    #tgr_syserr_staterr2.Draw('same')
    sys_tmr.GetYaxis().SetTitle('Sys. Err. (%)')
    sys_tmr.GetXaxis().SetTitle(xaxis)
    sys_tmr.SetMaximum(syserrmax*2.1)
    #sys_tmr.SetMaximum(1)
    sys_tmr.SetMinimum(-syserrmax*1.1)
    #sys_tmr.SetMinimum(-1)
    tlegend2.SetNColumns(2)
    tlegend2.Draw()
    if pass_stat_syserr:
        tbox_blue.SetLineStyle(1)
        tbox_blue.SetLineColor(ROOT.kBlue)
        tbox_blue.SetLineWidth(3)
        tbox_blue.Draw()
    else:
        tbox_red.SetLineStyle(1)
        tbox_red.SetLineColor(ROOT.kRed)
        tbox_red.SetLineWidth(3)
        tbox_red.Draw()

    tcanvas2.SaveAs(statdir+statfile+'_sys_percent__'+test_stat+'.pdf')
    tcanvas2.SaveAs(statdir+statfile+'_sys_percent__'+test_stat+'.png')
    tcanvas2.SaveAs(statdir+statfile+'_sys_percent__'+test_stat+'.root')

    #tcanvas2.SaveAs(store_file_path+'_sys_percent__'+test_stat+'.pdf')
    #tcanvas2.SaveAs(store_file_path+'_sys_percent__'+test_stat+'.png')
    #tcanvas2.SaveAs(store_file_path+'_sys_percent__'+test_stat+'.root')


    del tcanvas
    del tcanvas2

    del pad1
    del pad2

    del pad1_tmr
    del pad2_tmr
    del sys_tmr

    del tlegend
    del tlegend2


    del h1stat
    del h2stat
    del h1__total
    del h2__total
    del h1
    del h2

    del tgr_h1_over_h2
    del tgr_h1stat_over_h2stat
    del tgr_h1_over_h2__total


    del tgr_h2_over_h2
    del tgr_h2stat_over_h2stat
    del tgr_h2_over_h2__total


    

if __name__ == "__main__":
    ##-for test-
    CMSSW_BASE=os.getenv('CMSSW_BASE')
    ROOT.gROOT.LoadMacro(CMSSW_BASE+'/src/Gen_validation/CMSSW_tools/scripts/modules/GetHisto.C+')
    h2path='/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg260_master_dyellell01234j_5f_LO_MLM__5000evt/combined_histo/'
    h1path='/cms/ldap_home/jhchoi/gridvalidation/mg265_validation/event_gen/workdir/JOBDIR_HistoFactory__GENEVT_mg265_dyellell01234j_5f_LO_MLM__5000evt/combined_histo/'

    '''
    h1=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__306000__dimuon_mass.root',"Graph")
    h2=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__306000__dimuon_mass.root',"Graph")
    h1stat=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__306000__dimuon_mass__statonly.root',"Graph")
    h2stat=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__306000__dimuon_mass__statonly.root',"Graph")

    #histopath,"DYValidation/"+x+'_'+str(idx)
    CompareTGraphAsymmErrorsWithStat("dimuon_mass",'LHAPDF306000', h1, h1stat,"MG5 v260",ROOT.kRed,h2,h2stat,"MG5 v261",ROOT.kBlue,False)

    '''
    #h1=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__306000__dimuon_mass.root',"Graph")
    #h2=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__306000__dimuon_mass.root',"Graph")
    #h1stat=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__306000__dimuon_mass__statonly.root',"Graph")
    #h2stat=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__306000__dimuon_mass__statonly.root',"Graph")
    


    #h1=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__muRmuF_default__dimuon_mass.root',"Graph")    
    #h2=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__muRmuF_default__dimuon_mass.root',"Graph")
    #h1stat=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__muRmuF_default__dimuon_mass__statonly.root',"Graph")
    #h2stat=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__muRmuF_default__dimuon_mass__statonly.root',"Graph")


    h1=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__muRmuF_default__dimuon_mass.root',"Graph")
    h2=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__muRmuF_default__dimuon_mass.root',"Graph")
    h1stat=ROOT.GetTGraphAsymmErrors(h1path+'/combined_histo__muRmuF_default__dimuon_mass__statonly.root',"Graph")
    h2stat=ROOT.GetTGraphAsymmErrors(h2path+'/combined_histo__muRmuF_default__dimuon_mass__statonly.root',"Graph")


    #(xaxis,yaxis,yaxis_ratio,title,h1,h1stat,label1,color1,h2,h2stat,label2,color2,store_file_path,test_stat,pvalue_threshold,do_norm=True)
    CompareTGraphAsymmErrorsWithStat("dimuon_mass",'norm. nevents','mg265/mg260','muRmuF_default', h1, h1stat,"MG5 v265",ROOT.kRed,h2,h2stat,"MG5 v260",ROOT.kBlue,'./result.pdf','Chi2Test',0.00001,True)
    #CompareTGraphAsymmErrorsWithStat("dimuon_mass",'norm. nevents','mg261/mg260','muRmuF_default', h1, h1stat,"MG5 v261",ROOT.kRed,h1,h1stat,"MG5 v260",ROOT.kBlue,'./result.pdf','Chi2Test',0.00001,True)

    #canvas_name='test'
    #tcanvas = ROOT.TCanvas(canvas_name,canvas_name,800,800)

    #h1stat.GetHistogram().Draw()
    #th1d_1=TGraphAsymmErrorsToTH1D(h1stat)
    #th1d_1.Draw()
    #tcanvas.SaveAs('test.pdf')
'''
kWhite  = 0,   kBlack  = 1,   kGray    = 920,  kRed    = 632,  kGreen  = 416,
kBlue   = 600, kYellow = 400, kMagenta = 616,  kCyan   = 432,  kOrange = 800,
kSpring = 820, kTeal   = 840, kAzure   =  860, kViolet = 880,  kPink   = 900
'''
