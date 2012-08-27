ToolUndo=function(_3624){
Button.call(this,_3624);
};
ToolUndo.prototype=new Button();
ToolUndo.prototype.type="ToolUndo";
ToolUndo.prototype.execute=function(){
this.palette.workflow.getCommandStack().undo();
ToolGeneric.prototype.execute.call(this);
};
