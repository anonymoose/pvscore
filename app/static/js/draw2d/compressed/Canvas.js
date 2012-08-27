/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Canvas=function(_1102){try{if(_1102){this.construct(_1102);}this.enableSmoothFigureHandling=false;this.canvasLines=new ArrayList();}catch(e){pushErrorStack(e,"Canvas=function(/*:String*/id)");}};Canvas.IMAGE_BASE_URL="";Canvas.prototype.type="Canvas";Canvas.prototype.construct=function(_1103){this.canvasId=_1103;this.html=document.getElementById(this.canvasId);this.scrollArea=document.body.parentNode;};Canvas.prototype.setViewPort=function(divId){this.scrollArea=document.getElementById(divId);};Canvas.prototype.addFigure=function(_1105,xPos,yPos,_1108){try{if(this.enableSmoothFigureHandling===true){if(_1105.timer<=0){_1105.setAlpha(0.001);}var _1109=_1105;var _110a=function(){if(_1109.alpha<1){_1109.setAlpha(Math.min(1,_1109.alpha+0.05));}else{window.clearInterval(_1109.timer);_1109.timer=-1;}};if(_1109.timer>0){window.clearInterval(_1109.timer);}_1109.timer=window.setInterval(_110a,30);}_1105.setCanvas(this);if(xPos&&yPos){_1105.setPosition(xPos,yPos);}if(_1105 instanceof Line){this.canvasLines.add(_1105);this.html.appendChild(_1105.getHTMLElement());}else{var obj=this.canvasLines.getFirstElement();if(obj===null){this.html.appendChild(_1105.getHTMLElement());}else{this.html.insertBefore(_1105.getHTMLElement(),obj.getHTMLElement());}}if(!_1108){_1105.paint();}}catch(e){pushErrorStack(e,"Canvas.prototype.addFigure= function( /*:Figure*/figure,/*:int*/ xPos,/*:int*/ yPos, /*:boolean*/ avoidPaint)");}};Canvas.prototype.removeFigure=function(_110c){if(this.enableSmoothFigureHandling===true){var oThis=this;var _110e=_110c;var _110f=function(){if(_110e.alpha>0){_110e.setAlpha(Math.max(0,_110e.alpha-0.05));}else{window.clearInterval(_110e.timer);_110e.timer=-1;oThis.html.removeChild(_110e.html);_110e.setCanvas(null);}};if(_110e.timer>0){window.clearInterval(_110e.timer);}_110e.timer=window.setInterval(_110f,20);}else{this.html.removeChild(_110c.html);_110c.setCanvas(null);}if(_110c instanceof Line){this.canvasLines.remove(_110c);}};Canvas.prototype.getEnableSmoothFigureHandling=function(){return this.enableSmoothFigureHandling;};Canvas.prototype.setEnableSmoothFigureHandling=function(flag){this.enableSmoothFigureHandling=flag;};Canvas.prototype.getWidth=function(){return parseInt(this.html.style.width);};Canvas.prototype.setWidth=function(width){if(this.scrollArea!==null){this.scrollArea.style.width=width+"px";}else{this.html.style.width=width+"px";}};Canvas.prototype.getHeight=function(){return parseInt(this.html.style.height);};Canvas.prototype.setHeight=function(_1112){if(this.scrollArea!==null){this.scrollArea.style.height=_1112+"px";}else{this.html.style.height=_1112+"px";}};Canvas.prototype.setBackgroundImage=function(_1113,_1114){if(_1113!==null){if(_1114){this.html.style.background="transparent url("+_1113+") ";}else{this.html.style.background="transparent url("+_1113+") no-repeat";}}else{this.html.style.background="transparent";}};Canvas.prototype.getY=function(){return this.y;};Canvas.prototype.getX=function(){return this.x;};Canvas.prototype.getAbsoluteY=function(){var el=this.html;var ot=el.offsetTop;while((el=el.offsetParent)!==null){ot+=el.offsetTop;}return ot;};Canvas.prototype.getAbsoluteX=function(){var el=this.html;var ol=el.offsetLeft;while((el=el.offsetParent)!==null){ol+=el.offsetLeft;}return ol;};Canvas.prototype.getScrollLeft=function(){return this.scrollArea.scrollLeft;};Canvas.prototype.getScrollTop=function(){return this.scrollArea.scrollTop;};