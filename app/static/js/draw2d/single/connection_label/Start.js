Start=function(){
ImageFigure.call(this,this.type+".png");
this.outputPort=null;
this.setDimension(50,50);
};
Start.prototype=new ImageFigure();
Start.prototype.type="Start";
Start.prototype.setWorkflow=function(_394f){
ImageFigure.prototype.setWorkflow.call(this,_394f);
if(_394f!==null&&this.outputPort===null){
this.outputPort=new MyOutputPort();
this.outputPort.setMaxFanOut(5);
this.outputPort.setWorkflow(_394f);
this.outputPort.setBackgroundColor(new Color(245,115,115));
this.outputPort.setName("output");
this.addPort(this.outputPort,this.width,this.height/2);
}
};
