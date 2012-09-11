MyOutputPort=function(_3e30){
OutputPort.call(this,_3e30);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3e32=new CommandConnect(this.parentNode.workflow,this,port);
_3e32.setConnection(new DecoratedConnection());
this.parentNode.workflow.getCommandStack().execute(_3e32);
}
};
