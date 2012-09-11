ToolRectangle=function(_3ddb){
ToolGeneric.call(this,_3ddb);
this.setDimension(24,24);
};
ToolRectangle.prototype=new ToolGeneric;
ToolRectangle.prototype.type="ToolRectangle";
ToolRectangle.prototype.execute=function(x,y){
var _3dde=new Rectangle();
_3dde.setDimension(100,60);
_3dde.setBackgroundColor(new Color(255,255,255));
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_3dde,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
