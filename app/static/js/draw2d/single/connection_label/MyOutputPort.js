MyOutputPort=function(_3dea){
OutputPort.call(this,_3dea);
};
MyOutputPort.prototype=new OutputPort();
MyOutputPort.prototype.onDrop=function(port){
if(this.getMaxFanOut()<=this.getFanOut()){
return;
}
if(this.parentNode.id==port.parentNode.id){
}else{
var _3dec=new CommandConnect(this.parentNode.workflow,this,port);
_3dec.setConnection(new DoubleclickConnection());
this.parentNode.workflow.getCommandStack().execute(_3dec);
}
};
