End=function(){
Node.call(this);
this.inputPort1=null;
this.inputPort2=null;
this.setDimension(50,50);
};
End.prototype=new Node;
End.prototype.type="End";
End.prototype.setWorkflow=function(_3679){
Node.prototype.setWorkflow.call(this,_3679);
if(_3679!==null){
this.inputPort1=new InputPort();
this.inputPort1.setWorkflow(_3679);
this.inputPort1.setBackgroundColor(new Color(115,115,245));
this.addPort(this.inputPort1,0,this.height/3);
this.inputPort2=new InputPort();
this.inputPort2.setWorkflow(_3679);
this.inputPort2.setBackgroundColor(new Color(115,115,245));
this.addPort(this.inputPort2,0,this.height/3*2);
}
};
End.prototype.setDimension=function(w,h){
Node.prototype.setDimension.call(this,w,h);
if(this.inputPort1!==null){
this.inputPort1.setPosition(0,this.height/3);
this.inputPort2.setPosition(0,this.height/3*2);
}
};
