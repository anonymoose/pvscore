/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ConnectionAnchor=function(_5c2){this.owner=_5c2;};ConnectionAnchor.prototype.type="ConnectionAnchor";ConnectionAnchor.prototype.getLocation=function(_5c3){return this.getReferencePoint();};ConnectionAnchor.prototype.getOwner=function(){return this.owner;};ConnectionAnchor.prototype.setOwner=function(_5c4){this.owner=_5c4;};ConnectionAnchor.prototype.getBox=function(){return this.getOwner().getAbsoluteBounds();};ConnectionAnchor.prototype.getReferencePoint=function(){if(this.getOwner()===null){return null;}else{return this.getOwner().getAbsolutePosition();}};