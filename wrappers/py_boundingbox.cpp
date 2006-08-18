/*
  BoundingBox wrapper
 */

#include <sstream>
#include <boost/python.hpp>
#include "boundingbox.h"

using namespace boost::python;
using namespace support3d;

// wrapper for the getBounds() method that returns the bounds as a 2-tuple
object getBounds(BoundingBox* self)
{
  vec3d bmin, bmax;
  self->getBounds(bmin, bmax);
  return make_tuple(bmin, bmax);
}

// wrapper for the transform() method so that the result is properly returned
BoundingBox transform(BoundingBox* self, const mat4d& M)
{
  BoundingBox bb;
  self->transform(M, bb);
  return bb;
}

boost::python::str repr(BoundingBox* self)
{
  std::ostringstream s;
  s<<*self;
  return boost::python::str(s.str());
}

// BoundingBox
void class_BoundingBox()
{

  class_<BoundingBox>("BoundingBox", "Axis aligned bounding box.", init<>())
    .def(init<const vec3d&, const vec3d&>())
    .def(self_ns::str(self))
    .def("__repr__", &repr)

    .def("clear", &BoundingBox::clear, 
	 "Make the bounding box empty.")

    .def("isEmpty", &BoundingBox::isEmpty, 
	 "isEmpty() -> Bool\n\n"
	 "Return True if the bounding box is empty.")

    .def("getBounds", &getBounds,
	 "getBounds() -> (bmin, bmax)\n\n"
	 "Return the minimum and maximum bound. The bounds are returned as\n"
	 "vec3 objects.")

    .def("setBounds", &BoundingBox::setBounds, (arg("b1"), arg("b2")),
	 "setBounds(b1, b2)\n\n"
	 "Set new bounds for the bounding box. The rectangle given\n"
	 "by b1 and b2 defines the new bounding box.")

    .def("addPoint", &BoundingBox::addPoint, arg("p"),
	 "addPoint(p)\n\n"
	 "Enlarge the bounding box so that the point p is enclosed in the box.")

    .def("addBoundingBox", &BoundingBox::addBoundingBox, arg("bb"),
	 "addBoundingBox(bb)\n\n"
	 "Enlarge the bounding box so that the bounding box bb is enclosed in\n"
	 "the box.")

    .def("transform", &transform, arg("M"),
	 "transform(M) -> BoundingBox\n\n"
	 "Returns a transformed bounding box. The transformation is given by M\n"
	 "which must be a mat4. The result will still be axis aligned, so the\n"
	 "volume will not be preserved.")
  ;
}
