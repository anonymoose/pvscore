/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

AnnotationDialog=function(_5c5){this.figure=_5c5;Dialog.call(this);this.setDimension(400,100);};AnnotationDialog.prototype=new Dialog();AnnotationDialog.prototype.type="AnnotationDialog";AnnotationDialog.prototype.createHTMLElement=function(){var item=Dialog.prototype.createHTMLElement.call(this);var _5c7=document.createElement("form");_5c7.style.position="absolute";_5c7.style.left="10px";_5c7.style.top="30px";_5c7.style.width="375px";_5c7.style.font="normal 10px verdana";item.appendChild(_5c7);this.label=document.createTextNode("Text");_5c7.appendChild(this.label);this.input=document.createElement("input");this.input.style.border="1px solid gray";this.input.style.font="normal 10px verdana";this.input.type="text";var _5c8=this.figure.getText();if(_5c8){this.input.value=_5c8;}else{this.input.value="";}this.input.style.width="100%";_5c7.appendChild(this.input);this.input.focus();return item;};AnnotationDialog.prototype.onOk=function(){this.workflow.getCommandStack().execute(new CommandSetText(this.figure,this.input.value));this.workflow.removeFigure(this);};