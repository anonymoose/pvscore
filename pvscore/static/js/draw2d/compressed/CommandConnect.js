/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

CommandConnect=function(_1508,_1509,_150a){Command.call(this,"create connection");this.workflow=_1508;this.source=_1509;this.target=_150a;this.connection=null;};CommandConnect.prototype=new Command();CommandConnect.prototype.type="CommandConnect";CommandConnect.prototype.setConnection=function(_150b){this.connection=_150b;};CommandConnect.prototype.execute=function(){if(this.connection===null){this.connection=new Connection();}this.connection.setSource(this.source);this.connection.setTarget(this.target);this.workflow.addFigure(this.connection);};CommandConnect.prototype.redo=function(){this.workflow.addFigure(this.connection);this.connection.reconnect();};CommandConnect.prototype.undo=function(){this.workflow.removeFigure(this.connection);};