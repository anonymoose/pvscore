/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

InputFieldFigure=function(){InputPort.call(this);};InputFieldFigure.prototype=new InputPort();InputFieldFigure.prototype.type="InputFieldFigure";InputFieldFigure.prototype.createCommand=function(_1153){if(_1153.getPolicy()==EditPolicy.CONNECT){if(_1153.source.parentNode.id==_1153.target.parentNode.id){return null;}if(_1153.source instanceof OutputPort){return new CommandConnect(_1153.canvas,_1153.source,_1153.target);}}return InputPort.prototype.createCommand.call(this,_1153);};