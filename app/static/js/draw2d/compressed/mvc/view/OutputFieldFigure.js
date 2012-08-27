/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

OutputFieldFigure=function(){OutputPort.call(this);};OutputFieldFigure.prototype=new OutputPort();OutputFieldFigure.prototype.createCommand=function(_1189){if(_1189.getPolicy()==EditPolicy.CONNECT){if(_1189.source.parentNode.id==_1189.target.parentNode.id){return null;}if(_1189.source instanceof InputPort){return new CommandConnect(_1189.canvas,_1189.target,_1189.source);}return null;}return Port.prototype.createCommand.call(this,_1189);};