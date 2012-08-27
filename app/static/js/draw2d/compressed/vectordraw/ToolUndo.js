/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolUndo=function(_1119){Button.call(this,_1119);this.setDimension(24,24);};ToolUndo.prototype=new Button();ToolUndo.prototype.type="ToolUndo";ToolUndo.prototype.execute=function(){this.getWorkflow().getCommandStack().undo();};