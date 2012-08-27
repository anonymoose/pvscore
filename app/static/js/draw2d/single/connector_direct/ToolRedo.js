ToolRedo=function(_39f6){
Button.call(this,_39f6);
};
ToolRedo.prototype=new Button();
ToolRedo.prototype.type="ToolRedo";
ToolRedo.prototype.execute=function(){
this.palette.workflow.getCommandStack().redo();
ToolGeneric.prototype.execute.call(this);
};
