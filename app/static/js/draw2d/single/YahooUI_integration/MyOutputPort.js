MyOutputPort=function(_42ee){
OutputPort.call(this,_42ee);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.type="MyOutputPort";
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _42f0=new CommandConnect(this.parentNode.workflow,this,port);
_42f0.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_42f0);
}
};
