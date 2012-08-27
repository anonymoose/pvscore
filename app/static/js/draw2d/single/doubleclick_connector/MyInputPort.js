MyInputPort=function(_3e22){
InputPort.call(this,_3e22);
};
MyInputPort.prototype=new InputPort();
MyInputPort.prototype.type="MyInputPort";
MyInputPort.prototype.onDrop=function(port){
if(port.getMaxFanOut&&port.getMaxFanOut()<=port.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3e24=new CommandConnect(this.parentNode.workflow,port,this);
_3e24.setConnection(new DoubleclickConnection());
this.parentNode.workflow.getCommandStack().execute(_3e24);
}
};
