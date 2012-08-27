/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MenuItem=function(_c11,_c12,_c13){this.label=_c11;this.iconUrl=_c12;this.parentMenu=null;this.action=_c13;};MenuItem.prototype.type="MenuItem";MenuItem.prototype.isEnabled=function(){return true;};MenuItem.prototype.getLabel=function(){return this.label;};MenuItem.prototype.execute=function(x,y){this.parentMenu.workflow.showMenu(null);this.action(x,y);};