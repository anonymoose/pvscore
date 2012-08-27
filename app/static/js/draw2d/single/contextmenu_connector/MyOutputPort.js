MyOutputPort=function(_3e45){
OutputPort.call(this,_3e45);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.type="MyOutputPort";
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3e47=new CommandConnect(this.parentNode.workflow,this,port);
_3e47.setConnection(new ContextmenuConnection());
this.parentNode.workflow.getCommandStack().execute(_3e47);
}
};
