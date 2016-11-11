// =====================================================================================
// 
//       Filename:  menger.cpp
// 
//    Description:  makes points for n interations of Menger sponge
// 
//        Version:  1.0
//        Created:  18/11/2009 11:31:35
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include "cube.h"
#include <vector>
#include <deque>
#include <iostream>
#include <iterator>
#include <algorithm>

using namespace std;

void make_cubes(std::deque<Cube>& cubes);
void menger_iteration(int n, ostream& os=cout);

int main(int argc, char **argv) {
    int n;
    cin >> n;
    menger_iteration(n);
    return 0;
}	

void menger_iteration(int n, ostream& os){
    vector<int> origin(3,0);

    deque<Cube> cubes;
    cubes.push_back(Cube(origin));

    for (int i = 0; i < n; i++) make_cubes(cubes);

    string graphics = "Gray,Cuboid[";
    os << "{" << graphics;
    copy(cubes.begin(), cubes.end() - 1, ostream_iterator<Cube>(os, "], Cuboid["));
    os << cubes.back();
    os << "]}" << endl;
}

void make_cubes(std::deque<Cube>& cubes){
    int n_cubes = cubes.size();
    for (int c = 0; c < n_cubes; c++) {
        std::vector<int> point(cubes.front().get_lower());
        cubes.pop_front();

        for (int i = 0; i < 3; i++) point[i] *= 3;

        for (int i = 0; i < 3; i++) {
            int old_y = point[1];
            for (int j = 0; j < 3; j++) {
                int old_z = point[2];
                for (int k = 0; k < 3; k++) {
                    int counters[] = {i, j, k};
                    cubes.push_back(Cube(point));
                    if (std::count(counters, counters+3, 1) >= 2) continue;
                    point[2]++;
            }       
                point[2] = old_z;
                point[1]++;
            }       
            point[1] = old_y;
            point[0]++;
        }       
    }       
}
