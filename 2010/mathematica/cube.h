#ifndef  CUBE_INC
#define  CUBE_INC
// =====================================================================================
// 
//       Filename:  cube.h
// 
//    Description:  cube class header
// 
//        Version:  1.0
//        Created:  18/11/2009 11:39:47
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <vector>
#include <iterator>

// =====================================================================================
//        Class:  Cube
//  Description:  l
// =====================================================================================
class Cube
{
    public:

        // ====================  LIFECYCLE     =======================================
        Cube(std::vector<int> lower);                             // constructor
        //a cube is drawn with unit side from lower vertex with
        //Mathematica Cuboid

        // ====================  ACCESSORS     =======================================
        inline std::vector<int> get_lower() const { return lower; }

        // ====================  MUTATORS      =======================================

        // ====================  OPERATORS     =======================================
        friend std::ostream& operator<<(std::ostream& os, const Cube& c);

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        std::vector<int> lower;

}; // -----  end of class Cube  -----

#endif // ----- #ifndef CUBE_INC  -----
