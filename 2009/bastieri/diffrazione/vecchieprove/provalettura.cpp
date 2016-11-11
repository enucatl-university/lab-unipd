#include "readData.cpp"

int main( int argc, char* argv[] ) {
  char* progname = argv[0];
  cout << " program name: " << progname << endl;
  for ( int i = 1; i < argc; i++ ) {
    cout << " argument n. " << i << " " << argv[i] << endl;
  }
  char* input = argv[1];
  char* output = argv[2];
  saveData( input, output );
}
