/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolOval=function(_a29){ToolGeneric.call(this,_a29);this.setDimension(24,24);};ToolOval.prototype=new ToolGeneric();ToolOval.prototype.type="ToolOval";ToolOval.prototype.execute=function(x,y){var _a2c=new Oval();_a2c.setDimension(100,60);_a2c.setBackgroundColor(new Color(255,255,255));this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_a2c,x,y));ToolGeneric.prototype.execute.call(this,x,y);};