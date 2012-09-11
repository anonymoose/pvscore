End=function(){
ImageFigure.call(this,this.type+".png");
this.inputPort=null;
this.setDimension(50,50);
};
End.prototype=new ImageFigure();
End.prototype.type="End";
End.prototype.setWorkflow=function(_4424){
ImageFigure.prototype.setWorkflow.call(this,_4424);
if(_4424!==null&&this.inputPort===null){
this.inputPort=new MyInputPort();
this.inputPort.setWorkflow(_4424);
this.inputPort.setBackgroundColor(new Color(115,115,245));
this.addPort(this.inputPort,0,this.height/2);
}
};
