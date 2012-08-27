/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

End=function(){ImageFigure.call(this,this.type+".png");this.inputPort=null;this.setDimension(50,50);};End.prototype=new ImageFigure();End.prototype.type="End";End.prototype.setWorkflow=function(_510){ImageFigure.prototype.setWorkflow.call(this,_510);if(_510!==null&&this.inputPort===null){this.inputPort=new InputPort();this.inputPort.setWorkflow(_510);this.inputPort.setBackgroundColor(new Color(115,115,245));this.inputPort.setColor(null);this.inputPort.setName("input");this.addPort(this.inputPort,0,this.height/2);}};