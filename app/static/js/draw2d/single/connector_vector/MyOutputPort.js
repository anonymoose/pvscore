MyOutputPort=function(_4448){
OutputPort.call(this,_4448);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _444a=new CommandConnect(this.parentNode.workflow,this,port);
_444a.setConnection(new ArrowConnection());
this.parentNode.workflow.getCommandStack().execute(_444a);
}
};
