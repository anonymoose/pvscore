/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Graphics=function(_4a1,_4a2,_4a3){this.jsGraphics=_4a1;this.xt=_4a3.x;this.yt=_4a3.y;this.radian=_4a2*Math.PI/180;this.sinRadian=Math.sin(this.radian);this.cosRadian=Math.cos(this.radian);};Graphics.prototype.setStroke=function(x){this.jsGraphics.setStroke(x);};Graphics.prototype.drawLine=function(x1,y1,x2,y2){var _x1=this.xt+x1*this.cosRadian-y1*this.sinRadian;var _y1=this.yt+x1*this.sinRadian+y1*this.cosRadian;var _x2=this.xt+x2*this.cosRadian-y2*this.sinRadian;var _y2=this.yt+x2*this.sinRadian+y2*this.cosRadian;this.jsGraphics.drawLine(_x1,_y1,_x2,_y2);};Graphics.prototype.fillRect=function(x,y,w,h){var x1=this.xt+x*this.cosRadian-y*this.sinRadian;var y1=this.yt+x*this.sinRadian+y*this.cosRadian;var x2=this.xt+(x+w)*this.cosRadian-y*this.sinRadian;var y2=this.yt+(x+w)*this.sinRadian+y*this.cosRadian;var x3=this.xt+(x+w)*this.cosRadian-(y+h)*this.sinRadian;var y3=this.yt+(x+w)*this.sinRadian+(y+h)*this.cosRadian;var x4=this.xt+x*this.cosRadian-(y+h)*this.sinRadian;var y4=this.yt+x*this.sinRadian+(y+h)*this.cosRadian;this.jsGraphics.fillPolygon([x1,x2,x3,x4],[y1,y2,y3,y4]);};Graphics.prototype.fillPolygon=function(_4b9,_4ba){var rotX=[];var rotY=[];for(var i=0;i<_4b9.length;i++){rotX[i]=this.xt+_4b9[i]*this.cosRadian-_4ba[i]*this.sinRadian;rotY[i]=this.yt+_4b9[i]*this.sinRadian+_4ba[i]*this.cosRadian;}this.jsGraphics.fillPolygon(rotX,rotY);};Graphics.prototype.setColor=function(_4be){this.jsGraphics.setColor(_4be.getHTMLStyle());};Graphics.prototype.drawPolygon=function(_4bf,_4c0){var rotX=[];var rotY=[];for(var i=0;i<_4bf.length;i++){rotX[i]=this.xt+_4bf[i]*this.cosRadian-_4c0[i]*this.sinRadian;rotY[i]=this.yt+_4bf[i]*this.sinRadian+_4c0[i]*this.cosRadian;}this.jsGraphics.drawPolygon(rotX,rotY);};