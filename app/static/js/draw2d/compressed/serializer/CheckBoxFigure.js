/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CheckBoxFigure=function(_26){if(_26){this.title=_26;}else{this.title="";}Figure.call(this);this.setProperty("property_1","value_1");this.setProperty("property_2","value_2");this.setProperty("property_3","value_3");};CheckBoxFigure.prototype=new Figure();CheckBoxFigure.prototype.type="CheckBoxFigure";CheckBoxFigure.prototype.createHTMLElement=function(){var _27=Figure.prototype.createHTMLElement.call(this);_27.style.margin="0px";_27.style.padding="0px";this.ui_element=document.createElement("input");this.ui_element.type="checkbox";this.ui_element.style.position="absolute";this.ui_element.style.left="0px";this.ui_element.style.top="0px";this.ui_element.style.margin="0px";this.ui_element.style.padding="0px";this.ui_element.style.cursor="move";this.textNode=document.createElement("div");this.textNode.innerHTML="blabla";this.textNode.style.fontFamily="sans-serif";this.textNode.style.fontSize="8pt";this.textNode.style.position="absolute";this.textNode.style.left="20px";this.textNode.style.top="0px";_27.appendChild(this.ui_element);_27.appendChild(this.textNode);return _27;};CheckBoxFigure.prototype.setDimension=function(w,h){Figure.prototype.setDimension.call(this,w,20);};