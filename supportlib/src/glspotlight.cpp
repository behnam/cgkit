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

#include "glspotlight.h"

#include "vec3.h"

#ifdef WIN32
#include <windows.h>
#endif

#if defined(__APPLE__) || defined(MACOSX)
#include "OpenGL/gl.h"
#else
#include "GL/gl.h"
#endif

namespace support3d {

GLSpotLight::GLSpotLight()
: LightSource(),
  ambient(vec3d(0,0,0), 0),
  diffuse(vec3d(1,1,1), 0),
  specular(vec3d(1,1,1), 0),
  constant_attenuation(1.0, 0),
  linear_attenuation(0.0, 0),
  quadratic_attenuation(0.0, 0),
  exponent(0.0, 0),
  cutoff(45.0, 0)
{
  addSlot("ambient", ambient);
  addSlot("diffuse", diffuse);
  addSlot("specular", specular);
  addSlot("constant_attenuation", constant_attenuation);
  addSlot("linear_attenuation", linear_attenuation);
  addSlot("quadratic_attenuation", quadratic_attenuation);
  addSlot("exponent", exponent);
  addSlot("cutoff", cutoff);
}

GLSpotLight::GLSpotLight(string aname)
: LightSource(aname),
  ambient(vec3d(0,0,0), 0),
  diffuse(vec3d(1,1,1), 0),
  specular(vec3d(1,1,1), 0),
  constant_attenuation(1.0, 0),
  linear_attenuation(0.0, 0),
  quadratic_attenuation(0.0, 0),
  exponent(0.0, 0),
  cutoff(45.0, 0)
{
  addSlot("ambient", ambient);
  addSlot("diffuse", diffuse);
  addSlot("specular", specular);
  addSlot("constant_attenuation", constant_attenuation);
  addSlot("linear_attenuation", linear_attenuation);
  addSlot("quadratic_attenuation", quadratic_attenuation);
  addSlot("exponent", exponent);
  addSlot("cutoff", cutoff);
}

/**
  Apply the light using OpenGL commands.

  This method does not enable the light source (you have to call glEnable(GL_LIGHTn)
  yourself).

  \pre The transformation of the light was already applied
 */
void GLSpotLight::applyGL(int idx)
{
  GLfloat c[4] = {0,0,0,1};
  int glidx = GL_LIGHT0 + idx;
  double I = intensity.getValue();

  // Cutoff = 180 => PointLight
  glLightf(glidx, GL_SPOT_CUTOFF, GLfloat(cutoff.getValue()));
  glLightf(glidx, GL_SPOT_EXPONENT, GLfloat(exponent.getValue()));
    
  // Position is always at the origin (which is the local origin)
  glLightfv(glidx, GL_POSITION, c);

  // Direction is always along positive local Z axis
  c[2]=1;
  glLightfv(glidx, GL_SPOT_DIRECTION, c);

  const vec3d& ac = ambient.getValue();
  c[0] = GLfloat(I*ac.x);
  c[1] = GLfloat(I*ac.y);
  c[2] = GLfloat(I*ac.z);
  glLightfv(glidx, GL_AMBIENT, c);

  const vec3d& dc = diffuse.getValue();
  c[0] = GLfloat(I*dc.x);
  c[1] = GLfloat(I*dc.y);
  c[2] = GLfloat(I*dc.z);
  glLightfv(glidx, GL_DIFFUSE, c);

  const vec3d& sc = specular.getValue();
  c[0] = GLfloat(sc.x);
  c[1] = GLfloat(sc.y);
  c[2] = GLfloat(sc.z);
  glLightfv(glidx, GL_SPECULAR, c);

  glLightf(glidx, GL_CONSTANT_ATTENUATION, GLfloat(constant_attenuation.getValue()));
  glLightf(glidx, GL_LINEAR_ATTENUATION, GLfloat(linear_attenuation.getValue()));
  glLightf(glidx, GL_QUADRATIC_ATTENUATION, GLfloat(quadratic_attenuation.getValue()));
}


}  // end of namespace
