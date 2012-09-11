ToolRedo=function(_43ce){
Button.call(this,_43ce);
};
ToolRedo.prototype=new Button();
ToolRedo.prototype.type="ToolRedo";
ToolRedo.prototype.execute=function(){
this.palette.workflow.getCommandStack().redo();
ToolGeneric.prototype.execute.call(this);
};
