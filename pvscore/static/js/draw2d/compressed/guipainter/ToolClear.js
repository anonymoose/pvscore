/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolClear=function(_8){Button.call(this,_8);};ToolClear.prototype=new Button();ToolClear.prototype.type="ToolClear";ToolClear.prototype.execute=function(){this.palette.workflow.clear();ToolGeneric.prototype.execute.call(this);};