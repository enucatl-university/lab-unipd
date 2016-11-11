#!/usr/bin/python
#coding=utf-8


from ROOT import TH1F, TCanvas, TF1, TGraph, TFile, TGraphErrors, TMath
from math import sqrt, log, pi, fabs

#COSTANTI
bins = 1024
def graph_style (graph, title):
    #graph.SetMarkerStyle(7)
    graph.SetTitle(title)
    graph.GetXaxis().SetTitle( 'E (keV)' )
    graph.GetYaxis().SetTitle( 'eventi' )
    graph.GetXaxis().SetTitleSize( 0.035 )
    graph.GetYaxis().SetTitleSize( 0.035 )
    graph.GetXaxis().SetLabelSize( 0.035 )
    graph.GetYaxis().SetLabelSize( 0.035 )
    graph.GetXaxis().SetDecimals( )
    graph.GetYaxis().SetDecimals( )          

class Spettro:
    def __init__(self, filename):
        self.filename = filename
        self.hist_filename = filename + ".dat"
        self.leggi_file()
        self.leggi_hist()

    def leggi_file(self):
        self.intervalli = []
        with  open(self.hist_filename, "w") as file_w:
            with open(self.filename) as file:
                flag = 0
                flag_roi = 0
                self.calib = 0
                self.ka, self.kb, self.la, self.lb = [-1 for _ in range(4)]
                i = 0
                for line in file:
                    if "<<END>>" in line:
                        break
                    if flag:
                        file_w.write(line)
                    if "REAL_TIME" in line:
                        self.time = float(line.split()[-1])
                    if "<<DATA>>" in line:
                        flag = 1
                        flag_roi = 0
                    if flag_roi:
                        inter = [int(x) for x in line.split()[0:2]]
                        self.intervalli.append(inter)
#                        print(inter)
                        if "ka" in line:
                            self.ka = i
                        if "kb" in line:
                            self.kb = i
                        if "la" in line:
                            self.la = i
                        if "lb" in line:
                            self.lb = i
                        i += 1
                    if "ROI" in line:
                        flag_roi = 1
                    if "200.17 13.95" in line:
                        self.calib = 1 #calibrazione giorno 1
                    elif "200.75 13.95" in line:
                        self.calib = 2 #calibrazione giorno 2
                        # se non trova nessuna di queste due righe è un file
                        # di calibrazione: resta calib = 0

    def leggi_hist(self):
        self.hist_name = self.filename.split(".")[0]
        self.hist = TH1F(self.hist_name, self.hist_name, bins, 0, bins)
        with open(self.hist_filename) as file:
            for i, line in enumerate(file):
                line = float(line)
                self.hist.SetBinContent(i + 1, line)

    def riscala_hist(self, time_scale):
        self.hist.Scale(time_scale / self.time)

    def riscala_integrali(self, time_scale):
        self.integrali = [i * time_scale / self.time for i in self.integrali]
        self.integrali_err = [i * time_scale / self.time for i in self.integrali_err]

    def analisi_picchi(self):
        self.centroidi, self.sigma, self.integrali = [[] for _ in range(3)]
        gau = TF1("gau", "[0] * exp(-(x - [1])**2 / (2 *[2]**2))", 0, bins)
        for estremi in self.intervalli:
            m = estremi[0]
            M = estremi[1]
            gau.SetParameters(self.hist.GetBinContent(int((m+M)/2)), (m+M)/2, (M-m)/3)
            self.hist.GetYaxis().SetTitle("Numero fotoni")
            self.hist.GetXaxis().SetTitle("Canale")
            self.hist.Fit("gau", "WRQN+", "", m, M)
            #self.hist.Write()         # questo cosa faceva?
            self.integrali.append(gau.GetParameter(0) * sqrt(2 * pi) * gau.GetParameter(2))
            self.centroidi.append(gau.GetParameter(1))
            self.sigma.append(gau.GetParameter(2))
        self.risoluzioni = [2 * sqrt(2 * log(2)) * s / N * 100 for s,N in zip(self.sigma, self.integrali)]
        self.integrali_err = [sqrt(fabs(n)) for n in self.integrali]
        self.centroidi_err = [x/y for x,y in zip(self.sigma, self.integrali_err)]
        self.intensita_rel = [x / max(self.integrali) for x in self.integrali]

    def calibrazione(self):
        if self.calib == 1:
            a = 0.0686703
            ea = 1.57738e-05
            b = 0.198718
            eb = 0.00840664
            ro = -0.825
        elif self.calib == 2:
            a = 0.0687142
            ea = 1.44101e-05
            b = 0.15057
            eb = 0.00768328
            ro = -0.826
        else:
            a = 1
            ea = 0
            b = 0
            eb = 0
        hist_en_name = self.hist_name + "_en"
        self.hist_en = TH1F(hist_en_name, hist_en_name, bins, b, a * bins + b) # istogramma in energia
        with open(self.hist_filename) as file:
            for i, line in enumerate(file):
                line = float(line)
                self.hist_en.SetBinContent(i + 1, line)
        canali = self.centroidi # temporaneo
        self.centroidi = [x * a + b for x in self.centroidi]
        self.centroidi_err = [sqrt(a**2 * ex**2 + x**2 * ea**2 + eb**2 + ro
            * x * ea * eb) for ex,x in
                zip(self.centroidi_err,canali)]

bins = 1024

### LEGGE ASSORBIMENTO ####
#spessori_al = ['00','02','04','06','08','10']
#file_al = ["dati/Al"+ x + ".mca" for x in spessori_al]
#spettri_al = [Spettro(x) for x in file_al]
#for al in spettri_al:
#    al.intervalli = [[194,206],[238,248],[250,261]] #ridefinisce intervalli dei picchi uguali per tutti gli spettri di Al
#    al.analisi_picchi()
#    al.calibrazione()
#    al.riscala_integrali(spettri_al[0].time)
#    print(al.centroidi, al.integrali)

#spettri_al[0].hist.Draw()

#with open("fit_spessore", "w") as file:
#    for l, al in zip(spessori_al, spettri_al):
#        file.write(l + " " + " ".join(str(log(v)) + " 0 " + str(err/v) for v,err in
#        zip(al.integrali,al.integrali_err)) + "\n")
pol1 = TF1("pol1", "[0] * x + [1]", 0, bins)  
pol1.SetLineWidth(1)
#mu, mu_err = [[] for _ in range(2)]
#can_al_fit = TCanvas("can_al_fit", "can_al_fit")
#can_al_fit.SetFillColor(10)
#gr_al_1 = TGraphErrors("fit_spessore", "%lg %lg %lg %lg")
#gr_al_1.GetYaxis().SetTitle("log I")
#gr_al_1.GetXaxis().SetTitle("Spessore (mm)")
#gr_al_1.SetTitle("Legge di assorbimento")
#gr_al_1.Draw("ap")
#gr_al_1.Fit("pol1", "")
#mu.append(pol1.GetParameter(0))
#mu_err.append(pol1.GetParameter(1))
#chi2 = pol1.GetChisquare()
#ndf = pol1.GetNDF()
#prob = TMath.Prob(chi2, ndf)
#print("Probabilità = " + str(prob))
#can_al_fit.SaveAs("gr_al_fit.eps")
#gr_al_2 = TGraphErrors("fit_spessore", "%lg %*lg %*lg %*lg %lg %lg %lg")
#gr_al_2.GetYaxis().SetTitle("log I")
#gr_al_2.GetXaxis().SetTitle("Spessore (mm)")
#gr_al_2.SetTitle("Legge di assorbimento")
#gr_al_2.Draw("p same")
#gr_al_2.Fit("pol1", "")
#mu.append(pol1.GetParameter(0))
#mu_err.append(pol1.GetParameter(1))
#gr_al_3 = TGraphErrors("fit_spessore", "%lg %*lg %*lg %*lg %*lg %*lg %*lg %lg %lg %lg")
#gr_al_3.GetYaxis().SetTitle("log I")
#gr_al_3.GetXaxis().SetTitle("Spessore (mm)")
#gr_al_3.SetTitle("Legge di assorbimento")
#gr_al_3.Draw("p same")
#gr_al_3.Fit("pol1", "")
#mu.append(pol1.GetParameter(0))
#mu_err.append(pol1.GetParameter(1))
#mu = [- 10 * m for m in mu] # cambio segno e conversione in cm
#mu_ro = [m / 2.699 for m in mu]
#print(spettri_al[0].centroidi, mu, mu_ro)

### CAMPIONI MONOELEMENTALI ###
righe = ["ka","kb","la","lb"]
elementi = ["cadmio", "ferro", "molibdeno", "nichel", "piombo", "rame", "tantalio"]
numero_atomico = [48,26,42,28,82,29,73]
file_elementi = ["dati/" + x + ".mca" for x in elementi]
spettri_elementi = [Spettro(x) for x in file_elementi]

for s in spettri_elementi:
    s.analisi_picchi()
    s.calibrazione()

graph_style(spettri_elementi[6].hist_en, "tantalio")
spettri_elementi[6].hist_en.Draw()

### TABELLA LATEX righe K e L degli elementi ###
righe_tex = ["$K_{\\alpha}$", "$K_{\\beta}$", "$L_{\\alpha}$", "$L_{\\beta}$"]
with open("tab_monoelementi.tex", "w") as file:
    file.write("\\begin{tabular}{r@{ $\\pm$ }lcr@{ $\\pm$ }ll}\n")
    file.write("\\multicolumn{2}{c}{\\unit[picco]{(keV)}} & \\unit[risoluzione]{(\\%)} & \\multicolumn{2}{c}{integrale} & riga \\\\ \n \\hline \n")
    for e,s,z in zip(elementi,spettri_elementi,numero_atomico):
        file.write("\\multicolumn{3}{l}{\\textbf{" + e + " ($Z$=" + str(z) +
                ")}} & \\multicolumn{3}{l}{tempo = " + str(s.time) +"}\\\\ \n")
        for riga,b in zip(righe_tex, [s.ka,s.kb,s.la,s.lb]):
            if b != -1:
                    line = "%.2f \t&\t %.2f \t&\t %.1f \t&\t %.0f \t&\t %.0f \t & \t"%(s.centroidi[b], s.centroidi_err[b], s.risoluzioni[b], s.integrali[b], s.integrali_err[b])
                    line = line + riga + " \\\\ \n"
                    file.write(line)
    file.write("\\end{tabular}")



### LEGGE MOOSELEY ###
for a,b in zip(["ka","kb","la","lb"],[s.ka,s.kb,s.la,s.lb]):
    with open("fit_elementi_" + a, "a") as file:
        if b != -1:
            file.write(str((numero_atomico[b]-1)**2) + " " + str(s.centroidi[b]) + " 0 " + str(s.centroidi_err[b]) + "\n")
    for c,ec,i,r in zip(s.centroidi,s.centroidi_err,s.intensita_rel,s.risoluzioni):
        print("%.3f\t%.3f\t%.3f\t%.2f"%(c,ec,i,r))
gr_elementi = [TGraphErrors("fit_elementi_" + a) for a in ["la","kb","lb","ka"]]


### TABELLA LATEX legge mooseley ###
with open("tab_mooseley.tex", "w") as file:
    file.write("\\begin{tabular}{r@{ = }r@{ $\\pm$ }l}\n")
    for i,gr,riga in zip(range(4), gr_elementi, righe_tex):
        if i is 0:
            gr.Draw("ap")
        else:
            gr.Draw("p same")
        gr.Fit("pol1", "")
        file.write("\\hline \n")
        file.write("\\multicolumn{3}{l}{\\textbf{"+ riga +"} \\\\ \n")
        line1 = "c \t&\t %.2f \t&\t \\unit[ %.2f]{keV} \\\\ \n"%(pol1.GetParameter(1), pol1.GetParError(1))
        line2 = "d \t&\t %.4f \t&\t \\unit[ %.4f]{keV} \\\\ \n"%(pol1.GetParameter(0), pol1.GetParError(0))
        file.write(line1 + line2)
    file.write("\\end{tabular}")

### SPETTRO AMERICIO ###
am = Spettro("dati/calibrAm_1.mca")
am.analisi_picchi()
am.calibrazione()
graph_style(am.hist_en, "^{241}Am")
can_am = TCanvas("am", "am")
can_am.SetFillColor(10)
am.hist_en.Draw()
can_am.SaveAs("fig_Am.eps")





#ipotesi_picchi = ["?", "Raggi X $L_{\alpha_1}$ Lp", "?", "Raggi X $L_{\beta_2}$ Lp", "Raggi X $L_{\beta_1}$ Lp", "Raggi X $L_{\gamma_1}$ Lp", "Transizione E1 nel Np", "Transizione E1 nel Np"]
#ipotesi_picchi = ["Cloro" ,"Ar", "Ca", "Mn", "Fe" "tutti spostati di +5kev", "Raggi X $L_{\gamma_1}$ Lp", "As", "Transizione E1 nel Np"]
#with open("tab_fondoAl.tex", "w") as file:
#    file.write("\\begin{tabular}{r@{ $\\pm$ }lcr@{ $\\pm$ }lc}\n")
#    file.write("\\multicolumn{2}{c}{\\unit[picco]{(keV)}} & \\unit[risoluzione]{(\\%)} & \\multicolumn{2}{c}{$I$} & Origine picco \\\\ \n \\hline \n")
#    for p, p_e, ris, i, i_e, ip in zip(am.centroidi, am.centroidi_err, am.risoluzioni, am.integrali, am.integrali_err, ipotesi_picchi):
#        line = "%.2f \t&\t %.2f \t&\t %.1f \t&\t %.0f \t&\t %.0f \t&\t"%(p, p_e, ris, i, i_e)
#        line = line + ip + "\\\\ \n"
#        file.write(line)
#    file.write("\\end{tabular}")
### PARTICOLATO ATMOSFERICO ###
#can_filtro = TCanvas("can_filtro", "can_filtro")
#can_filtro.SetFillColor(10)
#fp = Spettro("dati/filtro_pulito.mca")
#fs = Spettro("dati/filtro_sporco.mca")
#fs.hist.Add(fp.hist, -1)
#fs.analisi_picchi()
#fs.hist.Draw()
#fp.hist.SetLineStyle(3)
#fp.hist.Draw("same")
#can_2 = TCanvas("can_2", "can_2")
#can_2.SetFillColor(10)
#fs.riscala_hist(fp.time)
#fs.calibrazione()
#print(fs.centroidi)
#fs.hist_en.Draw()

#input()
