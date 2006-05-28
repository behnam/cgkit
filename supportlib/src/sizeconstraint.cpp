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

#include "sizeconstraint.h"
#include "arrayslot.h"

namespace support3d {

/**
  Calls resize() on all registered slots.

  This is called by actual constraint implementations whenever the size
  has changed. The size attribute must be set to the new size before
  calling this method.

  The method may throw an exception when a resize operation on a slot
  has failed. In this case the registered slots may have different sizes.
  In this case, the caller must call the method again after restoring the
  original size.
 */
void SizeConstraintBase::execSlotResize()
{
  std::vector<IArraySlot*>::iterator it;
  std::vector<IArraySlot*>::iterator it_end = slots.end();
  for(it=slots.begin(); it!=it_end; it++)
  {
    (*it)->resize(size);
  }
}

// registerSlot
void SizeConstraintBase::registerSlot(IArraySlot& aslot)
{
  DEBUGINFO1(this, "SizeConstraint::registerSlot(0x%x)", long(&aslot));

  // Check if the slot is already there...
  std::vector<IArraySlot*>::iterator it = std::find(slots.begin(), slots.end(), &aslot);
  if (it!=slots.end())
    throw EValueError("Slot is already registered with the size constraint.");

  // Add the slot...
  slots.push_back(&aslot);
  // ...and adjust the size
  aslot.resize(size);

  DEBUGINFO2(this, "SizeConstraint::registerSlot(0x%x) -- end (#reg slots: %d)", long(&aslot), slots.size());
}

// unregisterSlot
void SizeConstraintBase::unregisterSlot(IArraySlot& aslot)
{
  DEBUGINFO1(this, "SizeConstraint::unregisterSlot(0x%x)", long(&aslot));

  // Search for the slot...
  std::vector<IArraySlot*>::iterator it = std::find(slots.begin(), slots.end(), &aslot);
  // ...and remove it (if it was there)
  if (it!=slots.end())
  {
    slots.erase(it);
  }
  else
  {
    throw EValueError("Could not unregister slot from size constraint.");
  }

  DEBUGINFO2(this, "SizeConstraint::unregisterSlot(0x%x) -- end (#reg slots: %d)", long(&aslot), slots.size());
}

/////////////// UserSizeConstraint ////////////////////

void UserSizeConstraint::setSize(int newsize)
{ 
  // Store the previous size so it can be restored if a resize 
  // operation failed
  int prevsize = size;

  size = newsize;
  try
  {
    execSlotResize(); 
  }
  catch(...)
  {
    // A registered slot could not resize, so restore the previous size
    // (which ought to work as those that have already been resized actually
    // *are* resizeable and the other ones haven't been resized anyway)
    size = prevsize;
    execSlotResize();
    throw;
  }
}

/////////////// LinearSizeConstraint ////////////////////

LinearSizeConstraint::LinearSizeConstraint(IArraySlot& actrl, int a, int b)
  : SizeConstraintBase(), Dependent(), ctrl(&actrl), a(a), b(b)
{
  ctrl->addDependent(this);
}

LinearSizeConstraint::~LinearSizeConstraint()
{
  DEBUGINFO(this, "LinearSizeConstraint::~LinearSizeConstraint()");
  if (ctrl!=0)
  {
    DEBUGINFO1(this, "  0x%x->removeDependent()", long(ctrl));
    ctrl->removeDependent(this);
  }
  DEBUGINFO(this, "LinearSizeConstraint::~LinearSizeConstraint() --- end");
}

// setCoeffs
void LinearSizeConstraint::setCoeffs(int newa, int newb)
{
  int preva = a;
  int prevb = b;
  a = newa;
  b = newb;
  try
  {
    onResize(ctrl->size());
  }
  catch(...)
  {
    a = preva;
    b = prevb;
    throw;
  }
}

// onResize
void LinearSizeConstraint::onResize(int newsize)
{ 
  // Store the previous size so it can be restored if a resize 
  // operation failed
  int prevsize = size;

  size = a*newsize+b; 
  try
  {
    execSlotResize(); 
  }
  catch(...)
  {
    // A registered slot could not resize, so restore the previous size
    // (which ought to work as those that have already been resized actually
    // *are* resizeable and the other ones haven't been resized anyway)
    size = prevsize;
    execSlotResize();
    throw;
  }
}

// queryResizeVeto
bool LinearSizeConstraint::queryResizeVeto(int size)
{
  std::vector<IArraySlot*>::iterator it;
  std::vector<IArraySlot*>::iterator it_end = slots.end();
  // Issue a veto if one of the registered slots cannot be resized...
  for(it=slots.begin(); it!=it_end; it++)
  {
    if (!(*it)->isResizable(size, true))
      return true;
  }
  return false;
}


}  // end of namespace
