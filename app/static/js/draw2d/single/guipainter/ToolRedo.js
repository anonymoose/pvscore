ToolRedo=function(_3d99){
Button.call(this,_3d99);
};
ToolRedo.prototype=new Button();
ToolRedo.prototype.type="ToolRedo";
ToolRedo.prototype.execute=function(){
this.palette.workflow.getCommandStack().redo();
ToolGeneric.prototype.execute.call(this);
};
