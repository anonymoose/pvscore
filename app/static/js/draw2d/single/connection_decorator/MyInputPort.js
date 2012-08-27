MyInputPort=function(_3b7a){
InputPort.call(this,_3b7a);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.type="MyInputPort";
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3b7c=new CommandConnect(this.parentNode.workflow,port,this);
_3b7c.setConnection(new DecoratedConnection());
this.parentNode.workflow.getCommandStack().execute(_3b7c);
}
};
