End=function(){
ImageFigure.call(this,this.type+".png");
this.inputPort=null;
this.setDimension(50,50);
};
End.prototype=new ImageFigure();
End.prototype.type="End";
End.prototype.setWorkflow=function(_3dd9){
ImageFigure.prototype.setWorkflow.call(this,_3dd9);
if(_3dd9!==null&&this.inputPort===null){
this.inputPort=new InputPort();
this.inputPort.setWorkflow(_3dd9);
this.inputPort.setBackgroundColor(new Color(115,115,245));
this.inputPort.setColor(null);
this.addPort(this.inputPort,0,this.height/2);
}
};
