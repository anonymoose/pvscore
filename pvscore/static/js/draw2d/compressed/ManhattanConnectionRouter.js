/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ManhattanConnectionRouter=function(){this.MINDIST=20;};ManhattanConnectionRouter.prototype=new ConnectionRouter();ManhattanConnectionRouter.prototype.type="ManhattanConnectionRouter";ManhattanConnectionRouter.prototype.route=function(conn){var _838=conn.getStartPoint();var _839=this.getStartDirection(conn);var toPt=conn.getEndPoint();var _83b=this.getEndDirection(conn);this._route(conn,toPt,_83b,_838,_839);};ManhattanConnectionRouter.prototype._route=function(conn,_83d,_83e,toPt,_840){var TOL=0.1;var _842=0.01;var UP=0;var _844=1;var DOWN=2;var LEFT=3;var _847=_83d.x-toPt.x;var _848=_83d.y-toPt.y;var _849;var dir;if(((_847*_847)<(_842))&&((_848*_848)<(_842))){conn.addPoint(new Point(toPt.x,toPt.y));return;}if(_83e==LEFT){if((_847>0)&&((_848*_848)<TOL)&&(_840===_844)){_849=toPt;dir=_840;}else{if(_847<0){_849=new Point(_83d.x-this.MINDIST,_83d.y);}else{if(((_848>0)&&(_840===DOWN))||((_848<0)&&(_840==UP))){_849=new Point(toPt.x,_83d.y);}else{if(_83e==_840){var pos=Math.min(_83d.x,toPt.x)-this.MINDIST;_849=new Point(pos,_83d.y);}else{_849=new Point(_83d.x-(_847/2),_83d.y);}}}if(_848>0){dir=UP;}else{dir=DOWN;}}}else{if(_83e==_844){if((_847<0)&&((_848*_848)<TOL)&&(_840===LEFT)){_849=toPt;dir=_840;}else{if(_847>0){_849=new Point(_83d.x+this.MINDIST,_83d.y);}else{if(((_848>0)&&(_840===DOWN))||((_848<0)&&(_840===UP))){_849=new Point(toPt.x,_83d.y);}else{if(_83e==_840){var pos=Math.max(_83d.x,toPt.x)+this.MINDIST;_849=new Point(pos,_83d.y);}else{_849=new Point(_83d.x-(_847/2),_83d.y);}}}if(_848>0){dir=UP;}else{dir=DOWN;}}}else{if(_83e==DOWN){if(((_847*_847)<TOL)&&(_848<0)&&(_840==UP)){_849=toPt;dir=_840;}else{if(_848>0){_849=new Point(_83d.x,_83d.y+this.MINDIST);}else{if(((_847>0)&&(_840===_844))||((_847<0)&&(_840===LEFT))){_849=new Point(_83d.x,toPt.y);}else{if(_83e===_840){var pos=Math.max(_83d.y,toPt.y)+this.MINDIST;_849=new Point(_83d.x,pos);}else{_849=new Point(_83d.x,_83d.y-(_848/2));}}}if(_847>0){dir=LEFT;}else{dir=_844;}}}else{if(_83e==UP){if(((_847*_847)<TOL)&&(_848>0)&&(_840===DOWN)){_849=toPt;dir=_840;}else{if(_848<0){_849=new Point(_83d.x,_83d.y-this.MINDIST);}else{if(((_847>0)&&(_840===_844))||((_847<0)&&(_840===LEFT))){_849=new Point(_83d.x,toPt.y);}else{if(_83e===_840){var pos=Math.min(_83d.y,toPt.y)-this.MINDIST;_849=new Point(_83d.x,pos);}else{_849=new Point(_83d.x,_83d.y-(_848/2));}}}if(_847>0){dir=LEFT;}else{dir=_844;}}}}}}this._route(conn,_849,dir,toPt,_840);conn.addPoint(_83d);};