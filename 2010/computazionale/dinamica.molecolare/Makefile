all: md prova drawer

md: md.cpp verlet.cpp verlet.h
	g++ -ggdb -I ${ROOTINCLUDE} -L ${ROOTLIB} -o md md.cpp verlet.cpp ${ROOT_LIBLIST}

prova: provadft.cpp verlet.cpp verlet.h
	g++ -ggdb -o prova provadft.cpp verlet.cpp

drawer: drawer.cpp
	g++ -ggdb -I ${ROOTINCLUDE} -L ${ROOTLIB} -o drawer drawer.cpp  ${ROOT_LIBLIST}
