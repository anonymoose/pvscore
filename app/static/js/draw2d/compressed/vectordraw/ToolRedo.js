/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolRedo=function(_c10){Button.call(this,_c10);this.setDimension(24,24);};ToolRedo.prototype=new Button();ToolRedo.prototype.type="ToolRedo";ToolRedo.prototype.execute=function(){this.getWorkflow().getCommandStack().redo();};