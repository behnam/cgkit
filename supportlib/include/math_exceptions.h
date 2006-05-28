// Math exceptions

#ifndef MATH_EXCEPTIONS_H
#define MATH_EXCEPTIONS_H

namespace support3d {

/// Base class for all xmath exceptions.
class EXMathException {};

/// Index for vector or matrix component was out of range.
//class EIndexError : public EXMathException {};
/// Divide by zero.
class EDivideByZero : public EXMathException {};
/// Divide by zero for matrices.
class ESingularMatrix : public EXMathException {};

}  // end of namespace

#endif
