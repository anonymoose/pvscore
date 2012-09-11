/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CommandResize=function(_e5e,_e5f,_e60){Command.call(this,"resize figure");this.figure=_e5e;if(_e5f===undefined){this.oldWidth=_e5e.getWidth();this.oldHeight=_e5e.getHeight();}else{this.oldWidth=_e5f;this.oldHeight=_e60;}};CommandResize.prototype=new Command();CommandResize.prototype.type="CommandResize";CommandResize.prototype.setDimension=function(_e61,_e62){this.newWidth=_e61;this.newHeight=_e62;};CommandResize.prototype.canExecute=function(){return this.newWidth!=this.oldWidth||this.newHeight!=this.oldHeight;};CommandResize.prototype.execute=function(){this.redo();};CommandResize.prototype.undo=function(){this.figure.setDimension(this.oldWidth,this.oldHeight);this.figure.workflow.moveResizeHandles(this.figure);};CommandResize.prototype.redo=function(){this.figure.setDimension(this.newWidth,this.newHeight);this.figure.workflow.moveResizeHandles(this.figure);};