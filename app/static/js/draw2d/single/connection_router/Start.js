Start=function(){
ImageFigure.call(this,this.type+".png");
this.outputPort=null;
this.setDimension(50,50);
};
Start.prototype=new ImageFigure();
Start.prototype.type="Start";
Start.prototype.setWorkflow=function(_3729){
ImageFigure.prototype.setWorkflow.call(this,_3729);
if(_3729!==null&&this.outputPort===null){
this.outputPort=new MyOutputPort();
this.outputPort.setWorkflow(_3729);
this.outputPort.setMaxFanOut(4);
this.outputPort.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort,this.width,this.height/2);
this.outputPort1=new MyOutputPort();
this.outputPort1.setWorkflow(_3729);
this.outputPort1.setMaxFanOut(4);
this.outputPort1.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort1,this.width/2,0);
this.outputPort2=new MyOutputPort();
this.outputPort2.setWorkflow(_3729);
this.outputPort2.setMaxFanOut(4);
this.outputPort2.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort2,this.width/2,this.height);
this.outputPort3=new MyOutputPort();
this.outputPort3.setWorkflow(_3729);
this.outputPort3.setMaxFanOut(4);
this.outputPort3.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort3,0,this.height/2);
}
};
