/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ResizeImage=function(_9){this.url=_9;Node.call(this);this.outputPort1=null;this.outputPort2=null;this.setDimension(100,100);this.setColor(null);};ResizeImage.prototype=new Node;ResizeImage.prototype.type="ResizeImage";ResizeImage.prototype.createHTMLElement=function(){var _a=Node.prototype.createHTMLElement.call(this);if(navigator.appName.toUpperCase()=="MICROSOFT INTERNET EXPLORER"){this.d=document.createElement("div");this.d.style.position="absolute";this.d.style.left="0px";this.d.style.top="0px";this.d.style.filter="progid:DXImageTransform.Microsoft.AlphaImageLoader (src='"+this.url+"', sizingMethod='scale')";_a.appendChild(this.d);}else{this.img=document.createElement("img");this.img.style.position="absolute";this.img.style.left="0px";this.img.style.top="0px";this.img.src=this.url;_a.appendChild(this.img);this.d=document.createElement("div");this.d.style.position="absolute";this.d.style.left="0px";this.d.style.top="0px";_a.appendChild(this.d);}_a.style.left=this.x+"px";_a.style.top=this.y+"px";return _a;};ResizeImage.prototype.setDimension=function(w,h){Node.prototype.setDimension.call(this,w,h);if(this.d!==null){this.d.style.width=this.width+"px";this.d.style.height=this.height+"px";}if(this.img!==null){this.img.width=this.width;this.img.height=this.height;}if(this.outputPort1!==null){this.outputPort1.setPosition(this.width+3,this.height/3);this.outputPort2.setPosition(this.width+3,this.height/3*2);}};ResizeImage.prototype.setWorkflow=function(_d){Node.prototype.setWorkflow.call(this,_d);if(_d!==null){this.outputPort1=new OutputPort();this.outputPort1.setMaxFanOut(1);this.outputPort1.setWorkflow(_d);this.outputPort1.setBackgroundColor(new Color(245,115,115));this.addPort(this.outputPort1,this.width+3,this.height/3);this.outputPort2=new OutputPort();this.outputPort2.setMaxFanOut(1);this.outputPort2.setWorkflow(_d);this.outputPort2.setBackgroundColor(new Color(245,115,115));this.addPort(this.outputPort2,this.width+3,this.height/3*2);}};