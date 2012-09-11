ToolClear=function(_3168){
Button.call(this,_3168);
};
ToolClear.prototype=new Button();
ToolClear.prototype.type="ToolClear";
ToolClear.prototype.execute=function(){
this.palette.workflow.clear();
ToolGeneric.prototype.execute.call(this);
};
