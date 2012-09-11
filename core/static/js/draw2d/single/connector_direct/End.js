End=function(){
ImageFigure.call(this,this.type+".png");
this.inputPort=null;
this.setDimension(50,50);
};
End.prototype=new ImageFigure();
End.prototype.type="End";
End.prototype.setWorkflow=function(_463d){
ImageFigure.prototype.setWorkflow.call(this,_463d);
if(_463d!==null&&this.inputPort===null){
this.inputPort=new InputPort();
this.inputPort.setWorkflow(_463d);
this.inputPort.setBackgroundColor(new Color(115,115,245));
this.addPort(this.inputPort,0,this.height/2);
}
};
