ToolRedo=function(_3d70){
Button.call(this,_3d70);
this.setDimension(24,24);
};
ToolRedo.prototype=new Button();
ToolRedo.prototype.type="ToolRedo";
ToolRedo.prototype.execute=function(){
this.getWorkflow().getCommandStack().redo();
};
