ToolRedo=function(_3e3b){
Button.call(this,_3e3b);
};
ToolRedo.prototype=new Button();
ToolRedo.prototype.type="ToolRedo";
ToolRedo.prototype.execute=function(){
this.palette.workflow.getCommandStack().redo();
ToolGeneric.prototype.execute.call(this);
};
