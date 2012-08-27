/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyInputPort=function(_cc2){InputPort.call(this,_cc2);};MyInputPort.prototype=new InputPort();MyInputPort.prototype.type="MyInputPort";MyInputPort.prototype.onDrop=function(port){if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){return;}if(this.parentNode.id==port.parentNode.id){}else{var _cc4=new CommandConnect(this.parentNode.workflow,port,this);_cc4.setConnection(new DoubleclickConnection());this.parentNode.workflow.getCommandStack().execute(_cc4);}};