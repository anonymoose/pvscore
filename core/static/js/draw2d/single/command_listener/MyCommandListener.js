MyCommandListener=function(){
CommandStackEventListener.call(this);
};
MyCommandListener.prototype=new CommandStackEventListener;
MyCommandListener.prototype.type="MyCommandListener";
MyCommandListener.prototype.stackChanged=function(event){
var _42e2=document.getElementById("log");
var log=document.createElement("div");
if(event.isPostChangeEvent()){
log.innerHTML="POST:";
}else{
log.innerHTML="PRE:";
}
var _42e4=event.getDetails();
if(0!=(_42e4&(CommandStack.PRE_EXECUTE|CommandStack.POST_EXECUTE))){
log.innerHTML=log.innerHTML+" EXECUTE";
}else{
if(0!=(_42e4&(CommandStack.PRE_UNDO|CommandStack.POST_UNDO))){
log.innerHTML=log.innerHTML+" UNDO";
}else{
if(0!=(_42e4&(CommandStack.PRE_REDO|CommandStack.POST_REDO))){
log.innerHTML=log.innerHTML+" REDO";
}
}
}
var _42e5=event.getCommand();
if(_42e5 instanceof CommandAdd){
log.innerHTML=log.innerHTML+" => ADD Element";
}else{
if(_42e5 instanceof CommandConnect){
log.innerHTML=log.innerHTML+" => Connect two Ports";
}else{
if(_42e5 instanceof CommandDelete){
log.innerHTML=log.innerHTML+" => Delete Element";
}else{
if(_42e5 instanceof CommandMove){
log.innerHTML=log.innerHTML+" => Moving Element";
}else{
if(_42e5 instanceof CommandResize){
log.innerHTML=log.innerHTML+" => Resize Element";
}
}
}
}
}
_42e2.appendChild(log);
};
