/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CheckBoxFigure=function(_cee){if(_cee){this.title=_cee;}else{this.title="";}Figure.call(this);};CheckBoxFigure.prototype=new Figure();CheckBoxFigure.prototype.createHTMLElement=function(){var item=Figure.prototype.createHTMLElement.call(this);item.style.margin="0px";item.style.padding="0px";this.ui_element=document.createElement("input");this.ui_element.type="checkbox";this.ui_element.style.position="absolute";this.ui_element.style.left="0px";this.ui_element.style.top="0px";this.ui_element.style.margin="0px";this.ui_element.style.padding="0px";this.ui_element.style.cursor="move";this.textNode=document.createElement("div");this.textNode.innerHTML="blabla";this.textNode.style.fontFamily="sans-serif";this.textNode.style.fontSize="8pt";this.textNode.style.position="absolute";this.textNode.style.left="20px";this.textNode.style.top="0px";item.appendChild(this.ui_element);item.appendChild(this.textNode);return item;};CheckBoxFigure.prototype.setDimension=function(w,h){Figure.prototype.setDimension.call(this,w,20);};