/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

NullConnectionRouter=function(){};NullConnectionRouter.prototype=new ConnectionRouter();NullConnectionRouter.prototype.type="NullConnectionRouter";NullConnectionRouter.prototype.invalidate=function(){};NullConnectionRouter.prototype.route=function(_14e9){_14e9.addPoint(_14e9.getStartPoint());_14e9.addPoint(_14e9.getEndPoint());};