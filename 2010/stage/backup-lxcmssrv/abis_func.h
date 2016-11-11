#ifndef  ABIS_FUNC_INC
#define  ABIS_FUNC_INC
// =====================================================================================
// 
//       Filename:  abis_func.h
// 
//    Description:  My functions for easier data analysis
// 
//        Version:  1.0
//        Created:  09/23/2009 10:37:09 PM
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), webmaster@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <string>
#include <map>
#include "TTree.h"

namespace abis{

    //create branch with var in all trees in map
    //various oveloaded functions
    void make_branch(std::map<std::string, TTree*>& map_, std::string name, double& var);
    void make_branch(std::map<std::string, TTree*>& map_, std::string name, int& var);
    void make_branch(std::map<std::string, TTree*>& map_, std::string name, float& var);
}

//implementations
void abis::make_branch(std::map<std::string, TTree*>& map_, std::string name, double& var){
    for(std::map<std::string, TTree*>::iterator it = map_.begin(); it != map_.end(); it++) 
        it->second->Branch(name.c_str(), &var, (name + "/D").c_str());
}

void abis::make_branch(std::map<std::string, TTree*>& map_, std::string name, int& var){
    for(std::map<std::string, TTree*>::iterator it = map_.begin(); it != map_.end(); it++) 
        it->second->Branch(name.c_str(), &var, (name + "/I").c_str());
}

void abis::make_branch(std::map<std::string, TTree*>& map_, std::string name, float& var){
    for(std::map<std::string, TTree*>::iterator it = map_.begin(); it != map_.end(); it++) 
        it->second->Branch(name.c_str(), &var, (name + "/F").c_str());
}
#endif // ----- #ifndef ABIS_FUNC_INC  -----
