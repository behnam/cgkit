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

#ifndef MATERIAL_H
#define MATERIAL_H

/** \file material.h
 Contains the base Material class.
 */

#include "component.h"
#include "slot.h"

namespace support3d {

/**
  Base material.
 */
class Material : public Component
{
  public:
  /// Density of the material (used for dynamics).
  Slot<double> density;

  public:
  Material() : Component(), density() { addSlot("density", density); }
  Material(string aname, double adensity=1.0) 
    : Component(aname), density(adensity, 0) { addSlot("density", density); }
  virtual ~Material() {}

  virtual void applyGL() {}
  virtual bool usesBlending() { return false; }
};


}  // end of namespace

#endif
