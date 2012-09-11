/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CanvasDocument=function(_511){this.canvas=_511;};CanvasDocument.prototype.type="CanvasDocument";CanvasDocument.prototype.getFigures=function(){var _512=new ArrayList();var _513=this.canvas.figures;var _514=this.canvas.dialogs;for(var i=0;i<_513.getSize();i++){var _516=_513.get(i);if(_514.indexOf(_516)==-1&&_516.getParent()===null&&!(_516 instanceof WindowFigure)){_512.add(_516);}}return _512;};CanvasDocument.prototype.getFigure=function(id){return this.canvas.getFigure(id);};CanvasDocument.prototype.getLines=function(){return this.canvas.getLines();};CanvasDocument.prototype.getLine=function(id){return this.canvas.getLine(id);};