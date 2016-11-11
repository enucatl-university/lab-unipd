all: rk drawer resonance

rk: harmonic_rk4.h harmonic_rk4.cpp solver.cpp
	g++ -ggdb -I ${ROOTINCLUDE} -L ${ROOTLIB} -o rk solver.cpp harmonic_rk4.cpp ${ROOT_LIBLIST}

drawer: drawer.cpp
	g++ -ggdb -I ${ROOTINCLUDE} -L ${ROOTLIB} -o drawer drawer.cpp ${ROOT_LIBLIST}

resonance: resonance.cpp harmonic_rk4.h harmonic_rk4.cpp solver.cpp
	g++ -ggdb -I ${ROOTINCLUDE} -L ${ROOTLIB} -o resonance resonance.cpp harmonic_rk4.cpp ${ROOT_LIBLIST}
