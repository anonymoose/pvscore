/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolOvalUnfilled=function(_bf4){ToolGeneric.call(this,_bf4);this.setDimension(24,24);};ToolOvalUnfilled.prototype=new ToolGeneric();ToolOvalUnfilled.prototype.type="ToolOvalUnfilled";ToolOvalUnfilled.prototype.execute=function(x,y){var _bf7=new Oval();_bf7.setDimension(100,60);this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_bf7,x,y));ToolGeneric.prototype.execute.call(this,x,y);};