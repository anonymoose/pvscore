/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

MyGraphicalEditorFactory=function(){EditPartFactory.call(this);};MyGraphicalEditorFactory.prototype=new EditPartFactory();MyGraphicalEditorFactory.prototype.type="MyGraphicalEditorFactory";MyGraphicalEditorFactory.prototype.createEditPart=function(_22){var _23;if(_22 instanceof TableModel){_23=new TableFigure();}if(_22 instanceof ForeignKeyModel){_23=new ForeignKeyFigure();}if(_23===null){alert("factory called with unknown model class:"+_22.type);}_23.setModel(_22);return _23;};