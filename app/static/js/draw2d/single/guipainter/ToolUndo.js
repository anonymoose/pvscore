ToolUndo=function(_445b){
Button.call(this,_445b);
};
ToolUndo.prototype=new Button();
ToolUndo.prototype.type="ToolUndo";
ToolUndo.prototype.execute=function(){
this.palette.workflow.getCommandStack().undo();
ToolGeneric.prototype.execute.call(this);
};
