ToolFormButton=function(_3c0d){
ToolGeneric.call(this,_3c0d);
};
ToolFormButton.prototype=new ToolGeneric;
ToolFormButton.prototype.type="ToolFormButton";
ToolFormButton.prototype.execute=function(x,y){
var _3c10=new ButtonFigure();
_3c10.setDimension(100,20);
var _3c11=this.palette.workflow.getBestCompartmentFigure(x,y);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_3c10,x,y,_3c11));
ToolGeneric.prototype.execute.call(this,x,y);
};
