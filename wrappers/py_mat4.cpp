/*
  mat4 wrapper
 */

#include <sstream>
#include <boost/python.hpp>
#include "mat4.h"
#include "py_exceptions.h"

//#include <iostream.h>

using namespace boost::python;
using namespace support3d;

//////////////////////////////////////////////////////////////////////
// The following functions are used as class methods for the Python
// version of mat4.
// The C++ mat4 either doesn't have those methods or they have to
// be modified for Python.
//////////////////////////////////////////////////////////////////////

// toList() method (with no argument)
object toList0(const mat4d* self)
{
  list res;
  double array[16];
  self->toList(array);
  for(int i=0; i<16; i++)
    res.append(array[i]);
  return res;
}

// toList() method (with 1 argument)
object toList1(const mat4d* self, bool rowmajor)
{
  list res;
  double array[16];
  self->toList(array, rowmajor);
  for(int i=0; i<16; i++)
    res.append(array[i]);
  return res;
}

// identity() method
mat4d identity(mat4d* self)
{
  return mat4d(1);
}

// translation() method
mat4d translation(mat4d* self, const vec3d& t)
{
  mat4d res;
  res.setTranslation(t);
  return res;
}

// scaling() method
mat4d scaling(mat4d* self, const vec3d& s)
{
  mat4d res;
  res.setScaling(s);
  return res;
}

// rotation() method
mat4d rotation(mat4d* self, double angle, const vec3d& axis)
{
  mat4d res;
  res.setRotation(angle, axis);
  return res;
}

// orthographic() method
mat4d orthographic(mat4d* self, double left, double right, double bottom, double top, double nearval, double farval)
{
  mat4d res;
  res.setOrthographic(left, right, bottom, top, nearval, farval);
  return res;
}

// frustum() method
mat4d frustum(mat4d* self, double left, double right, double bottom, double top, double nearval, double farval)
{
  mat4d res;
  res.setFrustum(left, right, bottom, top, nearval, farval);
  return res;
}

// perspective() method
mat4d perspective(mat4d* self, double fovy, double aspect, double nearval, double farval)
{
  mat4d res;
  res.setPerspective(fovy, aspect, nearval, farval);
  return res;
}

// lookAt() method 
mat4d lookAt(mat4d* self, const vec3d& pos, const vec3d& target, const vec3d& up=vec3d(0,0,1))
{
  mat4d res;
  res.setLookAt(pos, target, up);
  return res;
}
BOOST_PYTHON_FUNCTION_OVERLOADS(lookAt_overloads, lookAt, 3, 4)


// decompose() method
// Returns a tuple (t, rot, scale)
object decompose(mat4d* self)
{
  mat4d rot;
  vec3d t, scale;
  self->decompose(t, rot, scale);
  return make_tuple(t, rot, scale);
}

boost::python::str repr(mat4d* self)
{
  std::ostringstream s;
  s<<*self;
  return boost::python::str(s.str());
}

mat4d __pos__(mat4d* self)
{
  return *self;
}

int __len__(mat4d* self)
{
  return 4;
}

vec4d __getitem__(mat4d* self, int idx)
{
  if (idx<0 || idx>3)
    throw EPyIndexError("index out of range");

  return self->getColumn(idx);
}

double __getitem_tup__(mat4d* self, tuple tup)
{
  int len = extract<int>(tup.attr("__len__")());
  if (len!=2)
  {
    throw EValueError("index tuple must be a 2-tuple");
  }
  int i = extract<int>(tup[0]);
  int j = extract<int>(tup[1]);
  if (i<0 || i>3 || j<0 || j>3)
      throw EIndexError();

  return self->at(i,j);
}

void __setitem__(mat4d* self, int idx, const vec4d& val)
{
  if (idx<0 || idx>3)
    throw EPyIndexError("index out of range");

  self->setColumn(idx, val);
}

void __setitem_tup__(mat4d* self, tuple tup, double val)
{
  int len = extract<int>(tup.attr("__len__")());
  if (len!=2)
  {
    throw EValueError("index tuple must be a 2-tuple");
  }
  int i = extract<int>(tup[0]);
  int j = extract<int>(tup[1]);
  if (i<0 || i>3 || j<0 || j>3)
      throw EIndexError();

  self->at(i,j) = val;
}

// pickle & copy support
struct mat4_pickle_suite : boost::python::pickle_suite
{
  // Return the arguments that will be passed to the constructor
  // (i.e. return a flattened matrix in row-major order)
  static tuple getinitargs(mat4d const& self)
  {
    return tuple(toList1(&self, true));
  }
};


//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

void class_mat4()
{
  vec4d (mat4d::*getRow)(short i) const = &mat4d::getRow;
  mat4d& (mat4d::*setRow)(short i, const vec4d& r) = &mat4d::setRow;
  vec4d (mat4d::*getColumn)(short i) const = &mat4d::getColumn;
  mat4d& (mat4d::*setColumn)(short i, const vec4d& c) = &mat4d::setColumn;
  vec4d (mat4d::*getDiag)() const = &mat4d::getDiag;
  mat4d& (mat4d::*setDiag)(const vec4d& d) = &mat4d::setDiag;
  mat4d (mat4d::*transpose)() const = &mat4d::transpose;
  mat4d (mat4d::*inverse)() const = &mat4d::inverse;
  mat4d (mat4d::*ortho)() const = &mat4d::ortho;
  mat3d (mat4d::*getMat3)() const = &mat4d::getMat3;

  class_<mat4d>("mat4")
    .def(init<double>())
    /*    .def(init<double,double,double,double,
	      double,double,double,double,
              double,double,double,double,
              double,double,double,double>())*/
    .def(init<const mat4d&>())
    .def(self_ns::str(self))
    .def("__repr__", &repr)
    .def("__pos__", __pos__)
    .def("__len__", __len__)
    .def("__getitem__", __getitem__)
    .def("__getitem__", __getitem_tup__)
    .def("__setitem__", __setitem__)
    .def("__setitem__", __setitem_tup__)
    .def(self+=self)
    .def(self-=self)
    .def(self*=double())
    .def(self*=self)
    .def(self/=double())
    .def(self%=double())
    .def(self%=self)
    .def(self+self)
    .def(self-self)
    .def(-self)
    .def(self*other<vec4d>())
    .def(other<vec4d>()*self)
    .def(self*other<vec3d>())
    .def(other<vec3d>()*self)
    .def(double()*self)
    .def(self*double())
    .def(self*self)
    .def(self/double())
    .def(self%double())
    .def(self%self)
    .def(self==self)
    .def(self!=self)
    .def("getColumn", getColumn, arg("index"))
    .def("setColumn", setColumn, return_self<>(), (arg("index"), arg("value")))
    .def("getRow", getRow, arg("index"))
    .def("setRow", setRow, return_self<>(), (arg("index"), arg("value")))
    .def("getDiag", getDiag)
    .def("setDiag", setDiag, return_self<>(), arg("value"))
    .def("toList", &toList0)
    .def("toList", &toList1, arg("rowmajor"))
    .def("identity", &identity)
    .def("translation", &translation, arg("t"))
    .def("scaling", &scaling, arg("s"))
    .def("rotation", &rotation, (arg("angle"), arg("axis")))
    .def("orthographic", &orthographic, (arg("left"), arg("right"), arg("bottom"), arg("top"), arg("near"), arg("far")))
    .def("frustum", &frustum, (arg("left"), arg("right"), arg("bottom"), arg("top"), arg("near"), arg("far")))
    .def("perspective", &perspective, (arg("fovy"), arg("aspect"), arg("near"), arg("far")))
    .def("lookAt", &lookAt, lookAt_overloads((arg("pos"), arg("target"), arg("up"))))
    //    .def("lookAt", &lookAt3)
    .def("transpose", transpose)
    .def("determinant", &mat4d::determinant)
    .def("inverse", inverse)
    .def("translate", &mat4d::translate, return_internal_reference<>(), arg("t"))
    .def("scale", &mat4d::scale, return_internal_reference<>(), arg("s"))
    .def("rotate", &mat4d::rotate, return_internal_reference<>(), (arg("angle"), arg("axis")))
    .def("ortho", ortho)
    .def("decompose", &decompose)
    .def("getMat3", getMat3)
    .def("setMat3", &mat4d::setMat3, return_internal_reference<>(), arg("m3"))
    .def_pickle(mat4_pickle_suite())
  ;
}

