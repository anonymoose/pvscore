/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyCompartmentFigure=function(){CompartmentFigure.call(this);this.defaultColor=new Color(230,230,250);this.setBackgroundColor(this.defaultColor);};MyCompartmentFigure.prototype=new CompartmentFigure();MyCompartmentFigure.prototype.onFigureLeave=function(_507){CompartmentFigure.prototype.onFigureLeave.call(this,_507);if(_507 instanceof CompartmentFigure){_507.setBackgroundColor(_507.defaultColor);}};MyCompartmentFigure.prototype.onFigureDrop=function(_508){CompartmentFigure.prototype.onFigureDrop.call(this,_508);if(_508 instanceof CompartmentFigure){_508.setBackgroundColor(this.getBackgroundColor().darker(0.1));}};MyCompartmentFigure.prototype.setBackgroundColor=function(_509){CompartmentFigure.prototype.setBackgroundColor.call(this,_509);for(var i=0;i<this.children.getSize();i++){var _50b=this.children.get(i);if(_50b instanceof CompartmentFigure){_50b.setBackgroundColor(this.getBackgroundColor().darker(0.1));}}};