// =====================================================================================
//        Class:  GreaterThan
//  Description:  Simple comparison for count_if
// =====================================================================================
class GreaterThan
{
    public:

        // ====================  LIFECYCLE     =======================================
        GreaterThan(double limit);                             // constructor

        // ====================  ACCESSORS     =======================================
        bool operator()(int value) const { return value > limit; }

    private:
        double limit;

}; // -----  end of class GreaterThan  -----

GreaterThan::GreaterThan(double limit_){
    limit = limit_;
}
