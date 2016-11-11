all: circuit eigen provajac

circuit: circuit.cpp matrix.h matrix.cpp
	g++ -ggdb -o circuit circuit.cpp matrix.cpp

eigen: well.cpp jacobi2.cpp jacobi2.h 
	g++ -ggdb -o well well.cpp jacobi2.cpp

provajac: jacobi2.cpp jacobi2.h provajac.cpp
	g++ -ggdb -o provajac jacobi2.cpp provajac.cpp 
