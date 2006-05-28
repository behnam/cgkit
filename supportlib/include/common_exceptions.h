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

#ifndef COMMON_EXCEPTIONS_H
#define COMMON_EXCEPTIONS_H

#include <exception>
#include <string>

namespace support3d {

////////////////////////////////////////////////////////////////

/**
  Exception: RuntimeError.
 */
class ERuntimeError : public std::exception
{
  public:
  std::string msg;

  public:
  ERuntimeError(std::string amsg) : msg(amsg) {}
  ~ERuntimeError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: IOError.
 */
class EIOError : public std::exception
{
  public:
  std::string msg;

  public:
  EIOError(std::string amsg) : msg(amsg) {}
  ~EIOError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: Out of memory.
 */
class EMemoryError : public std::exception
{
  public:
  std::string msg;

  public:
  EMemoryError() {}
  EMemoryError(std::string amsg) : msg(amsg) {}
  ~EMemoryError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    if (msg=="")
      return "Out of memory.";
    else
      return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: Index out of range.
 */
class EIndexError : public std::exception
{
  public:
  std::string msg;

  public:
  EIndexError() {}
  EIndexError(std::string amsg) : msg(amsg) {}
  ~EIndexError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    if (msg=="")
      return "Index out of range.";
    else
      return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: Invalid value.
 */
class EValueError : public std::exception
{
  public:
  std::string msg;

  public:
  EValueError(std::string amsg) : msg(amsg) {}
  ~EValueError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};


////////////////////////////////////////////////////////////////

/**
  Exception: Divide by zero.
 */
class EZeroDivisionError : public std::exception
{
  public:
  std::string msg;

  public:
  EZeroDivisionError(std::string amsg="") : msg(amsg) 
  {
    if (msg=="")
    {
      msg = "Division by zero";
    }
  }
  ~EZeroDivisionError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: Key error.
 */
class EKeyError : public std::exception
{
  public:
  std::string msg;

  public:
  EKeyError(std::string amsg) : msg(amsg) {}
  ~EKeyError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};

////////////////////////////////////////////////////////////////

/**
  Exception: Not implemented
 */
class ENotImplementedError : public std::exception
{
  public:
  std::string msg;

  public:
  ENotImplementedError(std::string amsg) : msg(amsg) {}
  ~ENotImplementedError() throw() {}

  /// Return exception message.
  const char* what() const throw()
  {
    return msg.c_str();
  }
};


}  // end of namespace

#endif
