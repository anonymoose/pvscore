/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ContextmenuConnection=function(){Connection.call(this);this.sourcePort=null;this.targetPort=null;this.lineSegments=[];this.setColor(new Color(0,0,115));this.setLineWidth(2);};ContextmenuConnection.prototype=new Connection();ContextmenuConnection.prototype.getContextMenu=function(){var menu=new Menu();var _c06=this;menu.appendMenuItem(new MenuItem("Blue",null,function(){_c06.setColor(new Color(0,0,255));}));menu.appendMenuItem(new MenuItem("Green",null,function(){_c06.setColor(new Color(0,255,0));}));menu.appendMenuItem(new MenuItem("Silver",null,function(){_c06.setColor(new Color(128,128,128));}));menu.appendMenuItem(new MenuItem("Black",null,function(){_c06.setColor(new Color(0,0,0));}));return menu;};