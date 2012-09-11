shape.uml.Actor=function(name){
this.portRight=null;
VectorFigure.call(this);
this.setName(name);
this.setDimension(50,90);
};
shape.uml.Actor.prototype=new VectorFigure();
shape.uml.Actor.prototype.type="shape.uml.Actor";
shape.uml.Actor.prototype.setName=function(name){
this.label.innerHTML=name;
};
shape.uml.Actor.prototype.setWorkflow=function(_39b9){
VectorFigure.prototype.setWorkflow.call(this,_39b9);
if(_39b9!==null&&this.portRight===null){
this.portRight=new Port();
this.portRight.setWorkflow(_39b9);
this.addPort(this.portRight,this.width,this.height/2);
this.portLeft=new Port();
this.portLeft.setWorkflow(_39b9);
this.addPort(this.portLeft,0,this.height/2);
}
};
shape.uml.Actor.prototype.createHTMLElement=function(){
var item=Figure.prototype.createHTMLElement.call(this);
this.label=document.createElement("div");
this.label.style.width="100%";
this.label.style.height="20px";
this.label.style.position="absolute";
this.label.style.textAlign="center";
this.label.style.top="0px";
this.label.style.left="0px";
this.label.style.fontSize="8pt";
this.disableTextSelection(this.label);
return item;
};
shape.uml.Actor.prototype.setDimension=function(w,h){
VectorFigure.prototype.setDimension.call(this,w,h);
if(this.portRight!==null){
this.portRight.setPosition(this.width,this.height/2);
this.portLeft.setPosition(0,this.height/2);
}
};
shape.uml.Actor.prototype.paint=function(){
VectorFigure.prototype.paint.call(this);
var _39bd=this.getWidth()/2;
var _39be=this.getWidth()/4;
var _39bf=this.getHeight()/2;
var _39c0=parseInt(this.label.style.height);
var _39c1=this.getWidth()*0.2;
var _39c2=this.getHeight()*0.1;
this.graphics.drawOval(_39bd-_39c1/2,0,_39c1,_39c2);
this.graphics.drawLine(_39bd,_39c2,_39bd,_39bf);
this.graphics.drawLine(_39be,_39c2*2,this.getWidth()-_39be,_39c2*2);
this.graphics.drawLine(_39bd,_39bf,_39be,this.getHeight()-_39c0);
this.graphics.drawLine(_39bd,_39bf,this.getWidth()-_39be,this.getHeight()-_39c0);
this.graphics.paint();
this.label.style.top=(this.getHeight()-_39c0)+"px";
this.html.appendChild(this.label);
};
