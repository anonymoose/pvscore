/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CommandSetColor=function(_129a,color){Command.call(this,"set color");this.figure=_129a;this.newColor=color;this.oldColor=_129a.getColor();};CommandSetColor.prototype=new Command();CommandSetColor.prototype.type="CommandSetColor";CommandSetColor.prototype.execute=function(){this.redo();};CommandSetColor.prototype.undo=function(){this.figure.setColor(this.oldColor);};CommandSetColor.prototype.redo=function(){this.figure.setColor(this.newColor);};