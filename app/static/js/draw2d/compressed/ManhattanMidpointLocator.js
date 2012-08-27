/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ManhattanMidpointLocator=function(_12c5){ConnectionLocator.call(this,_12c5);};ManhattanMidpointLocator.prototype=new ConnectionLocator;ManhattanMidpointLocator.prototype.type="ManhattanMidpointLocator";ManhattanMidpointLocator.prototype.relocate=function(_12c6){var conn=this.getConnection();var p=new Point();var _12c9=conn.getPoints();var index=Math.floor((_12c9.getSize()-2)/2);if(_12c9.getSize()<=index+1){return;}var p1=_12c9.get(index);var p2=_12c9.get(index+1);p.x=(p2.x-p1.x)/2+p1.x+5;p.y=(p2.y-p1.y)/2+p1.y+5;_12c6.setPosition(p.x,p.y);};