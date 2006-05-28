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

#ifndef COMPONENT_H
#define COMPONENT_H

/** \file component.h
 Contains the base Component class.
 */

#include <map>
#include <string>
#include <memory>
#include "slot.h"
#include "boost/shared_ptr.hpp"

// Define the CGKIT_SHARED variable
#ifdef DLL_EXPORT_COMPONENT
  #include "shared_export.h"
#else
  #include "shared.h"
#endif

namespace support3d {

using std::string;
using std::auto_ptr;


////////////////////////////////////////////////////////////////
// Slot descriptors
////////////////////////////////////////////////////////////////

struct SlotDescriptor
{
  virtual ~SlotDescriptor() {}
  virtual ISlot& getSlot() = 0;
};

struct DynamicSlotDescriptor : public SlotDescriptor
{
  auto_ptr<ISlot> slot;
  DynamicSlotDescriptor(auto_ptr<ISlot> aslot) : slot(aslot) {}
  ISlot& getSlot() { return *(slot.get()); }
};

struct StaticSlotDescriptor : public SlotDescriptor
{
  ISlot& slot;
  StaticSlotDescriptor(ISlot& aslot) : slot(aslot) {}
  ISlot& getSlot() { return slot; }
};


////////////////////////////////////////////////////////////////
// Component
////////////////////////////////////////////////////////////////

class CGKIT_SHARED SlotIterator
{
  private:
  std::map<string, SlotDescriptor*>::const_iterator it;
  std::pair<string, SlotDescriptor*> item;

  public:
  SlotIterator() { }
  SlotIterator(std::map<string, SlotDescriptor*>::const_iterator ait)
    : it(ait) 
  {}

  bool operator==(const SlotIterator& s) { return it==s.it; }
  bool operator!=(const SlotIterator& s) { return it!=s.it; }
  void operator++() { ++it; }
  void operator++(int) { it++; }
  std::pair<string, SlotDescriptor*>* operator->() 
  { 
    item.first=it->first; 
    item.second=it->second; 
    return &item; 
  }
};

/**
  This is the base class for all components.

  A component is a named container for slots.

  \see ISlot
 */
class CGKIT_SHARED Component
{
  public:
//  typedef std::map<string, SlotDescriptor*>::const_iterator SlotIterator;
  typedef support3d::SlotIterator SlotIterator;

  /// The name of the component.
  //Slot<string> name;
  string name;

  protected:

  /// Slot dictionary.
  std::map<string, SlotDescriptor*> slots;

  public:
  Component(string aname="");
  virtual ~Component();

  /**
    Return the component's name.

    \return Name
   */
  virtual string getName() const { return name; }

  /**
    Set a new name for the component.

  \param aname The new name to set.
   */
  virtual void setName(string aname) { name=aname; }

  bool hasSlot(const string& name) const;
  int numSlots() const;
  ISlot& slot(const string& name) const;
  
  void addSlot(const string& name, auto_ptr<ISlot> slot);
  void addSlot(const string& name, ISlot& slot);

  void removeSlot(const string& name);

//  SlotIterator slotsBegin() const { return slots.begin(); }
//  SlotIterator slotsEnd() const { return slots.end(); }
  SlotIterator slotsBegin() const { return SlotIterator(slots.begin()); }
  SlotIterator slotsEnd() const { return SlotIterator(slots.end()); }
};


}  // end of namespace

#endif
