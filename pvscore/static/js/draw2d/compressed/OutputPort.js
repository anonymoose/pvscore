/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

OutputPort=function(_127d){Port.call(this,_127d);this.maxFanOut=100;};OutputPort.prototype=new Port();OutputPort.prototype.type="OutputPort";OutputPort.prototype.onDragEnter=function(port){if(this.getMaxFanOut()<=this.getFanOut()){return;}if(port instanceof InputPort){Port.prototype.onDragEnter.call(this,port);}else{if(port instanceof LineStartResizeHandle){var line=this.workflow.currentSelection;if(line instanceof Connection&&line.getSource() instanceof OutputPort){Port.prototype.onDragEnter.call(this,line.getTarget());}}else{if(port instanceof LineEndResizeHandle){var line=this.workflow.currentSelection;if(line instanceof Connection&&line.getTarget() instanceof OutputPort){Port.prototype.onDragEnter.call(this,line.getSource());}}}}};OutputPort.prototype.onDragLeave=function(port){if(port instanceof InputPort){Port.prototype.onDragLeave.call(this,port);}else{if(port instanceof LineStartResizeHandle){var line=this.workflow.currentSelection;if(line instanceof Connection&&line.getSource() instanceof OutputPort){Port.prototype.onDragLeave.call(this,line.getTarget());}}else{if(port instanceof LineEndResizeHandle){var line=this.workflow.currentSelection;if(line instanceof Connection&&line.getTarget() instanceof OutputPort){Port.prototype.onDragLeave.call(this,line.getSource());}}}}};OutputPort.prototype.onDragstart=function(x,y){if(!this.canDrag){return false;}if(this.maxFanOut===-1){return true;}if(this.getMaxFanOut()<=this.getFanOut()){return false;}return true;};OutputPort.prototype.setMaxFanOut=function(count){this.maxFanOut=count;};OutputPort.prototype.getMaxFanOut=function(){return this.maxFanOut;};OutputPort.prototype.getFanOut=function(){if(this.getParent().workflow===null){return 0;}var count=0;var lines=this.getParent().workflow.getLines();var size=lines.getSize();for(var i=0;i<size;i++){var line=lines.get(i);if(line instanceof Connection){if(line.getSource()==this){count++;}else{if(line.getTarget()==this){count++;}}}}return count;};OutputPort.prototype.createCommand=function(_128a){if(_128a.getPolicy()===EditPolicy.CONNECT){if(_128a.source.parentNode.id===_128a.target.parentNode.id){return null;}if(_128a.source instanceof InputPort){return new CommandConnect(_128a.canvas,_128a.target,_128a.source);}return null;}return Port.prototype.createCommand.call(this,_128a);};