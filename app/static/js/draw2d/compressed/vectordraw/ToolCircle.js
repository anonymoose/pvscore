/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolCircle=function(_6d8){ToolGeneric.call(this,_6d8);this.setDimension(24,24);};ToolCircle.prototype=new ToolGeneric();ToolCircle.prototype.type="ToolCircle";ToolCircle.prototype.execute=function(x,y){var _6db=new Circle();_6db.setDimension(100,100);_6db.setBackgroundColor(new Color(255,255,255));this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_6db,x,y));ToolGeneric.prototype.execute.call(this,x,y);};