/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

FlowMenu=function(_89d){this.actionDelete=new ButtonDelete(this);this.actionFront=new ButtonMoveFront(this);this.actionBack=new ButtonMoveBack(this);ToolPalette.call(this);this.setDimension(20,60);this.setBackgroundColor(new Color(220,255,255));this.currentFigure=null;this.myworkflow=_89d;this.added=false;this.setDeleteable(false);this.setCanDrag(false);this.setResizeable(false);this.setSelectable(false);this.setBackgroundColor(null);this.setColor(null);this.scrollarea.style.borderBottom="0px";this.actionDelete.setPosition(0,0);this.actionFront.setPosition(0,18);this.actionBack.setPosition(0,36);this.addChild(this.actionDelete);this.addChild(this.actionFront);this.addChild(this.actionBack);};FlowMenu.prototype=new ToolPalette();FlowMenu.prototype.setAlpha=function(_89e){Figure.prototype.setAlpha.call(this,_89e);};FlowMenu.prototype.hasTitleBar=function(){return false;};FlowMenu.prototype.onSelectionChanged=function(_89f){if(_89f==this.currentFigure){return;}if(_89f instanceof Line){return;}if(this.added==true){this.myworkflow.removeFigure(this);this.added=false;}if(_89f!==null&&this.added==false){if(this.myworkflow.getEnableSmoothFigureHandling()==true){this.setAlpha(0.01);}this.myworkflow.addFigure(this,100,100);this.added=true;}if(this.currentFigure!==null){this.currentFigure.detachMoveListener(this);}this.currentFigure=_89f;if(this.currentFigure!==null){this.currentFigure.attachMoveListener(this);this.onOtherFigureMoved(this.currentFigure);}};FlowMenu.prototype.setWorkflow=function(_8a0){Figure.prototype.setWorkflow.call(this,_8a0);};FlowMenu.prototype.onOtherFigureMoved=function(_8a1){var pos=_8a1.getPosition();this.setPosition(pos.x+_8a1.getWidth()+7,pos.y-16);};