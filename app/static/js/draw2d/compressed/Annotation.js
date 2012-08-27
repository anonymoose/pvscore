/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Annotation=function(msg){this.msg=msg;this.alpha=1;this.color=new Color(0,0,0);this.bgColor=new Color(241,241,121);this.fontSize=10;this.textNode=null;Figure.call(this);};Annotation.prototype=new Figure();Annotation.prototype.type="Annotation";Annotation.prototype.createHTMLElement=function(){var item=Figure.prototype.createHTMLElement.call(this);item.style.color=this.color.getHTMLStyle();item.style.backgroundColor=this.bgColor.getHTMLStyle();item.style.fontSize=this.fontSize+"pt";item.style.width="auto";item.style.height="auto";item.style.margin="0px";item.style.padding="0px";item.onselectstart=function(){return false;};item.unselectable="on";item.style.cursor="default";this.textNode=document.createTextNode(this.msg);item.appendChild(this.textNode);this.disableTextSelection(item);return item;};Annotation.prototype.onDoubleClick=function(){var _1292=new AnnotationDialog(this);this.workflow.showDialog(_1292);};Annotation.prototype.setBackgroundColor=function(color){this.bgColor=color;if(this.bgColor!==null){this.html.style.backgroundColor=this.bgColor.getHTMLStyle();}else{this.html.style.backgroundColor="transparent";}};Annotation.prototype.getBackgroundColor=function(){return this.bgColor;};Annotation.prototype.setFontSize=function(size){this.fontSize=size;this.html.style.fontSize=this.fontSize+"pt";};Annotation.prototype.getText=function(){return this.msg;};Annotation.prototype.setText=function(text){this.msg=text;this.html.removeChild(this.textNode);this.textNode=document.createTextNode(this.msg);this.html.appendChild(this.textNode);};Annotation.prototype.setStyledText=function(text){this.msg=text;this.html.removeChild(this.textNode);this.textNode=document.createElement("div");this.textNode.innerHTML=text;this.html.appendChild(this.textNode);};