/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolRectangleUnfilled=function(_12e1){ToolGeneric.call(this,_12e1);this.setDimension(24,24);};ToolRectangleUnfilled.prototype=new ToolGeneric;ToolRectangleUnfilled.prototype.type="ToolRectangleUnfilled";ToolRectangleUnfilled.prototype.execute=function(x,y){var _12e4=new Rectangle();_12e4.setDimension(100,60);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_12e4,x,y));ToolGeneric.prototype.execute.call(this,x,y);};