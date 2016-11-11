#ifndef Circular_Reconstruction_h
#define Circular_Reconstruction_h

#include "TMath.h"
#include <cmath>
#include <map>
#include <string>
#include <iostream>

//return distance between point a and point b
double euclid_distance(const math::XYZPointD& a, const math::XYZPointD& b);


// =====================================================================================
//        Class:  CircularReconstruction
//  Description:  calculates various quantities (impact parameter, etc) with
//  a circular reconstruction
// =====================================================================================
//
class CircularReconstruction
{
    public:

        // ====================  LIFECYCLE     =======================================
        CircularReconstruction(pat::Muon* particle);                             // constructor
        ~CircularReconstruction();                             // constructor

        // ====================  ACCESSORS     =======================================
        double get_radius_global();
        double get_radius_inner();
        math::XYZPointD& get_centre_global();
        double impact_parameter_global();
        math::XYZPointD& get_centre_inner();
        double impact_parameter_inner();
        // ====================  MUTATORS      =======================================

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        const math::XYZPointD primary_vertex;
        const double magnetic_field;
        const double particle_mass;
        double pt_global, pt_inner;
        double phi_global, phi_inner;
        double chi0_global, chi0_inner;
        double radius_global, radius_inner;
        int charge;
        //use globalTrack (tracker + muon detector) or innerTrack (tracker
        //only)
        double d_global, d_inner;
        math::XYZPointD reference_point_global, reference_point_inner;
        math::XYZPointD centre_global, centre_inner;


}; // -----  end of class CircularReconstruction  -----

CircularReconstruction::CircularReconstruction(pat::Muon* particle):
    primary_vertex(0.03203, 0.00013, 0),
    magnetic_field(3.8),        /* Costant Magnetic Field in Tesla */
    particle_mass(0.1056583668) /* ± 0.0000000038  PDG MOHR 2008 with 2006 CODATA value (constant conversion) */
{
    pt_global = particle->globalTrack()->pt();
    phi_global = particle->globalTrack()->phi();
    charge = particle->charge();
    reference_point_global = particle->globalTrack()->referencePoint();
    chi0_global = phi_global + charge * M_PI_2;
    get_radius_global();
    get_centre_global();
    impact_parameter_global();

    pt_inner = particle->innerTrack()->pt();
    phi_inner = particle->innerTrack()->phi();
    charge = particle->charge();
    reference_point_inner = particle->innerTrack()->referencePoint();
    chi0_inner = phi_inner + charge * M_PI_2;
    get_radius_inner();
    get_centre_inner();
    impact_parameter_inner();
}

CircularReconstruction::~CircularReconstruction(){
}

double CircularReconstruction::get_radius_global(){
    radius_global = 1e11*pt_global/(magnetic_field*TMath::C());
    //[cm]
    return radius_global;
}

double CircularReconstruction::get_radius_inner(){
    radius_inner = 1e11*pt_inner/(magnetic_field*TMath::C());
    //[cm]
    return radius_inner;
}

math::XYZPointD& CircularReconstruction::get_centre_global(){
    double x = reference_point_global.X() - radius_global*cos(chi0_global);
    double y = reference_point_global.Y() - radius_global*sin(chi0_global);
    double z = 0;
    centre_global = math::XYZPointD(x, y, z);
    return centre_global;
}

math::XYZPointD& CircularReconstruction::get_centre_inner(){
    double x = reference_point_inner.X() - radius_inner*cos(chi0_inner);
    double y = reference_point_inner.Y() - radius_inner*sin(chi0_inner);
    double z = 0;
    centre_inner = math::XYZPointD(x, y, z);
    return centre_inner;
}

double CircularReconstruction::impact_parameter_inner(){
    d_inner = euclid_distance(primary_vertex, centre_inner) - radius_inner;
    return d_inner;
}

double CircularReconstruction::impact_parameter_global(){
    d_global = euclid_distance(primary_vertex, centre_global) - radius_global;
    return d_global;
}

double euclid_distance(const math::XYZPointD& a, const math::XYZPointD& b){
    double x = a.X() - b.X();
    double y = a.Y() - b.Y();
    double z = a.Z() - b.Z();
    return sqrt(x*x + y*y + z*z);
}

#endif

