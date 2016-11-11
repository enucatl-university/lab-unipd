//Analisi 1.02 -- Ilaria Brivio e Matteo Abis, 01/2008
//
//Analizza dati da file, restituendo tabella di frequenza,
//media aritmetica, errore quadratico medio ed errore sulla media.
#include<iostream>
#include<fstream>
#include<string>
#include<cmath>

using namespace std;

int contarighe(string);
double trovamax(double[], int );
double trovamin(double[], int );
double media(double[], int );
double sigma(double[], int );

int main()
	{
	string nomefile;
	cout << "Inserire il nome del file da analizzare: ";
	cin >> nomefile;
//copia dati sperimentali su array dinamico
	ifstream dati;
	dati.open(nomefile.c_str());
	while (!dati.is_open())
	{
		cout << "File non trovato!" << endl;
		cout << "Inserire il nome del file da analizzare: ";
		cin >> nomefile;
		dati.open(nomefile.c_str());
	}
	int osservazioni = contarighe(nomefile);
	if (osservazioni==1) //if per singolare e plurale
		cout << "\u00c8 stato trovato un solo dato." << endl;
	else cout << "Sono stati trovati " << osservazioni << " dati." << endl;
	double *tempi = new double[osservazioni];
	for(int i=0; i<osservazioni ; i++)
		dati >> tempi[i];
	dati.close();
	double delta; //dimensione intervallini (ms)
	cout << "Inserire dimensione intervallini (ms): ";
	cin >> delta;
	cin.get();	
	double min, max;
	//calcola media, sigma, massimo, minimo e numero di intervalli
	double med = media(tempi,osservazioni);
	double s = sigma(tempi,osservazioni);
	min = trovamin(tempi,osservazioni);
	max = trovamax(tempi,osservazioni);
	// calcola numero di intervallini presenti
	int m = int(((max-min)/delta)+2);
	//calcola da dove partono gli intervallini per avere la media al centro
	double partenza;
	for (int i=0;med -(i+.5)*delta > min; i++)
		partenza= med -(i+1.5)*delta;
	int *freq = new int[m];
	for(int i=0;i<m; i++) //inizializza a zero tutto l'array
		freq[i]=0;
	int j=0;
	//calcola frequenze in intervallini
	for(int i=0;i<osservazioni;i++)
		{
			for(j=0;j<m;j++)
		if((tempi[i]>(partenza+delta*j)) && (tempi[i] <=
(partenza+delta*(j+1))))
			freq[j]++;
		}
	cout << "Vuoi salvare i dati sulla frequenza? [s/N] ";
	char scelta;
	cin.get(scelta);
	if(scelta!='\n') cin.get();
	string fileSalva;
	ofstream salva;
	switch(scelta) //scelta output: file, stdout o niente.
	{
		case 's':	cout << "Salva come: ";
				cin >> fileSalva;
				salva.open(fileSalva.c_str());
				for(int i=0;i<m;i++)
			salva << partenza+delta*i << " " << freq[i] << endl;
				salva.close();
				cout << "Dati salvati con successo." << endl;
				break;
		default :
			cout << "Vuoi stamparli su schermo? [s/N] ";
			cin.get(scelta);
			if(scelta!='\n') cin.get();
			switch(scelta)
			{
				case 's':
				for(int i=0;i<m;i++)
			cout << partenza+delta*i << " " << freq[i] << endl;
				default : break;
			}
			break;
	}
	// calcola media aritmetica
	cout << "La media aritmetica \u00e8: " << med << endl;
	// errore quadratico medio
	cout << "L'errore quadratico medio \u00e8 " << s << endl;
	cout << "L'errore sulla media \u00e8 " << s/sqrt(osservazioni) << endl;
	int conta=0;
//scarta valori oltre  media-3sigma e media+3sigma
	for(int i=0;i<osservazioni;i++)
	{
		if(tempi[i]>= (med - 3*s) && tempi[i] <= (med + 3*s))
		conta++;
	}
	double *buoni = new double[conta];
	int k=0;
	for(int i=0;i<osservazioni;i++)
	{
		if(tempi[i] >= (med - 3*s) && tempi[i] <= (med + 3*s))
	{
		buoni[k]=tempi[i];
		k++;
	}
	}
		// calcola media aritmetica
	int scartati = osservazioni-conta;
	if (scartati==1) //singolare e plurale
		cout << "\u00c8 stato scartato un solo valore." << endl;
	else	cout << "Sono stati scartati " << scartati << " valori." <<
endl;
	med = media(buoni,conta);
	s = sigma(buoni,conta);
	cout << "La nuova media \u00e8 " << med << endl;
	// errore quadratico medio
	cout << "Il nuovo errore quadratico medio \u00e8 " << s << endl;
	cout << "L'errore sulla media \u00e8 " << s/sqrt(conta) << endl;	
	return 0;
	}

int contarighe(string nomefile)
{
	ifstream input(nomefile.c_str());
	int righe=0;
	double numeri;
	while (input >> numeri)
	{
		righe++;
	}
	input.close();
	return righe;
}

double trovamax(double array[], int l)
{
	double max=array[0];
	for(int i=0;i<l;i++)
	{
		if (max < array[i])
			max = array[i];
	}
	return max;
}

double trovamin(double array[], int l)
{
	double min=array[0];
	for(int i=0;i<l;i++)
	{
		if (min > array[i])
		min = array[i];
	}
	return min;
}

double media(double valori[], int l)
{
	double somma=0;
	for(int i=0;i<l;i++)
		somma+=valori[i];
	double xm = somma / double(l);
	return xm;
}

double sigma(double valori[], int l)
{
	double somma=0;
	for(int i=0;i<l;i++)
	somma+=(valori[i]-media(valori,l))*(valori[i]-media(valori,l));
	double si = sqrt(somma/double(l));
	return si;
}

