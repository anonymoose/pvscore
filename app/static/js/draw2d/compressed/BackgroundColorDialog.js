/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

BackgroundColorDialog=function(_5bf){ColorDialog.call(this);this.figure=_5bf;var _5c0=_5bf.getBackgroundColor();if(_5c0!==null){this.updateH(this.rgb2hex(_5c0.getRed(),_5c0.getGreen(),_5c0.getBlue()));}};BackgroundColorDialog.prototype=new ColorDialog();BackgroundColorDialog.prototype.type="BackgroundColorDialog";BackgroundColorDialog.prototype.onOk=function(){var _5c1=this.workflow;ColorDialog.prototype.onOk.call(this);if(typeof this.figure.setBackgroundColor=="function"){_5c1.getCommandStack().execute(new CommandSetBackgroundColor(this.figure,this.getSelectedColor()));if(_5c1.getCurrentSelection()==this.figure){_5c1.setCurrentSelection(this.figure);}}};