/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

RelationsetModel=function(){this.relations=new ArrayList();this.nonPersistentTableAliases=new ArrayList();};RelationsetModel.prototype.type="RelationsetModel";RelationsetModel.prototype.getRelationModels=function(){return this.relations;};RelationsetModel.prototype.getTableAliasModels=function(){return this.nonPersistentTableAliases;};RelationsetModel.prototype.addRelationModel=function(_18ae){this.relations.add(_18ae);if(this.nonPersistentTableAliases.indexOf(_18ae.getToTableModel())<=0){this.nonPersistentTableAliases.add(_18ae.getToTableModel());}if(this.nonPersistentTableAliases.indexOf(_18ae.getFromTableModel())<=0){this.nonPersistentTableAliases.add(_18ae.getFromTableModel());}};RelationsetModel.prototype.getPosition=function(_18af){return new Point(100,100);};