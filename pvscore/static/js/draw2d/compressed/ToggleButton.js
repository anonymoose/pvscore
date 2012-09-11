/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ToggleButton=function(_e34){Button.call(this,_e34);this.isDownFlag=false;};ToggleButton.prototype=new Button();ToggleButton.prototype.type="ToggleButton";ToggleButton.prototype.createHTMLElement=function(){var item=document.createElement("div");item.id=this.id;item.style.position="absolute";item.style.left=this.x+"px";item.style.top=this.y+"px";item.style.height="24px";item.style.width="24px";item.style.margin="0px";item.style.padding="0px";if(this.getImageUrl()!==null){item.style.backgroundImage="url("+this.getImageUrl()+")";}else{item.style.backgroundImage="";}var _e36=this;this.omousedown=function(_e37){if(_e36.enabled){if(!_e36.isDown()){Button.prototype.setActive.call(_e36,true);}}_e37.cancelBubble=true;_e37.returnValue=false;};this.omouseup=function(_e38){if(_e36.enabled){if(_e36.isDown()){Button.prototype.setActive.call(_e36,false);}_e36.isDownFlag=!_e36.isDownFlag;_e36.execute();}_e38.cancelBubble=true;_e38.returnValue=false;};if(item.addEventListener){item.addEventListener("mousedown",this.omousedown,false);item.addEventListener("mouseup",this.omouseup,false);}else{if(item.attachEvent){item.attachEvent("onmousedown",this.omousedown);item.attachEvent("onmouseup",this.omouseup);}}return item;};ToggleButton.prototype.isDown=function(){return this.isDownFlag;};ToggleButton.prototype.setActive=function(flag){Button.prototype.setActive.call(this,flag);this.isDownFlag=flag;};ToggleButton.prototype.execute=function(){};