MyOutputPort=function(_42e6){
OutputPort.call(this,_42e6);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _42e8=new CommandConnect(this.parentNode.workflow,this,port);
_42e8.setConnection(new DoubleclickConnection());
this.parentNode.workflow.getCommandStack().execute(_42e8);
}
};
