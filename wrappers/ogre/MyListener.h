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

#ifndef __MyFrameListener_H__
#define __MyFrameListener_H__
 
#include "OgreEventListeners.h"
#include "OgreKeyEvent.h"
#include "Ogre.h"

#define MAX_KEYDOWNS 10
#define MAX_KEYUPS 10

using namespace Ogre;
//
//
// **********************************************************************
// * class MyListener							*
// *									*
// * Temporary class until ogre 1.0 is released				*
// **********************************************************************
//
class MyListener: public KeyListener
{
protected:

public:
	char *keyCharList;
	int *keyIntList;
	char *charRoot;
	int *intRoot;
	int *keyModifiersList;
	int *modifiersRoot;

	int pressedCount;

	char *keyCharListUp;
	int *keyIntListUp;
	char *charRootUp;
	int *intRootUp;
	int *keyModifiersListUp;
	int *modifiersRootUp;

	int releasedCount;

	MyListener() 
	{
		keyCharList = new char[MAX_KEYDOWNS];
		keyIntList = new int[MAX_KEYDOWNS];
		keyModifiersList = new int[MAX_KEYDOWNS];
		charRoot = keyCharList;
		intRoot = keyIntList;
		modifiersRoot = keyModifiersList;
		pressedCount = 0;

		keyCharListUp = new char[MAX_KEYUPS];
		keyIntListUp = new int[MAX_KEYUPS];
		keyModifiersListUp = new int[MAX_KEYUPS];
		charRootUp = keyCharListUp;
		intRootUp = keyIntListUp;
		modifiersRootUp = keyModifiersListUp;
		releasedCount = 0;
	};

	~MyListener() 
	{
		delete keyCharList;
		delete keyIntList;
		delete keyCharListUp;
		delete keyIntListUp;

		delete keyModifiersList;
		delete keyModifiersListUp;
	};

	void keyClicked(KeyEvent* e) 
	{

	}; 

	void keyPressed(KeyEvent* e) 
	{
		pressedCount++;

		//cout << "Key number: " << pressedCount << endl;

		if( pressedCount > MAX_KEYDOWNS )
		{
			//cout << "temporary queue full" << endl;
			return;
		}

		/*
		*keyCharList = e->getKeyChar();
		keyCharList++;
		*keyIntList = e->getKey();
		keyIntList++;
		*/

		keyCharList[ pressedCount-1 ] = e->getKeyChar();
		keyIntList[ pressedCount-1 ] = e->getKey();
		keyModifiersList[ pressedCount-1 ] = e->getModifiers();
		
	};

	void flush() 
	{
		keyCharList = charRoot;
		keyIntList = intRoot;	
		keyModifiersList = modifiersRoot;
		
		pressedCount = 0;
	};

	void flushUp() 
	{
		keyCharListUp = charRootUp;
		keyIntListUp = intRootUp;	
		keyModifiersListUp = modifiersRootUp;
		
		releasedCount = 0;
	};

	void keyReleased(KeyEvent* e) 
	{
		//cout << "Key pressed!" << endl;

		releasedCount++;

		//cout << "Key number: " << pressedCount << endl;

		if( releasedCount > MAX_KEYUPS )
		{
			//cout << "temporary queue full" << endl;
			return;
		}

		keyCharListUp[ releasedCount-1 ] = e->getKeyChar();
		keyIntListUp[ releasedCount-1 ] = e->getKey();
		keyModifiersListUp[ releasedCount-1 ] = e->getModifiers();
	};

protected:

};

#endif
