/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyCommandListener=function(){CommandStackEventListener.call(this);};MyCommandListener.prototype=new CommandStackEventListener;MyCommandListener.prototype.type="MyCommandListener";MyCommandListener.prototype.stackChanged=function(event){var _1182=document.getElementById("log");var log=document.createElement("div");if(event.isPostChangeEvent()){log.innerHTML="POST:";}else{log.innerHTML="PRE:";}var _1184=event.getDetails();if(0!=(_1184&(CommandStack.PRE_EXECUTE|CommandStack.POST_EXECUTE))){log.innerHTML=log.innerHTML+" EXECUTE";}else{if(0!=(_1184&(CommandStack.PRE_UNDO|CommandStack.POST_UNDO))){log.innerHTML=log.innerHTML+" UNDO";}else{if(0!=(_1184&(CommandStack.PRE_REDO|CommandStack.POST_REDO))){log.innerHTML=log.innerHTML+" REDO";}}}var _1185=event.getCommand();if(_1185 instanceof CommandAdd){log.innerHTML=log.innerHTML+" => ADD Element";}else{if(_1185 instanceof CommandConnect){log.innerHTML=log.innerHTML+" => Connect two Ports";}else{if(_1185 instanceof CommandDelete){log.innerHTML=log.innerHTML+" => Delete Element";}else{if(_1185 instanceof CommandMove){log.innerHTML=log.innerHTML+" => Moving Element";}else{if(_1185 instanceof CommandResize){log.innerHTML=log.innerHTML+" => Resize Element";}}}}}_1182.appendChild(log);};