ToolGroup=function(_39f7){
ToolGeneric.call(this,_39f7);
this.setTooltip("Form Group");
};
ToolGroup.prototype=new ToolGeneric;
ToolGroup.prototype.type="ToolGroup";
ToolGroup.prototype.execute=function(x,y){
var _39fa=new GroupFigure();
_39fa.setDimension(100,60);
var _39fb=this.palette.workflow.getBestCompartmentFigure(x,y);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_39fa,x,y,_39fb));
ToolGeneric.prototype.execute.call(this,x,y);
};
