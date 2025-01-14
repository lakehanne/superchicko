/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture                          *
*                (c) 2006-2018 INRIA, USTL, UJF, CNRS, MGH                    *
*                                                                             *
* This library is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This library is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this library; if not, write to the Free Software Foundation,     *
* Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.          *
*******************************************************************************
*                           Plugin SoftRobots    v1.0                         *
*				                                              *
* This plugin is also distributed under the GNU LGPL (Lesser General          *
* Public License) license with the same conditions than SOFA.                 *
*                                                                             *
* Contributors: Defrost team  (INRIA, University of Lille, CNRS,              *
*               Ecole Centrale de Lille)                                      *
*                                                                             *
* Contact information: https://project.inria.fr/softrobot/contact/            *
*                                                                             *
******************************************************************************/
#ifndef SOFA_CORE_BEHAVIOR_IABConstraint_INL
#define SOFA_CORE_BEHAVIOR_IABConstraint_INL

#include "IABPlugin/behavior/IABConstraint.h"
#include <SofaBaseLinearSolver/FullMatrix.h>

namespace sofa
{

namespace core
{

namespace behavior
{

using component::linearsolver::FullVector;
using helper::ReadAccessor;

template<class DataTypes>
IABConstraint<DataTypes>::IABConstraint(MechanicalState<DataTypes> *mm)
    : d_endTime( initData(&d_endTime,(Real)-1, "endTime",
                          "The IABConstraint stops acting after the given value.\n"
                          "Use a negative value for infinite IABConstraints") )
    , m_state(mm)
{
}

template<class DataTypes>
IABConstraint<DataTypes>::~IABConstraint()
{
}


template <class DataTypes>
bool IABConstraint<DataTypes>::isActive() const
{
    if( d_endTime.getValue()<0 ) return true;
    return d_endTime.getValue()>getContext()->getTime();
}


template<class DataTypes>
void IABConstraint<DataTypes>::init()
{
    BaseConstraint::init();

    /// This throw a LogicException (logic exception are not meant for users but for
    /// developpers).
    if(getContext()==nullptr)
        dmsg_error() << "A constraint assumes that there is a valid context. Please fix your code. " ;

    m_state = dynamic_cast< MechanicalState<DataTypes>* >(getContext()->getMechanicalState());
}


template<class DataTypes>
void IABConstraint<DataTypes>::getConstraintViolation(const ConstraintParams* cParams,
                                                             BaseVector *resV)
{
    if (cParams)
    {
        const DataVecCoord& xfree = *cParams->readX(m_state);
        ReadAccessor<Data<VecCoord>> x = m_state->readPositions();

        VecDeriv dx;
        dx.resize(m_state->getSize());
        for(unsigned int i=0; i<dx.size(); i++)
            dx[i] = DataTypes::coordDifference(xfree.getValue()[i],x[i]);

        const Data<MatrixDeriv> *J = cParams->j()[m_state].read();
        FullVector<Real> Jdx;
        Jdx.resize(m_nbLines);
        Jdx.clear();
        for(unsigned int i=0; i<m_nbLines; i++)
        {
            MatrixDerivRowConstIterator rowIt = J->getValue().readLine(m_constraintId+i);
            for (MatrixDerivColConstIterator colIt = rowIt.begin(); colIt != rowIt.end(); ++colIt)
                Jdx.add(i, colIt.val() * dx[colIt.index()]);
        }

        getConstraintViolation(cParams, resV, &Jdx);
    }
}


template<class DataTypes>
void IABConstraint<DataTypes>::buildConstraintMatrix(const ConstraintParams* cParams,
                                                            MultiMatrixDerivId cId,
                                                            unsigned int &cIndex)
{
    if (cParams)
    {
        buildConstraintMatrix(cParams, *cId[m_state].write(), cIndex, m_state->readPositions().ref());
        // Give *cParams->readX(m_state) -> xfree
        //buildConstraintMatrix(cParams, *cId[m_state].write(), cIndex, *cParams->readX(m_state));
    }
}


template<class DataTypes>
void IABConstraint<DataTypes>::storeLambda(const ConstraintParams* cParams,
                                                  MultiVecDerivId res,
                                                  const BaseVector* lambda)
{
    if (cParams)
        storeLambda(cParams, *res[m_state].write(), *cParams->readJ(m_state), lambda);
}


template<class DataTypes>
void IABConstraint<DataTypes>::storeLambda(const ConstraintParams* cParams,
                                                  Data<VecDeriv>& result,
                                                  const Data<MatrixDeriv>& jacobian,
                                                  const BaseVector* lambda)
{
    auto res = sofa::helper::write(result, cParams);
    const MatrixDeriv& j = jacobian.getValue(cParams);
    j.multTransposeBaseVector(res, lambda ); // lambda is a vector of scalar value so block size is one.
}


template<class DataTypes>
std::string IABConstraint<DataTypes>::getTemplateName() const
{
    return templateName(this);
}

template<class DataTypes>
std::string IABConstraint<DataTypes>::templateName(const IABConstraint<DataTypes>*)
{
    return DataTypes::Name();
}


} // namespace behavior

} // namespace core

} // namespace sofa

#endif // SOFA_CORE_BEHAVIOR_IABConstraint_INL
