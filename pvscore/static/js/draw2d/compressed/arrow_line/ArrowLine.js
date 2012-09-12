/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ArrowLine=function(){this.lineColor=new Color(0,0,0);this.stroke=1;this.canvas=null;this.workflow=null;this.html=null;this.graphics=null;this.id=UUID.create();this.startX=30;this.startY=30;this.endX=100;this.endY=100;this.zOrder=ArrowLine.ZOrderBaseIndex;this.setSelectable(true);this.setDeleteable(true);this.arrowWidth=10;this.arrowLength=20;this.lineWidth=5;};ArrowLine.prototype=new Line();ArrowLine.prototype.type="ArrowLine";ArrowLine.prototype.paint=function(){if(this.graphics===null){this.graphics=new jsGraphics(this.id);}else{this.graphics.clear();}this.graphics.setStroke(this.stroke);this.graphics.setColor(this.lineColor.getHTMLStyle());var endY=this.getLength();var _14d7=[0,0,endY-this.arrowLength,endY-this.arrowLength,endY,endY-this.arrowLength,endY-this.arrowLength,0];var _14d8=[-this.lineWidth,+this.lineWidth,+this.lineWidth,this.lineWidth+this.arrowWidth/2,0,-(this.lineWidth+this.arrowWidth/2),-this.lineWidth,-this.lineWidth];var _14d9=this.getAngle()*Math.PI/180;var rotX=[];var rotY=[];for(var i=0;i<_14d7.length;i++){rotX[i]=this.startX+_14d7[i]*Math.cos(_14d9)-_14d8[i]*Math.sin(_14d9);rotY[i]=this.startY+_14d7[i]*Math.sin(_14d9)+_14d8[i]*Math.cos(_14d9);}this.graphics.drawPolyLine(rotX,rotY);this.graphics.paint();};