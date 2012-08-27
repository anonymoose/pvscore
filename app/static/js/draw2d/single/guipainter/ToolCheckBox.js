ToolCheckBox=function(_42c4){
ToolGeneric.call(this,_42c4);
};
ToolCheckBox.prototype=new ToolGeneric;
ToolCheckBox.prototype.type="ToolCheckBox";
ToolCheckBox.prototype.execute=function(x,y){
var _42c7=new CheckBoxFigure();
_42c7.setDimension(100,20);
var _42c8=this.palette.workflow.getBestCompartmentFigure(x,y);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_42c7,x,y,_42c8));
ToolGeneric.prototype.execute.call(this,x,y);
};
