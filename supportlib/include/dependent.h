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

#ifndef DEPENDENT_H
#define DEPENDENT_H

/** \file dependent.h
 Contains the Dependent base class and the NotificationForwarder.
 */

// Define the CGKIT_SHARED variable
#ifdef DLL_EXPORT_DEPENDENT
  #include "shared_export.h"
#else
  #include "shared.h"
#endif

namespace support3d {

/**
  Base class for everyone who wants to be notified by slots.

 */
class CGKIT_SHARED Dependent
{
  public:
  Dependent() {}
  virtual ~Dependent() {}
  /**
     Notification callback method.

     This method is called by a controlling slot whenever the value of the
     slot has changed. 

     The usual procedure in derived classes is to mark the local cache
     as invalid so that next time getValue() is called the updated value
     is retrieved from the controlling slot. All dependent slots also
     have to be notified.
   */
  virtual void onValueChanged() {};
  virtual void onValueChanged(int start, int end) {};
  /**
     Notification callback method.
     
     This method is called by a controlling array slot whenever the size
     of the slot has changed.

     \param newsize The new size of the array slot.
   */
  virtual void onResize(int newsize) {};
  /**
     Check if a dependent vetoes a resize operation.

     This method is called by a controlling slot whenever the slot size
     should be changed. If the method returns true the resize operation
     is rejected.
     The default implementation returns false. Only slots with size 
     constraints should return true.

     \param size The new size for the slot
     \return True if the resize operation has to be rejected
   */
  virtual bool queryResizeVeto(int size) { return false; };

  /**
     This callback is called when the controller is being deleted.

     When the controlling object is deleted it calls onControllerDeleted() on
     all dependent objects. The controller still exists and can be used. It is
     allowed to call removeDependent() on the controller, but it's not necessary
     as it is done by the controller automatically.
   */
  virtual void onControllerDeleted() {};
};

/** 
  Forward slot events to arbitrary class methods.

  This class can be used to forward slot events from one particular 
  slot (onValueChanged(), onResize(), ...) to an arbitrary method.
  The template parameter is the class of the object that will receive
  the events.

  \b Usage: Initialize the notification forwarder by calling an init() method
  which tells the forwarder which methods it should call when an event
  occurs. Then connect the slot you depend on with the forwarder instance.
  
 */
template<class T>
class NotificationForwarder : public Dependent
{
  public:
  typedef void (T::* OnValueChangedPtr)();
  typedef void (T::* OnValueChangedArrayPtr)(int start, int end);
  typedef void (T::* OnResizeArrayPtr)(int size);
  
  protected:
  T* _dest;
  OnValueChangedPtr _onValueChanged;
  OnValueChangedArrayPtr _onValueChangedArray;
  OnResizeArrayPtr _onResizeArray;

  public:
  NotificationForwarder()
  {
  }

  void init(T* dest, OnValueChangedPtr valchanged)
  {
    _dest = dest;
    _onValueChanged = valchanged;
    _onValueChangedArray = 0;
    _onResizeArray = 0;
  }

  void init(T* dest, OnValueChangedArrayPtr valchanged, OnResizeArrayPtr resize)
  {
    _dest = dest;
    _onValueChanged = 0;
    _onValueChangedArray = valchanged;
    _onResizeArray = resize;
  }

  void onValueChanged() 
  { 
    if (_onValueChanged!=0)
    {
      (_dest->*_onValueChanged)();
    }
  }
  void onValueChanged(int start, int end)
  {
    if (_onValueChangedArray!=0)
    {
      (_dest->*_onValueChangedArray)(start, end);
    }
  }
  void onResize(int newsize) 
  {
    if (_onResizeArray!=0)
    {
      (_dest->*_onResizeArray)(newsize);
    }
  }
};


}  // end of namespace

#endif
