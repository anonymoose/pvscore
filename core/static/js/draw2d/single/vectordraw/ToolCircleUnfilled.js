ToolCircleUnfilled=function(_42ea){
ToolGeneric.call(this,_42ea);
this.setDimension(24,24);
};
ToolCircleUnfilled.prototype=new ToolGeneric();
ToolCircleUnfilled.prototype.type="ToolCircleUnfilled";
ToolCircleUnfilled.prototype.execute=function(x,y){
var _42ed=new Circle();
_42ed.setDimension(100,100);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_42ed,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
