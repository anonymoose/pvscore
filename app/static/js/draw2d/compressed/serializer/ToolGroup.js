/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolGroup=function(_9a7){ToolGeneric.call(this,_9a7);this.setTooltip("Form Group");};ToolGroup.prototype=new ToolGeneric;ToolGroup.prototype.type="ToolGroup";ToolGroup.prototype.execute=function(x,y){var _9aa=new GroupFigure();_9aa.setDimension(100,60);this.palette.workflow.addFigure(_9aa,x,y);ToolGeneric.prototype.execute.call(this,x,y);};