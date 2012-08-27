MyInputPort=function(_4496){
InputPort.call(this,_4496);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.type="MyInputPort";
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _4498=new CommandConnect(this.parentNode.workflow,port,this);
_4498.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_4498);
}
};
