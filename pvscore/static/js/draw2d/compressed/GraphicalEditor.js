/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

GraphicalEditor=function(id){try{this.view=new GraphicalViewer(id);this.initializeGraphicalViewer();}catch(e){pushErrorStack(e,"GraphicalEditor=function(/*:String*/ id)");}};GraphicalEditor.prototype.type="GraphicalEditor";GraphicalEditor.prototype.initializeGraphicalViewer=function(){};GraphicalEditor.prototype.getGraphicalViewer=function(){return this.view;};