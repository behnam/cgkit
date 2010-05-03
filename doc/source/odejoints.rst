.. % ODE joints


ODE joints --- Joint classes for the ODEDynamics component
==========================================================

See the ODE manual (chapter  `Joint Types and Functions <http://opende.sourceforge.net/wiki/index.php/Manual_%28Joint_Types_and_Functions>`_) for a detailed description of joint types.

.. % ----------------------------------------------------------------------


:class:`ODEBallJoint` --- Ball and socket joint
-----------------------------------------------


.. class:: ODEBallJoint(name = "ODEBallJoint",  body1 = None,  body2 = None )

.. % ----------------------------------------------------------------------


:class:`ODEHingeJoint` --- Hinge joint
--------------------------------------


.. class:: ODEHingeJoint(name = "ODEHingeJoint",  body1 = None,  body2 = None )

.. % ----------------------------------------------------------------------


:class:`ODESliderJoint` --- Slider joint
----------------------------------------


.. class:: ODESliderJoint(name = "ODESliderJoint",  body1 = None,  body2 = None )

.. % ----------------------------------------------------------------------


:class:`ODEHinge2Joint` --- Hinge-2 joint
-----------------------------------------


.. class:: ODEHinge2Joint(name = "ODEHinge2Joint",  body1 = None,  body2 = None )

.. % ----------------------------------------------------------------------


:class:`ODEUniversalJoint` --- Universal joint
----------------------------------------------


.. class:: ODEUniversalJoint(name = "ODEUniversalJoint",  body1 = None,  body2 = None )


:class:`ODEFixedJoint` --- Fixed joint
--------------------------------------

.. class:: ODEFixedJoint(name = "ODEFixedJoint",  body1 = None,  body2 = None )

   Fixed Joint: Glues two bodies together.
   
   It is not recommended by ODE manual, but is useful when a solid body 
   has different contact properties on different sides.

