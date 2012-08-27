ButtonMoveBack=function(_371c){
Button.call(this,_371c,16,16);
};
ButtonMoveBack.prototype=new Button();
ButtonMoveBack.prototype.type="ButtonMoveBack";
ButtonMoveBack.prototype.execute=function(){
this.palette.workflow.moveBack(this.palette.workflow.getCurrentSelection());
ToolGeneric.prototype.execute.call(this);
};
