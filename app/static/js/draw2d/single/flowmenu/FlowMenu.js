FlowMenu=function(_39fd){
this.actionDelete=new ButtonDelete(this);
this.actionFront=new ButtonMoveFront(this);
this.actionBack=new ButtonMoveBack(this);
ToolPalette.call(this);
this.setDimension(20,60);
this.setBackgroundColor(new Color(220,255,255));
this.currentFigure=null;
this.myworkflow=_39fd;
this.added=false;
this.setDeleteable(false);
this.setCanDrag(false);
this.setResizeable(false);
this.setSelectable(false);
this.setBackgroundColor(null);
this.setColor(null);
this.scrollarea.style.borderBottom="0px";
this.actionDelete.setPosition(0,0);
this.actionFront.setPosition(0,18);
this.actionBack.setPosition(0,36);
this.addChild(this.actionDelete);
this.addChild(this.actionFront);
this.addChild(this.actionBack);
};
FlowMenu.prototype=new ToolPalette();
FlowMenu.prototype.setAlpha=function(_39fe){
Figure.prototype.setAlpha.call(this,_39fe);
};
FlowMenu.prototype.hasTitleBar=function(){
return false;
};
FlowMenu.prototype.onSelectionChanged=function(_39ff){
if(_39ff==this.currentFigure){
return;
}
if(_39ff instanceof Line){
return;
}
if(this.added==true){
this.myworkflow.removeFigure(this);
this.added=false;
}
if(_39ff!==null&&this.added==false){
if(this.myworkflow.getEnableSmoothFigureHandling()==true){
this.setAlpha(0.01);
}
this.myworkflow.addFigure(this,100,100);
this.added=true;
}
if(this.currentFigure!==null){
this.currentFigure.detachMoveListener(this);
}
this.currentFigure=_39ff;
if(this.currentFigure!==null){
this.currentFigure.attachMoveListener(this);
this.onOtherFigureMoved(this.currentFigure);
}
};
FlowMenu.prototype.setWorkflow=function(_3a00){
Figure.prototype.setWorkflow.call(this,_3a00);
};
FlowMenu.prototype.onOtherFigureMoved=function(_3a01){
var pos=_3a01.getPosition();
this.setPosition(pos.x+_3a01.getWidth()+7,pos.y-16);
};
