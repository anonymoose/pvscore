/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Port=function(_d0f,_d10){Corona=function(){};Corona.prototype=new Circle();Corona.prototype.setAlpha=function(_d11){Circle.prototype.setAlpha.call(this,Math.min(0.3,_d11));this.setDeleteable(false);this.setCanDrag(false);this.setResizeable(false);this.setSelectable(false);};if(_d0f===null||_d0f===undefined){this.currentUIRepresentation=new Circle();}else{this.currentUIRepresentation=_d0f;}if(_d10===null||_d10===undefined){this.connectedUIRepresentation=new Circle();this.connectedUIRepresentation.setColor(null);}else{this.connectedUIRepresentation=_d10;}this.disconnectedUIRepresentation=this.currentUIRepresentation;this.hideIfConnected=false;this.uiRepresentationAdded=true;this.parentNode=null;this.originX=0;this.originY=0;this.coronaWidth=10;this.corona=null;Rectangle.call(this);this.setDimension(8,8);this.setBackgroundColor(new Color(100,180,100));this.setColor(new Color(90,150,90));Rectangle.prototype.setColor.call(this,null);this.dropable=new DropTarget(this.html);this.dropable.node=this;this.dropable.addEventListener("dragenter",function(_d12){_d12.target.node.onDragEnter(_d12.relatedTarget.node);});this.dropable.addEventListener("dragleave",function(_d13){_d13.target.node.onDragLeave(_d13.relatedTarget.node);});this.dropable.addEventListener("drop",function(_d14){_d14.relatedTarget.node.onDrop(_d14.target.node);});};Port.prototype=new Rectangle();Port.prototype.type="Port";Port.ZOrderBaseIndex=5000;Port.setZOrderBaseIndex=function(_d15){Port.ZOrderBaseIndex=_d15;};Port.prototype.setHideIfConnected=function(flag){this.hideIfConnected=flag;};Port.prototype.dispose=function(){var size=this.moveListener.getSize();for(var i=0;i<size;i++){var _d19=this.moveListener.get(i);this.parentNode.workflow.removeFigure(_d19);_d19.dispose();}Rectangle.prototype.dispose.call(this);this.parentNode=null;this.dropable.node=null;this.dropable=null;this.disconnectedUIRepresentation.dispose();this.connectedUIRepresentation.dispose();};Port.prototype.createHTMLElement=function(){var item=Rectangle.prototype.createHTMLElement.call(this);item.style.zIndex=Port.ZOrderBaseIndex;this.currentUIRepresentation.html.zIndex=Port.ZOrderBaseIndex;item.appendChild(this.currentUIRepresentation.html);this.uiRepresentationAdded=true;return item;};Port.prototype.setUiRepresentation=function(_d1b){if(_d1b===null){_d1b=new Figure();}if(this.uiRepresentationAdded){this.html.removeChild(this.currentUIRepresentation.getHTMLElement());}this.html.appendChild(_d1b.getHTMLElement());_d1b.paint();this.currentUIRepresentation=_d1b;};Port.prototype.onMouseEnter=function(){this.setLineWidth(2);};Port.prototype.onMouseLeave=function(){this.setLineWidth(0);};Port.prototype.setDimension=function(_d1c,_d1d){Rectangle.prototype.setDimension.call(this,_d1c,_d1d);this.connectedUIRepresentation.setDimension(_d1c,_d1d);this.disconnectedUIRepresentation.setDimension(_d1c,_d1d);this.setPosition(this.x,this.y);};Port.prototype.setBackgroundColor=function(_d1e){this.currentUIRepresentation.setBackgroundColor(_d1e);};Port.prototype.getBackgroundColor=function(){return this.currentUIRepresentation.getBackgroundColor();};Port.prototype.getConnections=function(){var _d1f=new ArrayList();var size=this.moveListener.getSize();for(var i=0;i<size;i++){var _d22=this.moveListener.get(i);if(_d22 instanceof Connection){_d1f.add(_d22);}}return _d1f;};Port.prototype.setColor=function(_d23){this.currentUIRepresentation.setColor(_d23);};Port.prototype.getColor=function(){return this.currentUIRepresentation.getColor();};Port.prototype.setLineWidth=function(_d24){this.currentUIRepresentation.setLineWidth(_d24);};Port.prototype.getLineWidth=function(){return this.currentUIRepresentation.getLineWidth();};Port.prototype.paint=function(){try{this.currentUIRepresentation.paint();}catch(e){pushErrorStack(e,"Port.prototype.paint=function()");}};Port.prototype.setPosition=function(xPos,yPos){this.originX=xPos;this.originY=yPos;Rectangle.prototype.setPosition.call(this,xPos,yPos);if(this.html===null){return;}this.html.style.left=(this.x-this.getWidth()/2)+"px";this.html.style.top=(this.y-this.getHeight()/2)+"px";};Port.prototype.setParent=function(_d27){if(this.parentNode!==null){this.parentNode.detachMoveListener(this);}this.parentNode=_d27;if(this.parentNode!==null){this.parentNode.attachMoveListener(this);}};Port.prototype.attachMoveListener=function(_d28){Rectangle.prototype.attachMoveListener.call(this,_d28);if(this.hideIfConnected==true){this.setUiRepresentation(this.connectedUIRepresentation);}};Port.prototype.detachMoveListener=function(_d29){Rectangle.prototype.detachMoveListener.call(this,_d29);if(this.getConnections().getSize()==0){this.setUiRepresentation(this.disconnectedUIRepresentation);}};Port.prototype.getParent=function(){return this.parentNode;};Port.prototype.onDrag=function(){Rectangle.prototype.onDrag.call(this);this.parentNode.workflow.showConnectionLine(this.parentNode.x+this.x,this.parentNode.y+this.y,this.parentNode.x+this.originX,this.parentNode.y+this.originY);};Port.prototype.getCoronaWidth=function(){return this.coronaWidth;};Port.prototype.setCoronaWidth=function(_d2a){this.coronaWidth=_d2a;};Port.prototype.setOrigin=function(x,y){this.originX=x;this.originY=y;};Port.prototype.onDragend=function(){this.setAlpha(1);this.setPosition(this.originX,this.originY);this.parentNode.workflow.hideConnectionLine();document.body.focus();};Port.prototype.onDragEnter=function(port){var _d2e=new EditPolicy(EditPolicy.CONNECT);_d2e.canvas=this.parentNode.workflow;_d2e.source=port;_d2e.target=this;var _d2f=this.createCommand(_d2e);if(_d2f===null){return;}this.parentNode.workflow.connectionLine.setColor(new Color(0,150,0));this.parentNode.workflow.connectionLine.setLineWidth(3);this.showCorona(true);};Port.prototype.onDragLeave=function(port){this.parentNode.workflow.connectionLine.setColor(new Color(0,0,0));this.parentNode.workflow.connectionLine.setLineWidth(1);this.showCorona(false);};Port.prototype.onDrop=function(port){var _d32=new EditPolicy(EditPolicy.CONNECT);_d32.canvas=this.parentNode.workflow;_d32.source=port;_d32.target=this;var _d33=this.createCommand(_d32);if(_d33!==null){this.parentNode.workflow.getCommandStack().execute(_d33);}};Port.prototype.getAbsolutePosition=function(){return new Point(this.getAbsoluteX(),this.getAbsoluteY());};Port.prototype.getAbsoluteBounds=function(){return new Dimension(this.getAbsoluteX(),this.getAbsoluteY(),this.getWidth(),this.getHeight());};Port.prototype.getAbsoluteY=function(){return this.originY+this.parentNode.getY();};Port.prototype.getAbsoluteX=function(){return this.originX+this.parentNode.getX();};Port.prototype.onOtherFigureMoved=function(_d34){this.fireMoveEvent();};Port.prototype.getName=function(){return this.name;};Port.prototype.setName=function(name){this.name=name;};Port.prototype.isOver=function(iX,iY){var x=this.getAbsoluteX()-this.coronaWidth-this.getWidth()/2;var y=this.getAbsoluteY()-this.coronaWidth-this.getHeight()/2;var iX2=x+this.width+(this.coronaWidth*2)+this.getWidth()/2;var iY2=y+this.height+(this.coronaWidth*2)+this.getHeight()/2;return (iX>=x&&iX<=iX2&&iY>=y&&iY<=iY2);};Port.prototype.showCorona=function(flag,_d3d){if(flag===true){this.corona=new Corona();this.corona.setAlpha(0.3);this.corona.setBackgroundColor(new Color(0,125,125));this.corona.setColor(null);this.corona.setDimension(this.getWidth()+(this.getCoronaWidth()*2),this.getWidth()+(this.getCoronaWidth()*2));this.parentNode.getWorkflow().addFigure(this.corona,this.getAbsoluteX()-this.getCoronaWidth()-this.getWidth()/2,this.getAbsoluteY()-this.getCoronaWidth()-this.getHeight()/2);}else{if(flag===false&&this.corona!==null){this.parentNode.getWorkflow().removeFigure(this.corona);this.corona=null;}}};Port.prototype.createCommand=function(_d3e){if(_d3e.getPolicy()===EditPolicy.MOVE){if(!this.canDrag){return null;}return new CommandMovePort(this);}if(_d3e.getPolicy()===EditPolicy.CONNECT){if(_d3e.source.parentNode.id===_d3e.target.parentNode.id){return null;}else{return new CommandConnect(_d3e.canvas,_d3e.source,_d3e.target);}}return null;};