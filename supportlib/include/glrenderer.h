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

#ifndef GLRENDERER_H
#define GLRENDERER_H

/** \file glrenderer.h
 OpenGL renderer.
 */

#include "mat4.h"
#include "worldobject.h"
#include "glmaterial.h"

namespace support3d {

class GLRenderInstance
{
  public:
  int viewx;
  int viewy;
  int viewwidth;
  int viewheight;
  mat4d projectionmatrix;
  // View matrix for left eye (and non-stereo view)
  mat4d viewmatrix1;
  // View matrix for right eye
  mat4d viewmatrix2;

  // Background color
  vec4d clearcol;

  /// Shall the display be left handed?
  bool left_handed;

  bool draw_solid;

  /// Bounding boxes?
  bool draw_bboxes;

  bool draw_coordsys;

  // Small coordinate system in the lower left corner?
  bool draw_orientation;

  /// GL_FLAT or GL_SMOOTH shade model?
  bool smooth_model;

  /// Backface culling?
  bool backface_culling;

  /// Apply specular color after texturing?
  bool separate_specular_color;

  /// Point, light, fill mode
  int polygon_mode;

  // 0=No stereo / 1=VSplit
  int stereo_mode;

  /// Default material
  GLMaterial defaultmat;  

  public:
  GLRenderInstance();
  virtual ~GLRenderInstance() {}

  void setProjection(const mat4d& P);
  mat4d getProjection();
  void setViewTransformation(const mat4d& V, int eyeindex=0);
  mat4d getViewTransformation(int eyeindex=0);
  void setViewport(int x, int y, int width, int height);
  void getViewport(int& x, int& y, int& width, int& height) const;
  void paint(WorldObject& root);
  //void pick(int x, int y);   Rückgabe?

  protected:
  void drawScene(WorldObject& root, const mat4d& viewmat);
  bool drawNode(WorldObject& node, bool draw_blends);
  void applyLights(WorldObject& node);
  void drawWireCube(double lx, double ly, double lz);
  void drawCoordSystem();
};


}  // end of namespace

#endif
