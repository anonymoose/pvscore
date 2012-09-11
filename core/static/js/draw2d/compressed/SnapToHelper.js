/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

SnapToHelper=function(_14a3){this.workflow=_14a3;};SnapToHelper.NORTH=1;SnapToHelper.SOUTH=4;SnapToHelper.WEST=8;SnapToHelper.EAST=16;SnapToHelper.CENTER=32;SnapToHelper.NORTH_EAST=SnapToHelper.NORTH|SnapToHelper.EAST;SnapToHelper.NORTH_WEST=SnapToHelper.NORTH|SnapToHelper.WEST;SnapToHelper.SOUTH_EAST=SnapToHelper.SOUTH|SnapToHelper.EAST;SnapToHelper.SOUTH_WEST=SnapToHelper.SOUTH|SnapToHelper.WEST;SnapToHelper.NORTH_SOUTH=SnapToHelper.NORTH|SnapToHelper.SOUTH;SnapToHelper.EAST_WEST=SnapToHelper.EAST|SnapToHelper.WEST;SnapToHelper.NSEW=SnapToHelper.NORTH_SOUTH|SnapToHelper.EAST_WEST;SnapToHelper.prototype.snapPoint=function(_14a4,_14a5,_14a6){return _14a5;};SnapToHelper.prototype.snapRectangle=function(_14a7,_14a8){return _14a7;};SnapToHelper.prototype.onSetDocumentDirty=function(){};