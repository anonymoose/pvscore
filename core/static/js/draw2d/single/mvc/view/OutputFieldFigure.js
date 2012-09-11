OutputFieldFigure=function(){
OutputPort.call(this);
};
OutputFieldFigure.prototype=new OutputPort();
OutputFieldFigure.prototype.createCommand=function(_42e9){
if(_42e9.getPolicy()==EditPolicy.CONNECT){
if(_42e9.source.parentNode.id==_42e9.target.parentNode.id){
return null;
}
if(_42e9.source instanceof InputPort){
return new CommandConnect(_42e9.canvas,_42e9.target,_42e9.source);
}
return null;
}
return Port.prototype.createCommand.call(this,_42e9);
};
