/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolGroup=function(_897){ToolGeneric.call(this,_897);this.setTooltip("Form Group");};ToolGroup.prototype=new ToolGeneric;ToolGroup.prototype.type="ToolGroup";ToolGroup.prototype.execute=function(x,y){var _89a=new GroupFigure();_89a.setDimension(100,60);var _89b=this.palette.workflow.getBestCompartmentFigure(x,y);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_89a,x,y,_89b));ToolGeneric.prototype.execute.call(this,x,y);};