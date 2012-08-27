ToolOval=function(_3b89){
ToolGeneric.call(this,_3b89);
this.setDimension(24,24);
};
ToolOval.prototype=new ToolGeneric();
ToolOval.prototype.type="ToolOval";
ToolOval.prototype.execute=function(x,y){
var _3b8c=new Oval();
_3b8c.setDimension(100,60);
_3b8c.setBackgroundColor(new Color(255,255,255));
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_3b8c,x,y));
ToolGeneric.prototype.execute.call(this,x,y);
};
