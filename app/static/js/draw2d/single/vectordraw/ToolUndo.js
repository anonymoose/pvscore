ToolUndo=function(_4279){
Button.call(this,_4279);
this.setDimension(24,24);
};
ToolUndo.prototype=new Button();
ToolUndo.prototype.type="ToolUndo";
ToolUndo.prototype.execute=function(){
this.getWorkflow().getCommandStack().undo();
};
