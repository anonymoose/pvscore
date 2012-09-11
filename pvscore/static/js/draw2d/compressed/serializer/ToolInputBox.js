/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolInputBox=function(_70d){ToolGeneric.call(this,_70d);};ToolInputBox.prototype=new ToolGeneric;ToolInputBox.prototype.type="ToolInputBox";ToolInputBox.prototype.execute=function(x,y){var _710=new InputBoxFigure();_710.setDimension(100,20);this.palette.workflow.addFigure(_710,x,y);var _711=this.palette.workflow.getBestCompartmentFigure(x,y);if(_711){_711.addChild(_710);}ToolGeneric.prototype.execute.call(this,x,y);};