MyCompartmentFigure=function(){
CompartmentFigure.call(this);
this.defaultColor=new Color(230,230,250);
this.setBackgroundColor(this.defaultColor);
};
MyCompartmentFigure.prototype=new CompartmentFigure();
MyCompartmentFigure.prototype.onFigureLeave=function(_3667){
CompartmentFigure.prototype.onFigureLeave.call(this,_3667);
if(_3667 instanceof CompartmentFigure){
_3667.setBackgroundColor(_3667.defaultColor);
}
};
MyCompartmentFigure.prototype.onFigureDrop=function(_3668){
CompartmentFigure.prototype.onFigureDrop.call(this,_3668);
if(_3668 instanceof CompartmentFigure){
_3668.setBackgroundColor(this.getBackgroundColor().darker(0.1));
}
};
MyCompartmentFigure.prototype.setBackgroundColor=function(color){
CompartmentFigure.prototype.setBackgroundColor.call(this,color);
for(var i=0;i<this.children.getSize();i++){
var child=this.children.get(i);
if(child instanceof CompartmentFigure){
child.setBackgroundColor(this.getBackgroundColor().darker(0.1));
}
}
};
