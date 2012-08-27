/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Point=function(x,y){this.x=x;this.y=y;};Point.prototype.type="Point";Point.prototype.getX=function(){return this.x;};Point.prototype.getY=function(){return this.y;};Point.prototype.getPosition=function(p){var dx=p.x-this.x;var dy=p.y-this.y;if(Math.abs(dx)>Math.abs(dy)){if(dx<0){return PositionConstants.WEST;}return PositionConstants.EAST;}if(dy<0){return PositionConstants.NORTH;}return PositionConstants.SOUTH;};Point.prototype.equals=function(o){return this.x==o.x&&this.y==o.y;};Point.prototype.getDistance=function(_6e2){return Math.sqrt((this.x-_6e2.x)*(this.x-_6e2.x)+(this.y-_6e2.y)*(this.y-_6e2.y));};Point.prototype.getTranslated=function(_6e3){return new Point(this.x+_6e3.x,this.y+_6e3.y);};Point.prototype.getPersistentAttributes=function(){return {x:this.x,y:this.y};};