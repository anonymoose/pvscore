/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

DoubleclickConnection=function(){Connection.call(this);this.sourcePort=null;this.targetPort=null;this.lineSegments=[];this.setColor(new Color(0,0,115));this.setLineWidth(2);this.setColor(new Color(128,255,128));this.isHighlight=false;};DoubleclickConnection.prototype=new Connection();DoubleclickConnection.prototype.onDoubleClick=function(){this.isHighlight=!this.isHighlight;if(this.isHighlight){this.setLineWidth(5);this.setColor(new Color(255,128,128));}else{this.setLineWidth(2);this.setColor(new Color(128,255,128));}};