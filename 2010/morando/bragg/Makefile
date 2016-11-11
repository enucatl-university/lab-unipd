TINC=/usr/include/root 
TLIB=/usr/lib/root
TLIBLIST=-lASImage -lAfterImage -lCint -lCore -lEG -lGX11 -lGX11TTF -lGeom -lGpad -lGraf -lGraf3d -lGui -lHist -lHistPainter -lHtml -lMLP -lMatrix -lMinuit -lNew -lPhysics -lPostscript -lProof -lRint -lTree -lTreePlayer -lTreeViewer -lVMC -lX3d -lfreetype -lASImageGui -lGX11TTF -lTreePlayer -lASImage -lPyROOT -lTree -lCintex -lTreeViewer -lQuadp -lvalarrayDict -lReflexDict -lvectorDict -ldequeDict -llistDict -lReflex -lVMC -lEG -lmap2Dict -lmapDict -lXMLIO -lMathCore -lRIO -lFitPanel -lXrdClient -lFoam -lMatrix -lFumili -lMinuit2 -lMinuit -lGed -lMLP -lRootAuth -lGeomBuilder -lmultimap2Dict -lSessionViewer -lGeomPainter -lmultimapDict -lsetDict -lGeom -lmultisetDict -lSmatrix -lGpad -lNet -lSpectrumPainter -lSpectrum -lGraf3d -lNew -lSPlot -lGraf -lPhysics -lXrdSec -lGuiBld -lPostscript -lSrvAuth -lXrdSecunix -lGuiHtml -lProofDraw -lXrdSut -lGui -lProofPlayer -lGX11 -lProof -lTMVA

all: bragg bragg400 medie larghezza

bragg: my_bragg.cpp compare.cpp
	g++ -o my_bragg my_bragg.cpp -I$(TINC) -L $(TLIB) $(TLIBLIST)

bragg400: my_bragg_400.cpp compare.cpp
	g++ -o my_bragg_400 my_bragg_400.cpp -I$(TINC) -L $(TLIB) $(TLIBLIST)

medie: medie.cpp
	g++ -o medie medie.cpp -I$(TINC) -L $(TLIB) $(TLIBLIST)

larghezza: larghezza.cpp compare.cpp
	g++ -o larghezza larghezza.cpp -I$(TINC) -L $(TLIB) $(TLIBLIST)
