#ifndef READ_DATA
#define READ_DATA

#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include "TFile.h"
#include "TTree.h"

//reads data from ASCII file (formatted in two columns) and saves a ROOT Tree.
using namespace std;

TTree* readData( char*, char* );

void saveData( char*, char* );

TTree* readData( char* inputFile, char* outputFile) {
//  Read data from a 2 column ascii file and create a ROOT Tree
  ifstream ascii( inputFile, ios_base::in );
  strcat( outputFile, "_tree");
  TTree* t = new TTree( outputFile,"data from ascii file" );
  Long64_t nlines = t->ReadFile( inputFile, "x:y" );
  ascii.close();
  cout << "found " << nlines << " lines." << endl;
  return t;
}

void saveData( char* inputFile, char* outputFile) {
//  Read data from an ascii file and create a root file with an histogram and an ntuple.

  TTree* t = readData( inputFile, outputFile );
  cout << "found " << t->GetEntries() << " lines." << endl;
  strcat( outputFile, ".root"); //name of output file ends in .root, while name of Tree does not.
  TFile f( outputFile, "RECREATE" );
  f.cd();
  t->Write();
  f.Close();
}

#endif
