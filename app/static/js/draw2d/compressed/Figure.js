/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

Figure=function(){this.construct();};Figure.prototype.type="Figure";Figure.ZOrderBaseIndex=100;Figure.setZOrderBaseIndex=function(_ad7){Figure.ZOrderBaseIndex=_ad7;};Figure.prototype.construct=function(){this.lastDragStartTime=0;this.x=0;this.y=0;this.width=10;this.height=10;this.border=null;this.id=UUID.create();this.html=this.createHTMLElement();this.canvas=null;this.workflow=null;this.draggable=null;this.parent=null;this.isMoving=false;this.canSnapToHelper=true;this.snapToGridAnchor=new Point(0,0);this.timer=-1;this.model=null;this.alpha=1;this.alphaBeforeOnDrag=1;this.properties={};this.moveListener=new ArrayList();this.setDimension(this.width,this.height);this.setDeleteable(true);this.setCanDrag(true);this.setResizeable(true);this.setSelectable(true);};Figure.prototype.dispose=function(){this.canvas=null;this.workflow=null;this.moveListener=null;if(this.draggable!==null){this.draggable.removeEventListener("mouseenter",this.tmpMouseEnter);this.draggable.removeEventListener("mouseleave",this.tmpMouseLeave);this.draggable.removeEventListener("dragend",this.tmpDragend);this.draggable.removeEventListener("dragstart",this.tmpDragstart);this.draggable.removeEventListener("drag",this.tmpDrag);this.draggable.removeEventListener("dblclick",this.tmpDoubleClick);this.draggable.node=null;this.draggable.target.removeAllElements();}this.draggable=null;if(this.border!==null){this.border.dispose();}this.border=null;if(this.parent!==null){this.parent.removeChild(this);}};Figure.prototype.getProperties=function(){return this.properties;};Figure.prototype.getProperty=function(key){return this.properties[key];};Figure.prototype.setProperty=function(key,_ada){this.properties[key]=_ada;this.setDocumentDirty();};Figure.prototype.getId=function(){return this.id;};Figure.prototype.setId=function(id){this.id=id;if(this.html!==null){this.html.id=id;}};Figure.prototype.setCanvas=function(_adc){this.canvas=_adc;};Figure.prototype.getWorkflow=function(){return this.workflow;};Figure.prototype.setWorkflow=function(_add){if(this.draggable===null){this.html.tabIndex="0";var _ade=this;this.keyDown=function(_adf){_adf.cancelBubble=true;_adf.returnValue=true;_ade.onKeyDown(_adf.keyCode,_adf.ctrlKey);};if(this.html.addEventListener){this.html.addEventListener("keydown",this.keyDown,false);}else{if(this.html.attachEvent){this.html.attachEvent("onkeydown",this.keyDown);}}this.draggable=new Draggable(this.html,Draggable.DRAG_X|Draggable.DRAG_Y);this.draggable.node=this;this.tmpContextMenu=function(_ae0){_ade.onContextMenu(_ade.x+_ae0.x,_ae0.y+_ade.y);};this.tmpMouseEnter=function(_ae1){_ade.onMouseEnter();};this.tmpMouseLeave=function(_ae2){_ade.onMouseLeave();};this.tmpDragend=function(_ae3){_ade.onDragend();};this.tmpDragstart=function(_ae4){var w=_ade.workflow;w.showMenu(null);if(w.toolPalette&&w.toolPalette.activeTool){_ae4.returnValue=false;w.onMouseDown(_ade.x+_ae4.x,_ae4.y+_ade.y);w.onMouseUp(_ade.x+_ae4.x,_ae4.y+_ade.y);return;}if(!(_ade instanceof ResizeHandle)&&!(_ade instanceof Port)){var line=w.getBestLine(_ade.x+_ae4.x,_ae4.y+_ade.y);if(line!==null){_ae4.returnValue=false;w.setCurrentSelection(line);w.showLineResizeHandles(line);w.onMouseDown(_ade.x+_ae4.x,_ae4.y+_ade.y);return;}else{if(_ade.isSelectable()){w.showResizeHandles(_ade);w.setCurrentSelection(_ade);}}}_ae4.returnValue=_ade.onDragstart(_ae4.x,_ae4.y);};this.tmpDrag=function(_ae7){_ade.onDrag();};this.tmpDoubleClick=function(_ae8){_ade.onDoubleClick();};this.draggable.addEventListener("contextmenu",this.tmpContextMenu);this.draggable.addEventListener("mouseenter",this.tmpMouseEnter);this.draggable.addEventListener("mouseleave",this.tmpMouseLeave);this.draggable.addEventListener("dragend",this.tmpDragend);this.draggable.addEventListener("dragstart",this.tmpDragstart);this.draggable.addEventListener("drag",this.tmpDrag);this.draggable.addEventListener("dblclick",this.tmpDoubleClick);}this.workflow=_add;};Figure.prototype.createHTMLElement=function(){var item=document.createElement("div");item.id=this.id;item.style.position="absolute";item.style.left=this.x+"px";item.style.top=this.y+"px";item.style.height=this.width+"px";item.style.width=this.height+"px";item.style.margin="0px";item.style.padding="0px";item.style.outline="none";item.style.zIndex=""+Figure.ZOrderBaseIndex;return item;};Figure.prototype.setParent=function(_aea){this.parent=_aea;};Figure.prototype.getParent=function(){return this.parent;};Figure.prototype.getZOrder=function(){return this.html.style.zIndex;};Figure.prototype.setZOrder=function(_aeb){this.html.style.zIndex=_aeb;};Figure.prototype.hasFixedPosition=function(){return false;};Figure.prototype.getMinWidth=function(){return 5;};Figure.prototype.getMinHeight=function(){return 5;};Figure.prototype.getHTMLElement=function(){if(this.html===null){this.html=this.createHTMLElement();}return this.html;};Figure.prototype.paint=function(){};Figure.prototype.setBorder=function(_aec){if(this.border!==null){this.border.figure=null;}this.border=_aec;this.border.figure=this;this.border.refresh();this.setDocumentDirty();};Figure.prototype.onRemove=function(_aed){};Figure.prototype.onContextMenu=function(x,y){var menu=this.getContextMenu();if(menu!==null){this.workflow.showMenu(menu,x,y);}};Figure.prototype.getContextMenu=function(){return null;};Figure.prototype.onDoubleClick=function(){};Figure.prototype.onMouseEnter=function(){};Figure.prototype.onMouseLeave=function(){};Figure.prototype.onDrag=function(){this.x=this.draggable.getLeft();this.y=this.draggable.getTop();if(this.isMoving==false){this.isMoving=true;this.alphaBeforeOnDrag=this.getAlpha();this.setAlpha(this.alphaBeforeOnDrag*0.5);}this.fireMoveEvent();};Figure.prototype.onDragend=function(){if(this.getWorkflow().getEnableSmoothFigureHandling()===true){var _af1=this;var _af2=function(){if(_af1.alpha<_af1.alphaBeforeOnDrag){_af1.setAlpha(Math.min(1,_af1.alpha+0.05));}else{window.clearInterval(_af1.timer);_af1.timer=-1;}};if(_af1.timer>0){window.clearInterval(_af1.timer);}_af1.timer=window.setInterval(_af2,20);}else{this.setAlpha(this.alphaBeforeOnDrag);}this.command.setPosition(this.x,this.y);this.workflow.commandStack.execute(this.command);this.command=null;this.isMoving=false;this.workflow.hideSnapToHelperLines();this.fireMoveEvent();};Figure.prototype.onDragstart=function(x,y){this.command=this.createCommand(new EditPolicy(EditPolicy.MOVE));return this.command!==null;};Figure.prototype.setCanDrag=function(flag){this.canDrag=flag;if(flag){this.html.style.cursor="move";}else{this.html.style.cursor="";}};Figure.prototype.getCanDrag=function(){return this.canDrag;};Figure.prototype.setAlpha=function(_af6){if(this.alpha===_af6){return;}this.alpha=Math.max(0,Math.min(1,_af6));if(this.alpha==1){this.html.style.filter="";this.html.style.opacity="";}else{this.html.style.filter="alpha(opacity="+Math.round(this.alpha*100)+")";this.html.style.opacity=this.alpha;}};Figure.prototype.getAlpha=function(){return this.alpha;};Figure.prototype.setDimension=function(w,h){this.width=Math.max(this.getMinWidth(),w);this.height=Math.max(this.getMinHeight(),h);if(this.html===null){return;}this.html.style.width=this.width+"px";this.html.style.height=this.height+"px";this.fireMoveEvent();if(this.workflow!==null&&this.workflow.getCurrentSelection()==this){this.workflow.showResizeHandles(this);}};Figure.prototype.setPosition=function(xPos,yPos){this.x=xPos;this.y=yPos;if(this.html===null){return;}this.html.style.left=this.x+"px";this.html.style.top=this.y+"px";this.fireMoveEvent();if(this.workflow!==null&&this.workflow.getCurrentSelection()==this){this.workflow.showResizeHandles(this);}};Figure.prototype.isResizeable=function(){return this.resizeable;};Figure.prototype.setResizeable=function(flag){this.resizeable=flag;};Figure.prototype.isSelectable=function(){return this.selectable;};Figure.prototype.setSelectable=function(flag){this.selectable=flag;};Figure.prototype.isStrechable=function(){return true;};Figure.prototype.isDeleteable=function(){return this.deleteable;};Figure.prototype.setDeleteable=function(flag){this.deleteable=flag;};Figure.prototype.setCanSnapToHelper=function(flag){this.canSnapToHelper=flag;};Figure.prototype.getCanSnapToHelper=function(){return this.canSnapToHelper;};Figure.prototype.getSnapToGridAnchor=function(){return this.snapToGridAnchor;};Figure.prototype.setSnapToGridAnchor=function(_aff){this.snapToGridAnchor=_aff;};Figure.prototype.getBounds=function(){return new Dimension(this.getX(),this.getY(),this.getWidth(),this.getHeight());};Figure.prototype.getWidth=function(){return this.width;};Figure.prototype.getHeight=function(){return this.height;};Figure.prototype.getY=function(){return this.y;};Figure.prototype.getX=function(){return this.x;};Figure.prototype.getAbsoluteY=function(){return this.y;};Figure.prototype.getAbsoluteX=function(){return this.x;};Figure.prototype.onKeyDown=function(_b00,ctrl){if(_b00==46){this.workflow.getCommandStack().execute(this.createCommand(new EditPolicy(EditPolicy.DELETE)));}if(ctrl){this.workflow.onKeyDown(_b00,ctrl);}};Figure.prototype.getPosition=function(){return new Point(this.x,this.y);};Figure.prototype.isOver=function(iX,iY){var x=this.getAbsoluteX();var y=this.getAbsoluteY();var iX2=x+this.width;var iY2=y+this.height;return (iX>=x&&iX<=iX2&&iY>=y&&iY<=iY2);};Figure.prototype.attachMoveListener=function(_b08){if(_b08===null||this.moveListener===null){return;}this.moveListener.add(_b08);};Figure.prototype.detachMoveListener=function(_b09){if(_b09===null||this.moveListener===null){return;}this.moveListener.remove(_b09);};Figure.prototype.fireMoveEvent=function(){this.setDocumentDirty();var size=this.moveListener.getSize();for(var i=0;i<size;i++){this.moveListener.get(i).onOtherFigureMoved(this);}};Figure.prototype.setModel=function(_b0c){if(this.model!==null){this.model.removePropertyChangeListener(this);}this.model=_b0c;if(this.model!==null){this.model.addPropertyChangeListener(this);}};Figure.prototype.getModel=function(){return this.model;};Figure.prototype.onOtherFigureMoved=function(_b0d){};Figure.prototype.setDocumentDirty=function(){if(this.workflow!==null){this.workflow.setDocumentDirty();}};Figure.prototype.disableTextSelection=function(_b0e){_b0e.onselectstart=function(){return false;};_b0e.unselectable="on";_b0e.style.MozUserSelect="none";_b0e.onmousedown=function(){return false;};};Figure.prototype.createCommand=function(_b0f){if(_b0f.getPolicy()==EditPolicy.MOVE){if(!this.canDrag){return null;}return new CommandMove(this);}if(_b0f.getPolicy()==EditPolicy.DELETE){if(!this.isDeleteable()){return null;}return new CommandDelete(this);}if(_b0f.getPolicy()==EditPolicy.RESIZE){if(!this.isResizeable()){return null;}return new CommandResize(this);}return null;};