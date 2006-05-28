/*======================================================================
 cgkit - Python Computer Graphics Kit
 Copyright (C) 2004 Matthias Baas (baas@ira.uka.de)

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 cgkit homepage: http://cgkit.sourceforge.net
======================================================================*/

#ifndef PROCEDURALSLOT_H
#define PROCEDURALSLOT_H

/** \file proceduralslot.h
 Procedural slot implementation.
 */

#include "slot.h"
#include "component.h"

namespace support3d {

/**
  A generic procedural slot.

  A procedural slot is one that \em computes its value instead of taking 
  it as input from another slot. This means a procedural slot can never
  take input connections but of course, they can be dependent on other slots.

  The procedure that computes the output value is \em not implemented right
  in this class, but is implemented in some other Component class (usually
  the component that contains the procedural slot). The pointers to the
  member functions are then passed to the procedural slot via the setProcedure()
  methods.

  You must always provide the component whose methods are to be called and
  a pointer to a method that computes the output value. That method must take
  one argument which is a reference to the result value. Optionally, you can
  pass pointers to the onValueChanged() and onResize() callback methods.

  The %ProceduralSlot class takes two template parameters, the first is the
  type of the output value and the second is the Component class whose methods
  will be called.

  Example:

  \code
  // A component that has a procedural slot that computes a double value
  class MyComponent : public Component
  {
    ProceduralSlot<double, MyComponent> myslot;
    ...
    ...
    void computeValue(double& result);
  }

  // Constructor
  MyComponent::MyComponent()
    : myslot()
  {
    // Initialize the procedural slot
    myslot.setProcedure(this, &MyComponent::computeValue);
    addSlot("myslot", myslot);
  }
  \endcode

 */
template<class T, class C>
class ProceduralSlot : public Slot<T>
{
  public:
  /// The type of the method that computes the output value
  typedef void (C::* ComputeValuePtr)(T&);
  /// The type of the onValueChanged callback method
  typedef void (C::* OnValueChangedPtr)();
  /// The type of the onValueChanged callback method for arrays
  typedef void (C::* OnValueChangedArrayPtr)(int, int);
  /// The type of the onResize callback method for arrays
  typedef void (C::* OnResizeArrayPtr)(int);
  /// The type of the onControllerDeleted callback method
  typedef void (C::* OnControllerDeletedPtr)(int);

  protected:
  /// The component whose methods should be called.
  C* component;
  /// Pointer to the method that computes the output value.
  ComputeValuePtr computeValuePtr;
  /// Pointer to the onValueChanged() callback method 
  OnValueChangedPtr onValueChangedPtr;
  /// Pointer to the onValueChanged() callback method for arrays
  OnValueChangedArrayPtr onValueChangedArrayPtr;
  /// Pointer to the onResize() callback method for arrays
  OnResizeArrayPtr onResizeArrayPtr;

  public:
  /**
     Constructor.
   */
  ProceduralSlot() 
    : Slot<T>(Slot<T>::NO_INPUT_CONNECTIONS), component(0), 
      computeValuePtr(0), onValueChangedPtr(0), onValueChangedArrayPtr(0), onResizeArrayPtr(0) {}

  /**
    Set the procedure that computes the output value.

    \param acomp The component that implements the methods
    \param proc The method that computes the output value
    \param vc The onValueChanged callback method
   */
  void setProcedure(C* acomp, ComputeValuePtr proc, OnValueChangedPtr vc=0)
  {
    component = acomp;
    computeValuePtr = proc;
    onValueChangedPtr = vc;
  }

  /**
    Set the procedure that computes the output value.

    \param acomp The component that implements the methods
    \param proc The method that computes the output value
    \param vca The onValueChanged callback method for arrays
    \param ra The onResize callback method
   */
  void setProcedure(C* acomp, ComputeValuePtr proc, OnValueChangedArrayPtr vca, OnResizeArrayPtr ra)
  {
    component = acomp;
    computeValuePtr = proc;
    onValueChangedArrayPtr = vca;
    onResizeArrayPtr = ra;
  }

  
  virtual void onValueChanged() 
  { 
    Slot<T>::onValueChanged(); 
    if (onValueChangedPtr!=0)
      (component->*onValueChangedPtr)(); 
  }

  virtual void onValueChanged(int start, int end) 
  { 
    Slot<T>::onValueChanged(start, end); 
    if (onValueChangedArrayPtr!=0)
      (component->*onValueChangedArrayPtr)(start, end); 
  }

  virtual void onResize(int newsize) 
  { 
    Slot<T>::onResize(newsize); 
    if (onResizeArrayPtr!=0)
      (component->*onResizeArrayPtr)(newsize);
  }

  protected:
  virtual void computeValue() { (component->*computeValuePtr)(Slot<T>::value); }
};


}  // end of namespace

#endif
