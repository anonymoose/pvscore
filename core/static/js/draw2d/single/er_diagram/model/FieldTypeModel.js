FieldTypeModel=function(name){
this.name=name;
this.parent=null;
};
FieldTypeModel.prototype.type="FieldTypeModel";
FieldTypeModel.prototype.getName=function(){
return this.name;
};
FieldTypeModel.prototype.setParent=function(_3185){
if(!(_3185 instanceof FieldModel)){
throw "Invalid parameter type in [FieldTypeModelBoolean.prototype.setParent]";
}
this.parent=_3185;
};
