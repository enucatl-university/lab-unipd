TINC=/usr/include/root 
TLIB=/usr/lib/root
TLIBLIST=-lASImage -lAfterImage -lCore -lEG -lGX11 -lGX11TTF -lGeom -lGpad -lGraf -lGraf3d -lGui -lHist -lHistPainter -lHtml -lMLP -lMatrix -lMinuit -lNew -lPhysics -lPostscript -lProof -lRint -lTree -lTreePlayer -lTreeViewer -lVMC -lX3d -lfreetype -lASImageGui -lGX11TTF -lTreePlayer -lASImage -lPyROOT -lTree -lTreeViewer -lQuadp -lvalarrayDict -lReflexDict -lvectorDict -ldequeDict -llistDict -lReflex -lVMC -lEG -lmap2Dict -lmapDict -lXMLIO -lMathCore -lRIO -lFitPanel  -lFoam -lMatrix -lFumili -lMinuit2 -lMinuit -lGed -lMLP -lRootAuth -lGeomBuilder -lmultimap2Dict -lSessionViewer -lGeomPainter -lmultimapDict -lsetDict -lGeom -lmultisetDict -lSmatrix -lGpad -lNet -lSpectrumPainter -lSpectrum -lGraf3d -lNew -lSPlot -lGraf -lPhysics  -lGuiBld -lPostscript -lSrvAuth  -lGuiHtml   -lGui  -lGX11  -lTMVA

diffanalysis: diffanalysis.cpp
	g++ -g -o diffanalysis diffanalysis.cpp -I$(TINC) -L $(TLIB) $(TLIBLIST)

