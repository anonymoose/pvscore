ToolUseGeometry=function(_3b8e){
ToggleButton.call(this,_3b8e);
};
ToolUseGeometry.prototype=new ToggleButton();
ToolUseGeometry.prototype.type="ToolUseGeometry";
ToolUseGeometry.prototype.execute=function(){
this.getToolPalette().getWorkflow().setSnapToGeometry(this.isDown());
};
