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

#ifndef LIGHTSOURCE_H
#define LIGHTSOURCE_H

/** \file lightsource.h
 Contains the LightSource base class.
 */

#include "worldobject.h"

namespace support3d {

/**
  This is the base class for all light sources.

 */
class LightSource : public WorldObject
{
  public:
  /// Enabled state
  Slot<bool> enabled;

  /** Enable or disable shadows.

     It's up to the actual light source implementation and the renderer
     whether the light source can cast shadows at all. So this flag might 
     get ignored by an actual implementation.
   */
  Slot<bool> cast_shadow;

  /// Light intensity
  Slot<double> intensity;

  public:
  LightSource() : WorldObject(), enabled(true, 0), cast_shadow(false, 0), intensity(1.0, 0)
  {
    addSlot("enabled", enabled);
    addSlot("cast_shadow", cast_shadow);
    addSlot("intensity", intensity);
  }
  LightSource(string aname) : WorldObject(aname), enabled(true, 0), cast_shadow(false, 0), intensity(1.0, 0)
  {
    addSlot("enabled", enabled);
    addSlot("cast_shadow", cast_shadow);
    addSlot("intensity", intensity);
  }

  /**
    Check if a particular object casts shadows.

    \return True if \a obj is supposed to block light from this light source.
   */
  bool isShadowCaster(boost::shared_ptr<WorldObject> obj) const
  { 
    // Dummy implementation that checks if obj has a bool slot "cast_shadows"
    // and returns the value of that slot. If no valid slot is available
    // the function returns true.
    try
    {
      ISlot* slot = &(obj->slot("cast_shadows"));
      Slot<bool>* bslot = dynamic_cast<Slot<bool>*>(slot);
      if (bslot!=0)
      {
	return bslot->getValue();
      }
      else
      {
	return true;
      }
    }
    catch(EKeyError&)
    {
      return true;
    }
  }

  /**
    Check if a particular object receives shadows.

    \return True if \a obj is supposed to receive shadows from this light source.
   */
  bool isShadowReceiver(boost::shared_ptr<WorldObject> obj) const 
  { 
    // Dummy implementation that checks if obj has a bool slot "receive_shadows"
    // and returns the value of that slot. If no valid slot is available
    // the function returns true.
    try
    {
      ISlot* slot = &(obj->slot("receive_shadows"));
      Slot<bool>* bslot = dynamic_cast<Slot<bool>*>(slot);
      if (bslot!=0)
      {
	return bslot->getValue();
      }
      else
      {
	return true;
      }
    }
    catch(EKeyError&)
    {
      return true;
    }
  }
};


}  // end of namespace

#endif
