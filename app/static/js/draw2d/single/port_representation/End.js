End=function(){
ImageFigure.call(this,this.type+".png");
this.inputPort=null;
this.setDimension(50,50);
};
End.prototype=new ImageFigure();
End.prototype.type="End";
End.prototype.setWorkflow=function(_3b8d){
ImageFigure.prototype.setWorkflow.call(this,_3b8d);
if(_3b8d!==null&&this.inputPort===null){
this.inputPort=new InputPort();
this.inputPort.setWorkflow(_3b8d);
this.inputPort.setBackgroundColor(new Color(115,115,245));
this.inputPort.setColor(null);
this.addPort(this.inputPort,0,this.height/2);
}
};
