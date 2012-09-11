Start=function(){
Node.call(this);
this.outputPort1=null;
this.outputPort2=null;
this.setDimension(50,50);
};
Start.prototype=new Node;
Start.prototype.type="Start";
Start.prototype.setWorkflow=function(_3b7d){
Node.prototype.setWorkflow.call(this,_3b7d);
if(_3b7d!==null){
this.outputPort1=new OutputPort();
this.outputPort1.setMaxFanOut(1);
this.outputPort1.setWorkflow(_3b7d);
this.outputPort1.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort1,this.width,this.height/3);
this.outputPort2=new OutputPort();
this.outputPort2.setMaxFanOut(1);
this.outputPort2.setWorkflow(_3b7d);
this.outputPort2.setBackgroundColor(new Color(245,115,115));
this.addPort(this.outputPort2,this.width,this.height/3*2);
}
};
Start.prototype.setDimension=function(w,h){
Node.prototype.setDimension.call(this,w,h);
if(this.outputPort1!==null){
this.outputPort1.setPosition(this.width,this.height/3);
this.outputPort2.setPosition(this.width,this.height/3*2);
}
};
