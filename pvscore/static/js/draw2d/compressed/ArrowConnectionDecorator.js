/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ArrowConnectionDecorator=function(_cd4,_cd5){ConnectionDecorator.call(this);if(_cd4===undefined||_cd4<1){this.lenght=15;}if(_cd5===undefined||_cd5<1){this.width=10;}};ArrowConnectionDecorator.prototype=new ConnectionDecorator();ArrowConnectionDecorator.prototype.type="ArrowConnectionDecorator";ArrowConnectionDecorator.prototype.paint=function(g){if(this.backgroundColor!==null){g.setColor(this.backgroundColor);g.fillPolygon([3,this.lenght,this.lenght,3],[0,(this.width/2),-(this.width/2),0]);}g.setColor(this.color);g.setStroke(1);g.drawPolygon([3,this.lenght,this.lenght,3],[0,(this.width/2),-(this.width/2),0]);};ArrowConnectionDecorator.prototype.setDimension=function(l,_cd8){this.width=w;this.lenght=l;};