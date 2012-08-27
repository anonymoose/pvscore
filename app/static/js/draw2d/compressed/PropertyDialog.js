/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

PropertyDialog=function(_712,_713,_714){this.figure=_712;this.propertyName=_713;this.label=_714;Dialog.call(this);this.setDimension(400,120);};PropertyDialog.prototype=new Dialog();PropertyDialog.prototype.type="PropertyDialog";PropertyDialog.prototype.createHTMLElement=function(){var item=Dialog.prototype.createHTMLElement.call(this);var _716=document.createElement("form");_716.style.position="absolute";_716.style.left="10px";_716.style.top="30px";_716.style.width="375px";_716.style.font="normal 10px verdana";item.appendChild(_716);this.labelDiv=document.createElement("div");this.labelDiv.innerHTML=this.label;this.disableTextSelection(this.labelDiv);_716.appendChild(this.labelDiv);this.input=document.createElement("input");this.input.style.border="1px solid gray";this.input.style.font="normal 10px verdana";this.input.type="text";var _717=this.figure.getProperty(this.propertyName);if(_717){this.input.value=_717;}else{this.input.value="";}this.input.style.width="100%";_716.appendChild(this.input);this.input.focus();return item;};PropertyDialog.prototype.onOk=function(){Dialog.prototype.onOk.call(this);this.figure.setProperty(this.propertyName,this.input.value);};