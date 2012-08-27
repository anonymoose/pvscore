MyInputPort=function(_42b4){
InputPort.call(this,_42b4);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.type="MyInputPort";
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _42b6=new CommandConnect(this.parentNode.workflow,port,this);
_42b6.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_42b6);
}
};
