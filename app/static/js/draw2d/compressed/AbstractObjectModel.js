/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

AbstractObjectModel=function(){this.listeners=new ArrayList();this.id=UUID.create();};AbstractObjectModel.EVENT_ELEMENT_ADDED="element added";AbstractObjectModel.EVENT_ELEMENT_REMOVED="element removed";AbstractObjectModel.EVENT_CONNECTION_ADDED="connection addedx";AbstractObjectModel.EVENT_CONNECTION_REMOVED="connection removed";AbstractObjectModel.prototype.type="AbstractObjectModel";AbstractObjectModel.prototype.getModelChildren=function(){return new ArrayList();};AbstractObjectModel.prototype.getModelParent=function(){return this.modelParent;};AbstractObjectModel.prototype.setModelParent=function(_d06){this.modelParent=_d06;};AbstractObjectModel.prototype.getId=function(){return this.id;};AbstractObjectModel.prototype.firePropertyChange=function(_d07,_d08,_d09){var _d0a=this.listeners.getSize();if(_d0a===0){return;}var _d0b=new PropertyChangeEvent(this,_d07,_d08,_d09);for(var i=0;i<_d0a;i++){try{this.listeners.get(i).propertyChange(_d0b);}catch(e){alert("Method: AbstractObjectModel.prototype.firePropertyChange\n"+e+"\nProperty: "+_d07+"\nListener Class:"+this.listeners.get(i).type);}}};AbstractObjectModel.prototype.addPropertyChangeListener=function(_d0d){if(_d0d!==null){this.listeners.add(_d0d);}};AbstractObjectModel.prototype.removePropertyChangeListener=function(_d0e){if(_d0e!==null){this.listeners.remove(_d0e);}};AbstractObjectModel.prototype.getPersistentAttributes=function(){return {id:this.id};};