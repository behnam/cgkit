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

#ifndef __MyMouseBListener_H__ 
#define __MyMouseBListener_H__

#include "OgreEventListeners.h"
#include "OgreKeyEvent.h"
#include "Ogre.h"
#include "OgreCore.h"

#define MAX_MOUSEBUTTONEVENTS 10



// bis jetzt unbuffered: immer nur letzter klick wird beachtet
// TODO :: PUFFERN
// TODO :: An CGKIT übergeben (wrapper funktion schreiben)

using namespace Ogre;
//
//
// **********************************************************************
// * class MyMouseButtonListener					*
// *									*
// * Temporary class until ogre 1.0 is released				*
// **********************************************************************
//
class MyMouseButtonListener: public MouseListener
{
protected:

public:
	int *mouseButtonList; // 0 LMB, 1 MMB, 3 RMB
	float *mouseXList;
	float *mouseYList;
	float *mousedXList;
	float *mousedYList;
	int *eventTypeList; // 0 PRESS, 1 RELEASE

	int *mouseButtonRoot;
	float *mouseYRoot;
	float *mousedXRoot;
	float *mousedYRoot;
	int *eventTypeRoot;

	int mouseCount;

	MyMouseButtonListener() 
	{
		mouseButtonList = new int[MAX_MOUSEBUTTONEVENTS];
		mouseXList = new float[MAX_MOUSEBUTTONEVENTS];
		mouseYList = new float[MAX_MOUSEBUTTONEVENTS];
		mousedXList = new float[MAX_MOUSEBUTTONEVENTS];
		mousedYList = new float[MAX_MOUSEBUTTONEVENTS];	
		eventTypeList = new int[MAX_MOUSEBUTTONEVENTS];	
		
		mouseButtonRoot = mouseButtonList;
		mouseXList = mouseXList;
		mouseYRoot = mouseYList;
		mousedXRoot = mousedXList;
		mousedYRoot = mousedYList;
		eventTypeRoot = eventTypeList;
	
		mouseCount = 0;
	};

	~MyMouseButtonListener() 
	{
		delete mouseButtonList;
		delete mouseXList;
		delete mouseYList;
		delete mousedXList;
		delete mousedYList;		
		delete eventTypeList;
	};

	void mouseReleased(MouseEvent *e) // Type = 1
	{
	
		//cout << "Mouse released!" << endl;

		mouseCount++;

		if( mouseCount > MAX_MOUSEBUTTONEVENTS )
		{
			//cout << "temporary queue full" << endl;
			return;
		}

		mouseButtonList[ mouseCount-1 ] = e->getButtonID();
		mouseXList[ mouseCount-1 ] = e->getX();
		mouseYList[ mouseCount-1 ] = e->getY();
		mousedXList[ mouseCount-1 ] = e->getRelX();
		mousedYList[ mouseCount-1 ] = e->getRelY();
		eventTypeList[ mouseCount-1 ] = 1;

	};

	void mousePressed(MouseEvent *e) // Type = 0
	{


		//cout << "Mouse preleased!" << endl;

		mouseCount++;

		if( mouseCount > MAX_MOUSEBUTTONEVENTS )
		{
			//cout << "temporary queue full" << endl;
			return;
		}

		mouseButtonList[ mouseCount-1 ] = e->getButtonID();

		//cout << "###################" << e->getButtonID() << endl;

		mouseXList[ mouseCount-1 ] = e->getX();
		mouseYList[ mouseCount-1 ] = e->getY();
		mousedXList[ mouseCount-1 ] = e->getRelX();
		mousedYList[ mouseCount-1 ] = e->getRelY();
		eventTypeList[ mouseCount-1 ] = 0;

	};

	void mouseClicked(MouseEvent *e)  
	{

	};

	void mouseExited(MouseEvent *e)
	{

	};

	void mouseEntered(MouseEvent *e)
	{

	};

	void flush() 
	{
		mouseCount = 0;

		mouseButtonList = mouseButtonRoot;
		mouseXList = mouseXList;
		mouseYList = mouseYRoot;
		mousedXList = mousedXRoot;
		mousedYList = mousedYRoot;
		eventTypeList = eventTypeRoot;
	};
};
	
#endif
