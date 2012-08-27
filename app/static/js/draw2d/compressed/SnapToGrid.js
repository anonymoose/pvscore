/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

SnapToGrid=function(_cdc){SnapToHelper.call(this,_cdc);};SnapToGrid.prototype=new SnapToHelper();SnapToGrid.prototype.type="SnapToGrid";SnapToGrid.prototype.snapPoint=function(_cdd,_cde,_cdf){_cdf.x=this.workflow.gridWidthX*Math.floor(((_cde.x+this.workflow.gridWidthX/2)/this.workflow.gridWidthX));_cdf.y=this.workflow.gridWidthY*Math.floor(((_cde.y+this.workflow.gridWidthY/2)/this.workflow.gridWidthY));return 0;};SnapToGrid.prototype.snapRectangle=function(_ce0,_ce1){_ce1.x=_ce0.x;_ce1.y=_ce0.y;_ce1.w=_ce0.w;_ce1.h=_ce0.h;return 0;};