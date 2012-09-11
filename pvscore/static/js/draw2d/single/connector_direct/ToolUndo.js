ToolUndo=function(_367c){
Button.call(this,_367c);
};
ToolUndo.prototype=new Button();
ToolUndo.prototype.type="ToolUndo";
ToolUndo.prototype.execute=function(){
this.palette.workflow.getCommandStack().undo();
ToolGeneric.prototype.execute.call(this);
};
