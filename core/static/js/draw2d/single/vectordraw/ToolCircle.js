ToolCircle=function(_3838){
ToolGeneric.call(this,_3838);
this.setDimension(24,24);
};
ToolCircle.prototype=new ToolGeneric();
ToolCircle.prototype.type="ToolCircle";
ToolCircle.prototype.execute=function(x,y){
var _383b=new Circle();
_383b.setDimension(100,100);
_383b.setBackgroundColor(new Color(255,255,255));
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_383b,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
