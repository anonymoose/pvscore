MyInputPort=function(_316e){
InputPort.call(this,_316e);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.type="MyInputPort";
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3170=new CommandConnect(this.parentNode.workflow,port,this);
_3170.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_3170);
}
};
