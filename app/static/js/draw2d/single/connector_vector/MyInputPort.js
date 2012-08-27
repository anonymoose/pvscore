MyInputPort=function(_366c){
InputPort.call(this,_366c);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _366e=new CommandConnect(this.parentNode.workflow,port,this);
_366e.setConnection(new ArrowConnection());
this.parentNode.workflow.getCommandStack().execute(_366e);
}
};
