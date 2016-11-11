#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1F, TCanvas, TF1, TGraph, TFile, TGraphErrors, TMath
from math import sqrt, log, pi, fabs
from Spettro import *

# Costanti
bins = 1024

data_folder = "spettri/"

pol1 = TF1("pol1", "[0] * x + [1]")  
pol1.SetLineWidth(1)          


# Fit calibrazione

#gr_calib1 = TGraph(data_folder+"calib_1")
#gr_calib1.Fit("pol1")
#gr_calib2 = TGraph(data_folder+"calib_2")
#gr_calib2.Fit("pol1")


#### LEGGE ASSORBIMENTO ####
spessori_al = ['00','02','04','06','08','10']
file_al = [data_folder + "am_spessore" + str(x) + ".mca" for x in range (6)]
spettri_al = [Spettro(x) for x in file_al]

for al in spettri_al:
    al.intervalli = [[194,206],[250,261]] #ridefinisce intervalli dei picchi uguali per tutti gli spettri di Al
    al.analisi_picchi()
    al.calibrazione()
    al.riscala_integrali(spettri_al[0].time)    
    al.disegna_spettro()

# Controllo compatibilità centroidi
pol0 = TF1("pol0", "[0]", 0, 10)
pol0.SetLineWidth(1)
##   picco 13
#media_c = [0,0]
#with open("al_compatibilita","w") as file:
#    for i,s in enumerate(spettri_al):
#        media_c = [m + c for m,c in zip(media_c,s.centroidi)]
#        file.write(str(i) + " " + " ".join(str(c) + " 0 " +
#            str(ce) for c,ce in zip(s.centroidi,s.centroidi_err)) + "\n")
#media_c = [x / 6 for x in media_c]
#can_al_compatib = TCanvas("can_al_compatib", "can_al_compatib")
#can_al_compatib.SetFillColor(10)
#gr_al_compatib = TGraphErrors("al_compatibilita")
#pol0.SetParameter(0,media_c[0])
#gr_al_compatib.Draw("ap")
#pol0.Draw("same")
##   picco 17
#can_al_compatib1 = TCanvas("can_al_compatib1", "can_al_compatib1")
#can_al_compatib1.SetFillColor(10)
#gr_al_compatib1 = TGraphErrors("al_compatibilita", "%lg %*lg %*lg %*lg %lg %lg %lg")
#pol0.SetParameter(0,media_c[1])
#gr_al_compatib1.Draw("ap")
#pol0.Draw("same")


#with open("fit_spessore", "w") as file:
#    for l, al in zip(spessori_al, spettri_al):
#        file.write(l + " " + " ".join(str(log(abs(v))) + " 0 " + str(err/v) for v,err in zip(al.integrali,al.integrali_err)) + "\n")

#mu, mu_err = [[] for _ in range(2)]
#can_al_fit = TCanvas("can_al_fit", "can_al_fit")
#can_al_fit.SetFillColor(10)
#gr_al_1 = TGraphErrors("fit_spessore", "%lg %lg %lg %lg")
#gr_al_1.SetMarkerStyle(7)
#gr_al_1.SetMarkerSize(0.002)
#gr_al_1.GetYaxis().SetTitle("log I")
#gr_al_1.GetXaxis().SetTitle("Spessore (mm)")
#gr_al_1.SetTitle("Legge di assorbimento")
#gr_al_1.GetXaxis().SetRangeUser(-1,11)
#gr_al_1.Draw("ap")
#gr_al_1.Fit("pol1", "")
#mu.append(pol1.GetParameter(0))
#mu_err.append(pol1.GetParError(0))
#chi2 = pol1.GetChisquare()
#ndf = pol1.GetNDF()
#prob = TMath.Prob(chi2, ndf)
#print("Probabilità = " + str(prob))
#gr_al_2 = TGraphErrors("fit_spessore", "%lg %*lg %*lg %*lg %lg %lg %lg")
#gr_al_2.SetMarkerStyle(7)
#gr_al_2.SetMarkerSize(0.002)
#gr_al_2.GetYaxis().SetTitle("log I")
#gr_al_2.GetXaxis().SetTitle("Spessore (mm)")
#gr_al_2.SetTitle("Legge di assorbimento")
#gr_al_2.GetXaxis().SetRangeUser(-1,11)
#gr_al_2.Draw("p same")
#gr_al_2.Fit("pol1", "")
#mu.append(pol1.GetParameter(0))
#mu_err.append(pol1.GetParError(0))
#chi2 = pol1.GetChisquare()
#ndf = pol1.GetNDF()
#prob = TMath.Prob(chi2, ndf)
#print("Probabilità = " + str(prob))
#mu = [- 10 * m for m in mu] # cambio segno e conversione in cm^-1
#mu_ro = [m / 2.699 for m in mu] # divisione per densità alluminio
#mu_ro_err = [m / 2.699 for m in mu_err]
#print(spettri_al[0].centroidi, mu, mu_ro)
#can_al_fit.SaveAs("gr_al_fit.eps")
##with open("mu_ro","w") as file:                                       
##    for c,m,ce,me in zip(spettri_al[0].centroidi,mu_ro,spettri_al[0].centroidi_err,mu_ro_err):
##        file.write(str(c) + " " + str(m) + " " + str(ce) + " " + str(me) + "\n")
##can_mu = TCanvas("can_mu", "can_mu")
##gr_mu = TGraphErrors("mu_ro")
##gr_mu.Draw("ap")
##gr_mu.Fit("pol1")



### CAMPIONI MONOELEMENTALI ###
elementi = ["nichel", "rame", "ferro", "ittrio", "niobio", "indio", "cadmio", "tantalio", "piombo", "stagno", "tantalio2", "bismuto"]
numero_atomico = [28,	29,	 26,	  39,	    41,	      49,	48,	  73,	     82,	50,	   73,		81]
file_elementi = [data_folder + x + ".mca" for x in elementi]
spettri_elementi = [Spettro(x) for x in file_elementi]

for s in spettri_elementi:
		s.disegna_spettro()
#for a in ["ka","kb","la","lb"]:
#    open("fit_elementi_" + a, "w")
#for e,s,z in zip(elementi, spettri_elementi, numero_atomico):
#    s.analisi_picchi()
#    s.calibrazione()
#    for a,b in zip(["ka", "kb", "la", "lb"],[s.ka, s.kb, s.la, s.lb]):
#        with open("fit_elementi_" + a, "a") as file:
#            if b != -1:
#                file.write(str((z-1)**2) + " " + str(s.centroidi[b]) + " 0 " +
#                        str(s.centroidi_err[b]) + "\n")
##        for c,ec,i,r in zip(s.centroidi,s.centroidi_err,s.intensita_rel,s.risoluzioni):
##            print("%.3f\t%.3f\t%.3f\t%.2f"%(c,ec,i,r))
#can_elementi = []
#gr_elementi = [TGraphErrors("fit_elementi_" + a) for a in
#        ["ka","kb","la","lb"]]
#righe = ["K_{#alpha}","K_{#beta}","L_{#alpha}","L_{#beta}"]
#for i in range(4):
#    nome = "can_elementi_" + str(i)
#    can_elementi.append(TCanvas(nome,nome))
#    can_elementi[i].SetFillColor(10)
#    gr = gr_elementi[i]
#    gr.SetTitle(righe[i])
#    gr.GetXaxis().SetTitle("(Z - 1)^2")
#    gr.GetYaxis().SetTitle("E (keV)")
#    gr.Draw("ap")
#    gr.Fit("pol1", "")




### PARTICOLATO ATMOSFERICO ###
can_filtro = TCanvas("can_filtro", "can_filtro")
can_filtro.SetFillColor(10)
fp = Spettro(data_folder + "filtro_pulito.mca")
fs = Spettro(data_folder + "filtro_sporco.mca")
fsa = Spettro(data_folder + "filtro_sporco_degli_altri.mca")
fp.disegna_spettro()
fs.disegna_spettro()
fsa.disegna_spettro()
#fp.hist.SetLineStyle(3)
##fs.hist.Add(fp.hist, -1)
##fs.riscala_hist(fp.time)
#fs.analisi_picchi()
#fp.analisi_picchi()
#fp.calibrazione()
#fs.calibrazione()
#fp.hist_en.SetLineStyle(3)
#fs.hist_en.Draw()
##fp.hist_en.Draw("same")
##print(fs.centroidi)
##print(fp.centroidi)
#picchi_sporco = ["Kr?","Cl","Ar","Ca","Fe","Fe","Ni","Cu","Ga","Pb+As","Pb+Kr???"]
## disegna elementi sullo spettro del filtro sporco
#for n in [1,3,4,5]:
#    s = spettri_elementi[n]
#    s.riscala_hist_en(fs.time / 5)
#    s.hist_en.SetLineStyle(n + 1)
#    s.hist_en.Draw("same")



### RIVELATORE ###
#can_riv = TCanvas("can_riv", "can_riv")
#can_riv.SetFillColor(10)
#riv = Spettro("dati/rivelatoreSi.mca")
#riv.analisi_picchi()
#riv.calibrazione()
#riv.hist_en.Draw()
##print(riv.centroidi)
#picchi_riv = ["Si","Cl","Ti","V","Ni","Cu","Ga","Br","?","Pa?"]
## disegna elementi sullo spettro del rivelatore
#for n in [3,5]:
#    s = spettri_elementi[n]
#    s.riscala_hist_en(riv.time / 10)
#    s.hist_en.SetLineStyle(n)
#    s.hist_en.Draw("same")

raw_input()
