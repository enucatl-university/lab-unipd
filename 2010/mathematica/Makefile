all: menger julia poincare

menger: menger.cpp cube.cpp
	g++ -ggdb -o menger menger.cpp cube.cpp

julia: julia.cpp
	g++ -o julia julia.cpp

poincare: forzato.cpp forzato_strang.h forzato_strang.cpp
	g++ -ggdb -o forzato forzato.cpp forzato_strang.cpp
