// =====================================================================================
// 
//       Filename:  cube.cpp
// 
//    Description:  cube class
// 
//        Version:  1.0
//        Created:  18/11/2009 11:39:26
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include "cube.h"

Cube::Cube(std::vector<int> l){
    lower = l;
}

std::ostream& operator<<(std::ostream& os, const Cube& c){
    //output cube as Mathematica list
    os << "{";
    std::copy(c.lower.begin(), c.lower.end() - 1, std::ostream_iterator<int>(os, ","));
    os << c.lower.back();
    os << "}";
    return os;
}

