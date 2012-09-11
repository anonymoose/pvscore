ToolInputBox=function(_33c5){
ToolGeneric.call(this,_33c5);
};
ToolInputBox.prototype=new ToolGeneric;
ToolInputBox.prototype.type="ToolInputBox";
ToolInputBox.prototype.execute=function(x,y){
var _33c8=new InputBoxFigure();
_33c8.setDimension(100,20);
var _33c9=this.palette.workflow.getBestCompartmentFigure(x,y);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_33c8,x,y,_33c9));
ToolGeneric.prototype.execute.call(this,x,y);
};
