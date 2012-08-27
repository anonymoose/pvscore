InputFieldFigure=function(){
InputPort.call(this);
};
InputFieldFigure.prototype=new InputPort();
InputFieldFigure.prototype.type="InputFieldFigure";
InputFieldFigure.prototype.createCommand=function(_42b3){
if(_42b3.getPolicy()==EditPolicy.CONNECT){
if(_42b3.source.parentNode.id==_42b3.target.parentNode.id){
return null;
}
if(_42b3.source instanceof OutputPort){
return new CommandConnect(_42b3.canvas,_42b3.source,_42b3.target);
}
}
return InputPort.prototype.createCommand.call(this,_42b3);
};
