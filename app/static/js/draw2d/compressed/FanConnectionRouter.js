/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

FanConnectionRouter=function(){};FanConnectionRouter.prototype=new NullConnectionRouter();FanConnectionRouter.prototype.type="FanConnectionRouter";FanConnectionRouter.prototype.route=function(conn){var _6e6=conn.getStartPoint();var toPt=conn.getEndPoint();var _6e8=conn.getSource().getConnections();var _6e9=new ArrayList();var _6ea=0;for(var i=0;i<_6e8.getSize();i++){var _6ec=_6e8.get(i);if(_6ec.getTarget()==conn.getTarget()||_6ec.getSource()==conn.getTarget()){_6e9.add(_6ec);if(conn==_6ec){_6ea=_6e9.getSize();}}}if(_6e9.getSize()>1){this.routeCollision(conn,_6ea);}else{NullConnectionRouter.prototype.route.call(this,conn);}};FanConnectionRouter.prototype.routeNormal=function(conn){conn.addPoint(conn.getStartPoint());conn.addPoint(conn.getEndPoint());};FanConnectionRouter.prototype.routeCollision=function(conn,_6ef){var _6f0=conn.getStartPoint();var end=conn.getEndPoint();conn.addPoint(_6f0);var _6f2=10;var _6f3=new Point((end.x+_6f0.x)/2,(end.y+_6f0.y)/2);var _6f4=end.getPosition(_6f0);var ray;if(_6f4==PositionConstants.SOUTH||_6f4==PositionConstants.EAST){ray=new Point(end.x-_6f0.x,end.y-_6f0.y);}else{ray=new Point(_6f0.x-end.x,_6f0.y-end.y);}var _6f6=Math.sqrt(ray.x*ray.x+ray.y*ray.y);var _6f7=_6f2*ray.x/_6f6;var _6f8=_6f2*ray.y/_6f6;var _6f9;if(_6ef%2===0){_6f9=new Point(_6f3.x+(_6ef/2)*(-1*_6f8),_6f3.y+(_6ef/2)*_6f7);}else{_6f9=new Point(_6f3.x+(_6ef/2)*_6f8,_6f3.y+(_6ef/2)*(-1*_6f7));}conn.addPoint(_6f9);conn.addPoint(end);};