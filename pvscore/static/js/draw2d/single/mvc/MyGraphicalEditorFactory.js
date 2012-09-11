MyGraphicalEditorFactory=function(){
EditPartFactory.call(this);
};
MyGraphicalEditorFactory.prototype=new EditPartFactory();
MyGraphicalEditorFactory.prototype.type="MyGraphicalEditorFactory";
MyGraphicalEditorFactory.prototype.createEditPart=function(model){
var _3183;
if(model instanceof TableModel){
_3183=new TableFigure();
}
if(model instanceof ForeignKeyModel){
_3183=new ForeignKeyFigure();
}
if(_3183===null){
alert("factory called with unknown model class:"+model.type);
}
_3183.setModel(model);
return _3183;
};
