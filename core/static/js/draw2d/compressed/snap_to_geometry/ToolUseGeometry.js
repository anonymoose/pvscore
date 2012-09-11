/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToolUseGeometry=function(_a2e){ToggleButton.call(this,_a2e);};ToolUseGeometry.prototype=new ToggleButton();ToolUseGeometry.prototype.type="ToolUseGeometry";ToolUseGeometry.prototype.execute=function(){this.getToolPalette().getWorkflow().setSnapToGeometry(this.isDown());};