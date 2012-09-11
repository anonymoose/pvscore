/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolFormButton=function(_aad){ToolGeneric.call(this,_aad);};ToolFormButton.prototype=new ToolGeneric;ToolFormButton.prototype.type="ToolFormButton";ToolFormButton.prototype.execute=function(x,y){var _ab0=new ButtonFigure();_ab0.setDimension(100,20);var _ab1=this.palette.workflow.getBestCompartmentFigure(x,y);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_ab0,x,y,_ab1));ToolGeneric.prototype.execute.call(this,x,y);};