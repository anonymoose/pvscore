End=function(){
ImageFigure.call(this,this.type+".png");
this.inputPort=null;
this.setDimension(50,50);
};
End.prototype=new ImageFigure();
End.prototype.type="End";
End.prototype.setWorkflow=function(_3670){
ImageFigure.prototype.setWorkflow.call(this,_3670);
if(_3670!==null&&this.inputPort===null){
this.inputPort=new InputPort();
this.inputPort.setWorkflow(_3670);
this.inputPort.setBackgroundColor(new Color(115,115,245));
this.inputPort.setColor(null);
this.inputPort.setName("input");
this.addPort(this.inputPort,0,this.height/2);
}
};
