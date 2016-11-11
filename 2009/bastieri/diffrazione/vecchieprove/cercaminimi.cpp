const int n = 8;
int minimi[n];

for( int i = 0; i < n ; i++ ){
	int *lookup = interval( step, limits[i], limits[i+1]);
	int minPos = minPosition( intensity, lookup[0], lookup[1] );
	minimi[i] = step[minPos];
}