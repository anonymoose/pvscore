/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ChopboxConnectionAnchor=function(_6cf){ConnectionAnchor.call(this,_6cf);};ChopboxConnectionAnchor.prototype=new ConnectionAnchor();ChopboxConnectionAnchor.prototype.type="ChopboxConnectionAnchor";ChopboxConnectionAnchor.prototype.getLocation=function(_6d0){var r=new Dimension();r.setBounds(this.getBox());r.translate(-1,-1);r.resize(1,1);var _6d2=r.x+r.w/2;var _6d3=r.y+r.h/2;if(r.isEmpty()||(_6d0.x==_6d2&&_6d0.y==_6d3)){return new Point(_6d2,_6d3);}var dx=_6d0.x-_6d2;var dy=_6d0.y-_6d3;var _6d6=0.5/Math.max(Math.abs(dx)/r.w,Math.abs(dy)/r.h);dx*=_6d6;dy*=_6d6;_6d2+=dx;_6d3+=dy;return new Point(Math.round(_6d2),Math.round(_6d3));};ChopboxConnectionAnchor.prototype.getBox=function(){return this.getOwner().getParent().getBounds();};ChopboxConnectionAnchor.prototype.getReferencePoint=function(){return this.getBox().getCenter();};