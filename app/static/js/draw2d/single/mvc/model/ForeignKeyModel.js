ForeignKeyModel=function(_3b8f,_3b90,_3b91,_3b92){
AbstractConnectionModel.call(this);
this.fromTable=_3b91;
this.fromField=_3b92;
this.toTable=_3b8f;
this.toField=_3b90;
};
ForeignKeyModel.prototype=new AbstractConnectionModel();
ForeignKeyModel.prototype.type="ForeignKeyModel";
ForeignKeyModel.prototype.getSourceModel=function(){
return this.getDatabaseModel().getTableModel(this.toTable);
};
ForeignKeyModel.prototype.getTargetModel=function(){
return this.getDatabaseModel().getTableModel(this.fromTable);
};
ForeignKeyModel.prototype.getSourcePortName=function(){
return "out_"+this.toField;
};
ForeignKeyModel.prototype.getTargetPortName=function(){
return "in_"+this.fromField;
};
ForeignKeyModel.prototype.getDatabaseModel=function(){
return this.getModelParent().getDatabaseModel();
};
ForeignKeyModel.prototype.getPersistentAttributes=function(){
var att=AbstractObjectModel.prototype.getPersistentAttributes.call(this);
att.fromTable=this.fromTable;
att.fromField=this.fromField;
att.toTable=this.toTable;
att.toField=this.toField;
return att;
};
