ToolRectangleUnfilled=function(_4441){
ToolGeneric.call(this,_4441);
this.setDimension(24,24);
};
ToolRectangleUnfilled.prototype=new ToolGeneric;
ToolRectangleUnfilled.prototype.type="ToolRectangleUnfilled";
ToolRectangleUnfilled.prototype.execute=function(x,y){
var _4444=new Rectangle();
_4444.setDimension(100,60);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_4444,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
