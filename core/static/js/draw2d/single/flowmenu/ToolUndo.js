ToolUndo=function(_4631){
Button.call(this,_4631);
};
ToolUndo.prototype=new Button();
ToolUndo.prototype.type="ToolUndo";
ToolUndo.prototype.execute=function(){
this.palette.workflow.getCommandStack().undo();
ToolGeneric.prototype.execute.call(this);
};
