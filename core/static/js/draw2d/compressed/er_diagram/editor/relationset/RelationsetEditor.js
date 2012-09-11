/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

RelationsetEditor=function(id,_a21){Workflow.call(this,id);this.relationset=_a21;var _a22=this.relationset.getTableAliasModels();for(var i=0;i<_a22.getSize();i++){var _a24=new TableAliasFigure(_a22.get(i));this.addFigure(_a24);}};RelationsetEditor.prototype=new Workflow();RelationsetEditor.prototype.type="RelationsetEditor";