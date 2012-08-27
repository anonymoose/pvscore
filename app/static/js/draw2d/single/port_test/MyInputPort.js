MyInputPort=function(_4493){
InputPort.call(this,_4493);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _4495=new CommandConnect(this.parentNode.workflow,port,this);
_4495.setConnection(new DecoratedConnection());
this.parentNode.workflow.getCommandStack().execute(_4495);
}
};
