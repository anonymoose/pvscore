/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyWorkflow=function(id){Workflow.call(this,id);};MyWorkflow.prototype=new Workflow();MyWorkflow.prototype.type="MyWorkflow";MyWorkflow.prototype.getContextMenu=function(){var menu=new Menu();var oThis=this;menu.appendMenuItem(new MenuItem("Grid 10x10",null,function(x,y){oThis.setGridWidth(10,10);oThis.setBackgroundImage("grid_10.png",true);}));menu.appendMenuItem(new MenuItem("Grid 20x20",null,function(x,y){oThis.setGridWidth(20,20);oThis.setBackgroundImage("grid_20.png",true);}));menu.appendMenuItem(new MenuItem("Add Circle",null,function(x,y){oThis.addFigure(new Circle(30),x,y);}));return menu;};