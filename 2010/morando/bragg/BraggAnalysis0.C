
{
    
   TControlBar *bar = new TControlBar("vertical", "BraggAnalysis");
   gROOT->LoadMacro("Dialogs.C");
   bar->AddButton("Visualizza 50 eventi",".x Bragg0.C", "Click Here For Help on Running the Demos");
   bar->AddButton("Macro per creare il rootfile",".x Bragg1new.C", "Crea il root file");  
  
   bar->AddButton("seleziona un intervallo di energie",".x Bragg1_3.C", "seleziona energia");

    
   bar->AddButton("browser",     "{TBrowser *b = new TBrowser();}", "Start the ROOT Browser");
   bar->AddButton("apri un root file",".x Bragg1_2.C", "apri un root file");
   bar->AddButton("Update di un root file con altri dati",".x Bragg1_1.C", "esegue l'update del root file");
   bar->AddButton("esci",     ".q", "Quit"); 
   bar->Show();
   gROOT->SaveContext();
}


