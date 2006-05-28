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

#ifndef GLMATERIAL_H
#define GLMATERIAL_H

/** \file glmaterial.h
 Contains the GLMaterial class.
 */

#include <vector>
#include <string>
#include "component.h"
#include "material.h"
#include "vec3.h"
#include "vec4.h"
#include "mat4.h"
#include "slot.h"
#include <boost/shared_ptr.hpp>


namespace support3d {

/**
  OpenGL texture object.

  This class represents an OpenGL texture and its parameters. 
  A %GLTexture object is used in combination with a GLMaterial 
  object where it has to be assigned to the \a texture attribute.

  This class cannot be used directly as it doesn't include a method
  for retrieving the actual texture data. This has to be done in
  a derived class in the loadTexData() method. This method either
  loads an image from disk or creates an image procedurally.

  \see GLMaterial
 */
class GLTexture
{
  public:
  /// Environment map flag
  bool environment_map;

  /// Mip map flag
  bool mipmap;

  /// Texture mode (GL_MODULATE, GL_DECAL, GL_BLEND, GL_REPLACE)
  int mode;

  /// Magnification filter (GL_NEAREST, GL_LINEAR)
  int mag_filter;

  /// Minification filter (GL_NEAREST, GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, ...)
  int min_filter;

  // Texture wrap in s direction (GL_CLAMP, GL_CLAMP_TO_EDGE, GL_REPEAT)
  int wrap_s;

  // Texture wrap in t direction (GL_CLAMP, GL_CLAMP_TO_EDGE, GL_REPEAT)
  int wrap_t;

  /// Internal texture format (GL_RGB, GL_RGBA, ...)
  int internalformat;

  /// Color for the texture blending
  vec4d texenvcolor;

  /// Texture coordinate transformation matrix
  mat4d transform;

  protected:
  /// Image file name
  string imagename;

  /// OpenGL texture name
  int texname;

  /// Update flags
  int flags;

  // Flags
  enum { IMAGE_NAME = 0x01 }; 

  public:
  GLTexture();
  virtual ~GLTexture();

  string getImageName();
  void setImageName(string name);

  void applyGL();

  // Initialization (alloc texture object)
  void allocGL();
  void releaseGL();
  void texData(int w, int h, int format, int type, char* data);

  /**
    Provide the texture data.

    This method has to be implemented in a derived class.
    The method must pass the texture data by calling texData().
   */
  virtual void loadTexData() {}
};

/**
  An OpenGL shader class.

  This class stores the file name of a shader and its uniform parameters
  which are stored in the slots.

  \see GLMaterial
 */
class GLShader : public Component
{
  public:
  enum ShaderType { VERTEX, FRAGMENT };

  /// Shader source file
  std::string filename;

  private:

  /// Shader type.
  ShaderType type;

  public:
  GLShader(ShaderType atype, std::string afilename=std::string()) : filename(afilename), type(atype) {}

  ShaderType getType() const { return type; }
};

/**
  An OpenGL material class.

  This material has the same parameters that the OpenGL material model
  has.

  \see GLTexture, GLShader
 */
class GLMaterial : public Material
{
  public:
  /// Ambient color 
  Slot<vec4d> ambient;
  /// Diffuse color 
  Slot<vec4d> diffuse;
  /// Specular color 
  Slot<vec4d> specular;
  /// Shininess color 
  Slot<double> shininess;
  /// Emission color 
  Slot<vec4d> emission;

  int blend_sfactor;
  int blend_dfactor;

  protected:
  /** A list of GLTexture objects.
   */
  std::vector<boost::shared_ptr<GLTexture> > textures;
  //  boost::shared_ptr<GLTexture> texture;

  /** A list of GLShader objects that make up a vertex shader.
      If this list is empty, no vertex shader is used. The shaders in 
      this list may only be of type VERTEX. An item may also contain an
      empty pointer in which case it should be ignored.
   */
  std::vector<boost::shared_ptr<GLShader> > vertex_shader;
  
  /** A list of GLShader objects that make up a fragment shader.
      If this list is empty, no fragment shader is used. The shaders in
      this list may only be of type FRAGMENT. An item may also contain an
      empty pointer in which case it should be ignored.
  */
  std::vector<boost::shared_ptr<GLShader> > fragment_shader;

  public:
  GLMaterial();
  GLMaterial(string aname, double adensity=1.0);
  virtual ~GLMaterial();
  
  virtual void applyGL();
  bool usesBlending();

  int getNumTextures() const;
  void setNumTextures(int num);
  boost::shared_ptr<GLTexture> getTexture(int idx=0) const;
  void setTexture(boost::shared_ptr<GLTexture> atexture, int idx=0);

  int getNumVertexShaders() const;
  void setNumVertexShaders(int num);
  boost::shared_ptr<GLShader> getVertexShader(int idx=0) const;
  void setVertexShader(boost::shared_ptr<GLShader> ashader, int idx=0);

  int getNumFragmentShaders() const;
  void setNumFragmentShaders(int num);
  boost::shared_ptr<GLShader> getFragmentShader(int idx=0) const;
  void setFragmentShader(boost::shared_ptr<GLShader> ashader, int idx=0);
  
};

}  // end of namespace

#endif
