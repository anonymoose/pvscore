ToolOvalUnfilled=function(_3d54){
ToolGeneric.call(this,_3d54);
this.setDimension(24,24);
};
ToolOvalUnfilled.prototype=new ToolGeneric();
ToolOvalUnfilled.prototype.type="ToolOvalUnfilled";
ToolOvalUnfilled.prototype.execute=function(x,y){
var _3d57=new Oval();
_3d57.setDimension(100,60);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_3d57,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
