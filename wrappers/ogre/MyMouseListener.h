/*======================================================================
  Fast Ogre Rendering For CGKIT (FORC)
 Copyright (C) 2004 Ole Ciliox (ole@ira.uka.de)

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
 
#ifndef __MyMouseListener_H__
#define __MyMouseListener_H__

#include "OgreEventListeners.h"
#include "OgreKeyEvent.h"
#include "Ogre.h"
#include "OgreCore.h"

#define MAX_MOTIONS 10

using namespace Ogre;
using std::cout;
using std::endl;
//
//
// **********************************************************************
// * class MyMouseListener						*
// *									*
// * Temporary class until ogre 1.0 is released				*
// **********************************************************************
//
class MyMouseListener: public MouseMotionListener
{
protected:

public:
	float moveX;
	float moveY;
	float moveRelX;
	float moveRelY;

	bool motion;
	bool lMB;
	bool mMB;
	bool rMB;

	MyMouseListener() 
	{
		moveX = 0.0; moveY = 0.0; moveRelX = 0.0; moveRelY = 0.0;
		motion = false;
		lMB = false;
		mMB = false;
		rMB = false;
	};

	~MyMouseListener()
	{

	};

	// MODIFIERS LEGENDE ;;;;;;;;;;;;;;;;;;;;
	// ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	// 16 : linker Mausknopf
	// 32 : rechter Mausknopf
	// 64 : mittlerer Mausknopf
	// 1  : shift zusätzlich
	// 2  : strg zuätzlich
	// 4  : meta zuätzlich (?)
	// 8  : alt zusätzlich
	// MODIFIERS : gesamtwert
	// ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	// ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	void mouseMoved(MouseEvent *e)
	{
		motion = true;
		//snapshot = e;
		//cout << "Mouse Moved!" << endl;

		//cout << "true values: " << e->getX() << " " << e->getY() << " " << e->getRelX() << " " << e->getRelY() << endl;

		moveX = (float)(e->getX());
		moveY = (float)(e->getY());
		moveRelX = (float)(e->getRelX());
		moveRelY = (float)(e->getRelY());


		lMB = (e->getModifiers() & InputEvent::BUTTON0_MASK) != 0;
		mMB = (e->getModifiers() & InputEvent::BUTTON2_MASK) != 0;
		rMB = (e->getModifiers() & InputEvent::BUTTON1_MASK) != 0;

		//e->consume();

	};

	void mouseDragged(MouseEvent *e)
	{
		motion = true;
		//snapshot = e;
		//cout << "Mouse Dragged!" << endl;

		//cout << "MODIFIERS: " << e->getModifiers() << endl;

		moveX = (float)(e->getX());
		moveY = (float)(e->getY());
		moveRelX = (float)(e->getRelX());
		moveRelY = (float)(e->getRelY());
		
		lMB = (e->getModifiers() & InputEvent::BUTTON0_MASK) != 0;
		mMB = (e->getModifiers() & InputEvent::BUTTON2_MASK) != 0;
		rMB = (e->getModifiers() & InputEvent::BUTTON1_MASK) != 0;
	};

	void mouseDragMoved(MouseEvent *e)
	{
		motion = true;
		//snapshot = e;
		//cout << "Mouse DragMoved!" << endl;

		//cout << "MODIFIERS: " << e->getModifiers() << endl;

		moveX = (float)(e->getX());
		moveY = (float)(e->getY());
		moveRelX = (float)(e->getRelX());
		moveRelY = (float)(e->getRelY());
		
		lMB = (e->getModifiers() & InputEvent::BUTTON0_MASK) != 0;
		mMB = (e->getModifiers() & InputEvent::BUTTON2_MASK) != 0;
		rMB = (e->getModifiers() & InputEvent::BUTTON1_MASK) != 0;
	};

	

	void flush() 
	{

	};
};
	
#endif
