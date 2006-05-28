/*
  null_deleter

  (for boost::shared_ptr)

  (C) 2004 Matthias Baas (baas@ira.uka.de)
 */

#ifndef NULLDELETER_H
#define NULLDELETER_H

struct null_deleter
{
  void operator()(void const *) const {}
};

#endif
