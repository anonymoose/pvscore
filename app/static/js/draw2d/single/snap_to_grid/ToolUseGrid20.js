ToolUseGrid20=function(_3e52){
ToggleButton.call(this,_3e52);
};
ToolUseGrid20.prototype=new ToggleButton();
ToolUseGrid20.prototype.type="ToolUseGrid20";
ToolUseGrid20.prototype.execute=function(){
if(this.isDown()){
this.getToolPalette().getWorkflow().setBackgroundImage("grid_20.png",true);
}else{
this.getToolPalette().getWorkflow().setBackgroundImage(null,false);
}
this.getToolPalette().getWorkflow().setGridWidth(20,20);
this.getToolPalette().getWorkflow().setSnapToGrid(this.isDown());
this.getToolPalette().tool1.setActive(false);
};
