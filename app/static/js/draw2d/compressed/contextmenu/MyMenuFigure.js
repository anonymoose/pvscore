/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyMenuFigure=function(){Rectangle.call(this);this.setDimension(50,50);this.setBackgroundColor(new Color(220,255,255));};MyMenuFigure.prototype=new Rectangle();MyMenuFigure.prototype.getContextMenu=function(){var menu=new Menu();var _7f1=this;menu.appendMenuItem(new MenuItem("Blue",null,function(){_7f1.setBackgroundColor(new Color(0,0,255));}));menu.appendMenuItem(new MenuItem("Green",null,function(){_7f1.setBackgroundColor(new Color(0,255,0));}));menu.appendMenuItem(new MenuItem("Silver",null,function(){_7f1.setBackgroundColor(new Color(128,128,128));}));menu.appendMenuItem(new MenuItem("Black",null,function(){_7f1.setBackgroundColor(new Color(0,0,0));}));return menu;};