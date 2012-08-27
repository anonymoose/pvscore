/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolCheckBox=function(_1164){ToolGeneric.call(this,_1164);};ToolCheckBox.prototype=new ToolGeneric;ToolCheckBox.prototype.type="ToolCheckBox";ToolCheckBox.prototype.execute=function(x,y){var _1167=new CheckBoxFigure();_1167.setDimension(100,20);var _1168=this.palette.workflow.getBestCompartmentFigure(x,y);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_1167,x,y,_1168));ToolGeneric.prototype.execute.call(this,x,y);};