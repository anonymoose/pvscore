MyOutputPort=function(_3c32){
OutputPort.call(this,_3c32);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.type="MyOutputPort";
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3c34=new CommandConnect(this.parentNode.workflow,this,port);
_3c34.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_3c34);
}
};
