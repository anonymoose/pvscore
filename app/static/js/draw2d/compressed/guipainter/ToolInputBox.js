/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolInputBox=function(_265){ToolGeneric.call(this,_265);};ToolInputBox.prototype=new ToolGeneric;ToolInputBox.prototype.type="ToolInputBox";ToolInputBox.prototype.execute=function(x,y){var _268=new InputBoxFigure();_268.setDimension(100,20);var _269=this.palette.workflow.getBestCompartmentFigure(x,y);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_268,x,y,_269));ToolGeneric.prototype.execute.call(this,x,y);};