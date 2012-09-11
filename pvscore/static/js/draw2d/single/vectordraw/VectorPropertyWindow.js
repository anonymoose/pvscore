VectorPropertyWindow=function(){
PropertyWindow.call(this);
this.setDimension(180,150);
};
VectorPropertyWindow.prototype=new PropertyWindow();
VectorPropertyWindow.prototype.type="VectorPropertyWindow";
VectorPropertyWindow.prototype.createHTMLElement=function(){
var item=PropertyWindow.prototype.createHTMLElement.call(this);
this.lineColorLabel=this.createLabel("Line Color:",15,100);
item.appendChild(this.lineColorLabel);
this.fillColorLabel=this.createLabel("Fill Color:",15,120);
item.appendChild(this.fillColorLabel);
this.lineColorArea=this.createLabel("&nbsp;",85,100);
this.lineColorArea.style.width="50px";
this.lineColorArea.style.border="1px solid gray";
this.lineColorArea.hostDialog=this;
this.lineColorArea.onclick=function(){
this.hostDialog.showLineColorDialog();
};
item.appendChild(this.lineColorArea);
this.fillColorArea=this.createLabel("&nbsp;",85,120);
this.fillColorArea.style.width="50px";
this.fillColorArea.style.border="1px solid gray";
this.fillColorArea.hostDialog=this;
this.fillColorArea.onclick=function(){
this.hostDialog.showFillColorDialog();
};
item.appendChild(this.fillColorArea);
return item;
};
VectorPropertyWindow.prototype.onSelectionChanged=function(_3d59){
PropertyWindow.prototype.onSelectionChanged.call(this,_3d59);
if(_3d59!==null&&(typeof _3d59.getColor=="function")){
if(_3d59.getColor()!==null){
this.lineColorArea.style.background=_3d59.getColor().getHTMLStyle();
}else{
this.lineColorArea.style.background="transparent";
}
this.lineColorArea.style.cursor="pointer";
this.lineColorArea.style.border="1px solid gray";
this.lineColorLabel.style.color="black";
}else{
this.lineColorArea.style.background="transparent";
this.lineColorArea.style.cursor=null;
this.lineColorArea.style.border="1px solid #d0d0d0";
this.lineColorLabel.style.color="#d0d0d0";
}
if(_3d59!==null&&(typeof _3d59.getBackgroundColor=="function")){
if(_3d59.getBackgroundColor()!==null){
this.fillColorArea.style.background=_3d59.getBackgroundColor().getHTMLStyle();
}else{
this.fillColorArea.style.background="transparent";
}
this.fillColorArea.style.cursor="pointer";
this.fillColorArea.style.border="1px solid gray";
this.fillColorLabel.style.color="black";
}else{
this.fillColorArea.style.background="transparent";
this.fillColorArea.style.cursor=null;
this.fillColorArea.style.border="1px solid #d0d0d0";
this.fillColorLabel.style.color="#d0d0d0";
}
};
VectorPropertyWindow.prototype.showLineColorDialog=function(){
if((this.getCurrentSelection()===null)||(typeof this.getCurrentSelection().getColor!="function")){
return;
}
var _3d5a=new LineColorDialog(this.getCurrentSelection());
_3d5a.setColor(this.getCurrentSelection().getColor());
this.workflow.showDialog(_3d5a);
};
VectorPropertyWindow.prototype.showFillColorDialog=function(){
if(typeof this.getCurrentSelection().getBackgroundColor!="function"){
return;
}
var _3d5b=new BackgroundColorDialog(this.getCurrentSelection());
_3d5b.setColor(this.getCurrentSelection().getBackgroundColor());
this.workflow.showDialog(_3d5b);
};
