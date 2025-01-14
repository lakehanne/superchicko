/******************************************************************************
                              *
******************************************************************************/

#ifndef SOFA_COMPONENT_CONSTRAINTSET_SURFACEPRESSURECONSTRAINT_H
#define SOFA_COMPONENT_CONSTRAINTSET_SURFACEPRESSURECONSTRAINT_H

#include "IABPlugin/constraint/model/SurfacePressureModel.h"
#include <sofa/helper/OptionsGroup.h>

#include <IABPlugin/ForceFields/include/initIABPlugin.h>

namespace sofa
{

namespace component
{

namespace constraintset
{

namespace _surfacepressureconstraint_
{

    using sofa::core::ConstraintParams ;
    using sofa::defaulttype::BaseVector ;
    using sofa::core::behavior::ConstraintResolution ;
    using helper::vector;

class VolumeGrowthConstraintResolution : public ConstraintResolution
{
public:
    VolumeGrowthConstraintResolution(const double& imposedVolumeGrowth, const double& minPressure, const double& maxPressure);

    //////////////////// Inherited from ConstraintResolution ////////////////////
    void init(int line, double** w, double *lambda) override;
    void resolution(int line, double** w, double* d, double* lambda, double* dfree) override;
    /////////////////////////////////////////////////////////////////////////////

protected:
    double      m_wActuatorActuator;
    double      m_imposedVolumeGrowth;
    double      m_minPressure;
    double      m_maxPressure;
};

class SurfacePressureConstraintResolution : public ConstraintResolution
{
public:
    SurfacePressureConstraintResolution(const double& imposedPressure, const double& minVolumeGrowth, const double& maxVolumeGrowth);

    //////////////////// Inherited from ConstraintResolution ///////////////////
    void init(int line, double** w, double *force) override;
    void resolution(int line, double** w, double* d, double* force, double* dfree) override;
    /////////////////////////////////////////////////////////////////////////////

protected:
    double      m_wActuatorActuator;
    double      m_imposedPressure;
    double      m_minVolumeGrowth;
    double      m_maxVolumeGrowth;
};


/**
 * This component constrains a model by applying pressure on surfaces (for exemple cavities).
 * Description can be found at:
 * https://softrobotscomponents.readthedocs.io
*/
template< class DataTypes >
class SOFA_IABPlugin_API SurfacePressureConstraint : public SurfacePressureModel<DataTypes>
{
public:
    SOFA_CLASS(SOFA_TEMPLATE(SurfacePressureConstraint,DataTypes), SOFA_TEMPLATE(SurfacePressureModel,DataTypes));

    typedef typename DataTypes::VecCoord    VecCoord;
    typedef typename DataTypes::VecDeriv    VecDeriv;
    typedef typename DataTypes::Coord       Coord;
    typedef typename DataTypes::Deriv       Deriv;
    typedef typename DataTypes::MatrixDeriv MatrixDeriv;
    typedef typename Coord::value_type      Real;
    typedef typename core::behavior::MechanicalState<DataTypes> MechanicalState;
    typedef typename DataTypes::MatrixDeriv::RowIterator MatrixDerivRowIterator;
    typedef Data<VecCoord>                  DataVecCoord;
    typedef Data<VecDeriv>                  DataVecDeriv;
    typedef Data<MatrixDeriv>               DataMatrixDeriv;

public:
    SurfacePressureConstraint(MechanicalState* object = nullptr);

    ~SurfacePressureConstraint() override;

    ////////////////////////////  Inherited from BaseObject //////////////////////
    void init() override;
    void reinit() override;
    void reset() override;
    //////////////////////////////////////////////////////////////////////////////


    /////////////////// from sofa::core::behavior::Constraint /////////////////////////
    void getConstraintResolution(std::vector<ConstraintResolution*>& resTab,
                                 unsigned int& offset) override;
    ///////////////////////////////////////////////////////////////////////////////////


protected:

    Data<vector<Real> >                     d_value;
    Data<unsigned int>                      d_valueIndex;
    Data<helper::OptionsGroup>              d_valueType;

    double                                  m_pressure;
    double                                  m_volumeGrowth;
    vector<Real>                            m_initialValue;

    ////////////////////////// Inherited attributes ////////////////////////////
    using SurfacePressureModel<DataTypes>::d_volumeGrowth ;
    using SurfacePressureModel<DataTypes>::d_maxVolumeGrowthVariation ;
    using SurfacePressureModel<DataTypes>::d_maxVolumeGrowth ;
    using SurfacePressureModel<DataTypes>::d_minVolumeGrowth ;
    using SurfacePressureModel<DataTypes>::d_maxPressure ;
    using SurfacePressureModel<DataTypes>::d_minPressure ;
    using IABConstraint<DataTypes>::m_componentstate;
    ////////////////////////////////////////////////////////////////////////////

private:
    void initData();
    void setUpVolumeLimits(double& imposedValue, double& minPressure, double& maxPressure);
    void setUpPressureLimits(double& imposedValue, double& minVolumeGrowth, double& maxVolumeGrowth);

};

// Declares template as extern to avoid the code generation of the template for
// each compilation unit. see: http://www.stroustrup.com/C++11FAQ.html#extern-templates
using defaulttype::Vec3Types;
extern template class SOFA_IABPlugin_API SurfacePressureConstraint<Vec3Types>;


}

using _surfacepressureconstraint_::SurfacePressureConstraint;
using _surfacepressureconstraint_::SurfacePressureConstraintResolution;
using _surfacepressureconstraint_::VolumeGrowthConstraintResolution;

} // namespace constraintset

} // namespace component

} // namespace sofa

#endif // SOFA_COMPONENT_CONSTRAINTSET_SURFACEPRESSURECONSTRAINT_H
