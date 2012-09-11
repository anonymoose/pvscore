MyOutputPort=function(_443c){
OutputPort.call(this,_443c);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.type="MyOutputPort";
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _443e=new CommandConnect(this.parentNode.workflow,this,port);
_443e.setConnection(new DecoratedConnection());
this.parentNode.workflow.getCommandStack().execute(_443e);
}
};
