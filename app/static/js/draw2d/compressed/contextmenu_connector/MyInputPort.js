/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyInputPort=function(_e){InputPort.call(this,_e);};MyInputPort.prototype=new InputPort();MyInputPort.prototype.type="MyInputPort";MyInputPort.prototype.onDrop=function(_f){if(_f.getMaxFanOut&&_f.getMaxFanOut()<=_f.getFanOut()){return;}if(this.parentNode.id==_f.parentNode.id){}else{var _10=new CommandConnect(this.parentNode.workflow,_f,this);_10.setConnection(new ContextmenuConnection());this.parentNode.workflow.getCommandStack().execute(_10);}};