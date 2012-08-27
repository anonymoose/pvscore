/* This notice must be untouched at all times.

Open-jACOB Draw2D
The latest version is available at
http://www.openjacob.org

Copyright (c) 2006 Andreas Herz. All rights reserved.
Created 5. 11. 2006 by Andreas Herz (Web: http://www.freegroup.de )

LICENSE: LGPL

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License (LGPL) as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA,
or see http://www.gnu.org/copyleft/lesser.html
*/

/**
 * 
 * @version 0.9.23
 * @author Andreas Herz
 * @constructor
 */
Figure=function()
{
  this.construct();
};

/** 
 * All objects have a member called "type", which uniquely identifies 
 * a property type. This is a provision for a possible serialization.
 *
 **/
Figure.prototype.type="Figure";

/** @private **/
Figure.ZOrderBaseIndex = 100;

/**
 * Set the common z-index of the window element. This method exists for
 * compatibility reason to dojo or another UI javascript library. 
 * It is now possible to arange the draw2d elements behind/before other UI elements-
 *
 * @see #setZOrder
 * @static
 * @param {int} index The z-order for all new figure objects.
 **/
Figure.setZOrderBaseIndex=function(/*:int*/ index)
{
  Figure.ZOrderBaseIndex = index;
};

/**
 * @private
 **/
Figure.prototype.construct=function()
{
  this.lastDragStartTime =0;
  /** @private **/
  this.x = 0;
  /** @private **/
  this.y = 0;
  /** @private **/
  this.width = 10;
  /** @private **/
  this.height= 10;
  /** @private **/
  this.border=null;  /*:Border*/
  /** @private **/
  this.id   = UUID.create();  /*:String*/
  /** @private **/
  this.html = this.createHTMLElement(); /*:HTMLElement*/
  /** @private **/
  this.canvas = null;    /*:Canvas*/ 
  /** @private **/
  this.workflow = null;  /*:Workflow*/
  /** @private **/
  this.draggable = null; /*:HTMLElement*/
  /** @private **/
  this.parent    = null; /*:CompartmentFigure*/
  /** @private **/
  this.isMoving  = false; /*:boolean*/
  /** @private **/
  this.canSnapToHelper = true; /*:boolean*/
  /** @private **/
  this.snapToGridAnchor = new Point(0,0);
  /** @private **/
  this.timer = -1; // Fadein/Fadeout timer id.
  /** @private **/
  this.model = null; /*:AbstractObjectModel*/
  /** @private **/
  this.alpha = 1.0;
  /** @private **/
  this.alphaBeforeOnDrag = 1.0;

  // a figure can store additional, user defined properties
  //
  /** @private **/
  this.properties = {} /*:Map<name,value>*/

  // Hier werden Object registriert welche informiert werden wollen wenn sich dieses
  // Object bewegt hat.
  //
  /** @private **/
  this.moveListener = new ArrayList();

  // It is important to set the flags below. Otherwise the flags will be <null>
  //
  this.setDimension(this.width,this.height);
  this.setDeleteable(true);
  this.setCanDrag(true);
  this.setResizeable(true);
  this.setSelectable(true);

};

/**
 * Override this method to free your resource too.
 *
 * @private
 **/
Figure.prototype.dispose=function()
{
  //this.id   = null; don't dispose the id! This is important for deregistration
  //this.html = null; don't dispose the html! This is important for deregistration
  this.canvas = null;
  this.workflow = null;
  this.moveListener = null;
  if(this.draggable!==null)
  {
    this.draggable.removeEventListener("mouseenter", this.tmpMouseEnter);
    this.draggable.removeEventListener("mouseleave", this.tmpMouseLeave);
    this.draggable.removeEventListener("dragend", this.tmpDragend);
    this.draggable.removeEventListener("dragstart",this.tmpDragstart );
    this.draggable.removeEventListener("drag",this.tmpDrag);
    this.draggable.removeEventListener("dblclick",this.tmpDoubleClick );
    this.draggable.node = null;
    this.draggable.target.removeAllElements();
  }
  this.draggable = null;
  if(this.border!==null)
    this.border.dispose();
  this.border = null;

  // remove this figure from the parent CompartmentFigure
  //
  if(this.parent!==null)
    this.parent.removeChild(this);
};


/**
 * A figure can store user defined attributes. This method returns all properties stored in this figure.<br>
 *
 * @see #setProperty
 * @returns All user defined properties of the figure
 * @type Map
 **/
Figure.prototype.getProperties=function()
{
  return this.properties;
};


/**
 * A figure can store user defined attributes. This method returns the requested property.<br>
 *
 * @see #setProperty
 * @returns The user defined property of this figure.
 * @type String
 **/
Figure.prototype.getProperty=function(/*:String*/ key)
{
  return this.properties[key];
};


/**
 * A figure can store any type of information. You can use this to attach any String or Object to this
 * figure.
 *
 * @see #getProperty
 * @param {String} key The key of the property.
 * @param {String} value The value of the property.
 **/
Figure.prototype.setProperty=function(/*:String*/ key,/*:String*/ value)
{
  this.properties[key]=value;
  this.setDocumentDirty();
};


/**
 * Return the document unique id of this element. It is not an uuid or guid
 * @type String
 **/
Figure.prototype.getId=function()
{
  return this.id;
};

/**
 * Set the unique id of this element.
 *
 * @param {String} id The new unique id of this element
 * @since 0.9.15
 **/
Figure.prototype.setId=function(/*:String*/ id)
{
  this.id=id;
  if(this.html!==null)
     this.html.id = id;
};


/**
 * @private
 * @param {Canvas} canvas
 **/
Figure.prototype.setCanvas= function(/*:Canvas*/ canvas)
{
  this.canvas = canvas;
};

/**
 * Returns the associated worklow canvas.
 *
 * @type Workflow
 **/
Figure.prototype.getWorkflow=function()
{
   return this.workflow;
};

/**
 * @private
 * @param {Workflow} workflow
 **/
Figure.prototype.setWorkflow= function(/*:Workflow*/ workflow)
{
  // The parent is a Workflow class - now we create the Drag-Objekt
  //
  if(this.draggable===null)
  {
    // Firefox seems to need to have the tabindex="0" property set to some value 
    // so it knows this Div or Span is keyboard selectable. That allows the keyboard 
    // event to be triggered. It is not so dumb - you might want to trap Delete or 
    // Insert keys on a figure etc. 
    this.html.tabIndex="0";

    var oThis = this;

    this.keyDown=function(event)
    {
      event.cancelBubble = true; // Stop event propagation
      event.returnValue = true;  // Execute the standard event for this event. Important for Input Fields/Dialogs
      oThis.onKeyDown(event.keyCode, event.ctrlKey);
    }
    if (this.html.addEventListener) 
      this.html.addEventListener("keydown", this.keyDown, false);
    else if (this.html.attachEvent) 
      this.html.attachEvent("onkeydown", this.keyDown);

    this.draggable = new Draggable(this.html, Draggable.DRAG_X | Draggable.DRAG_Y);
    this.draggable.node = this;
    this.tmpContextMenu = function (oEvent)
    {
       oThis.onContextMenu(oThis.x+oEvent.x, oEvent.y+oThis.y);
    };

    this.tmpMouseEnter  = function (oEvent)
    {
       oThis.onMouseEnter();
    };

    this.tmpMouseLeave  = function (oEvent){oThis.onMouseLeave();};
    this.tmpDragend     = function (oEvent){oThis.onDragend();};
    this.tmpDragstart   = function (oEvent){
       var w = oThis.workflow;
       w.showMenu(null);

       // reset old action of the toolbar
       if(w.toolPalette && w.toolPalette.activeTool)
       {
          oEvent.returnValue = false;
          w.onMouseDown(oThis.x+oEvent.x, oEvent.y+oThis.y);
          w.onMouseUp(oThis.x+oEvent.x, oEvent.y+oThis.y);
          return;
       }
       // check if a line has been hit. Unfortunately a line cant receive the mouseDown,mouseUp
       // event correct. This depends on the wz_vector library implementation
       // 
       if(!(oThis instanceof ResizeHandle) && !(oThis instanceof Port))
       {
          var line = w.getBestLine(oThis.x+oEvent.x, oEvent.y+oThis.y);
          if(line!==null)
          {
             oEvent.returnValue = false;
             w.setCurrentSelection(line);
             w.showLineResizeHandles(line);
             w.onMouseDown(oThis.x+oEvent.x, oEvent.y+oThis.y);
             return;
          }
          else if(oThis.isSelectable())
          {
            w.showResizeHandles(oThis);
            w.setCurrentSelection(oThis);
          }
       }
       oEvent.returnValue = oThis.onDragstart(oEvent.x,oEvent.y);
    };

    this.tmpDrag        = function (oEvent){oThis.onDrag();};
    this.tmpDoubleClick = function (oEvent){oThis.onDoubleClick();};

    this.draggable.addEventListener("contextmenu", this.tmpContextMenu);
    this.draggable.addEventListener("mouseenter", this.tmpMouseEnter);
    this.draggable.addEventListener("mouseleave", this.tmpMouseLeave);
    this.draggable.addEventListener("dragend", this.tmpDragend);
    this.draggable.addEventListener("dragstart",this.tmpDragstart );
    this.draggable.addEventListener("drag",this.tmpDrag);
    this.draggable.addEventListener("dblclick",this.tmpDoubleClick );
  }
  this.workflow = workflow;
};

/**
 * @private
 **/
Figure.prototype.createHTMLElement=function()
{
    var item = document.createElement('div');
    item.id        = this.id;
    item.style.position="absolute";
    item.style.left   = this.x+"px";
    item.style.top    = this.y+"px";
    item.style.height = this.width+"px";
    item.style.width  = this.height+"px";
    item.style.margin = "0px";
    item.style.padding= "0px";
    item.style.outline= "none";
    item.style.zIndex = ""+Figure.ZOrderBaseIndex;

    return item;
};


/**
 * Set the parent of this figure.
 * Don't call them manually. Is CompartmentFigre.appendChild() instead.

 * @param {CompartmentFigure} parent The new parent of this figure
 * @private
 **/
Figure.prototype.setParent=function(/*:CompartmentFigure*/ parent)
{
  this.parent = parent;
};

/**
 * Get the parent of this figure.
 *
 * @type CompartmentFigure
 **/
Figure.prototype.getParent=function()
{
  return this.parent;
};


/**
 * @return Returns the z-index of the element.
 * @type int
 **/
Figure.prototype.getZOrder=function()
{
    return this.html.style.zIndex;
};

/**
 * @param {int} index Set the new z-index of the element
 **/
Figure.prototype.setZOrder=function(/*:int*/ index)
{
    this.html.style.zIndex=index;
};


/**
 * Return true if the origin of the Object is the window and not
 * the document. This is usefull if you want implement a window or a
 * dialog element. The element doesn't move if the user scroll the document.
 *
 * @returns Returns [true] if the origin of the object the window.
 * @type boolean
 **/
Figure.prototype.hasFixedPosition=function()
{
  return false;
};

/**
 * This value is relevant for the interactive resize of the figure.
 *
 * @returns Returns the min width of this object.
 * @type int
 **/
Figure.prototype.getMinWidth=function()
{
  return 5;
};

/**
 * This value is relevant for the interactive resize of the figure.
 *
 * @returns Returns the min height of this object.
 * @type int
 **/
Figure.prototype.getMinHeight=function()
{
  return 5;
};

/**
 * @private
 **/
Figure.prototype.getHTMLElement=function()
{
  if(this.html===null)
    this.html = this.createHTMLElement();
  return this.html;
};

/**
 * @see Circle for an example implementation.
 * @private
 **/
Figure.prototype.paint=function()
{
  // called after the element has been added to the document
};

/**
 * @param {Border} border Set the border for this figure
 **/
Figure.prototype.setBorder=function(/*:Border*/ border)
{
  if(this.border!==null)
    this.border.figure=null;

  this.border=border;
  this.border.figure=this;
  this.border.refresh();
  this.setDocumentDirty();
};

/**
 * Callback method if the figure has been remove from the Workflow object.<br>
 * Usefull to trigger additional actions.
 *
 * @protected
 * @param {Workflow} workflow
 * @since 0.9.19
 **/
Figure.prototype.onRemove= function(/*:Workflow*/ workflow)
{
};


/**
 * Callback method for the context menu interaction.
 * Don't override this method! Implement getContextMenu instead.
 *
 * @see #getContextMenu
 * @private
 * @final
 * @param {int} x The absolute x coordinate of the right mouse button click
 * @param {int} y The absolute y coordinate of the right mouse button click
 **/
Figure.prototype.onContextMenu=function(/*:int*/ x, /*:int*/y)
{
    var menu = this.getContextMenu();
    if(menu!==null)
      this.workflow.showMenu(menu,x,y);
};

/**
 * @returns null or the Menu object for this figure.
 * @type Menu
 **/
Figure.prototype.getContextMenu=function()
{
   return null;
};

/**
 * Callback method for the double click event of user interaction.
 * Sub classes can override this method to implement their own behaviour.
 **/
Figure.prototype.onDoubleClick=function()
{
};

/**
 * Callback method for the mouse enter event. Usefull for mouse hover-effects.
 * Sub classes can override this method to implement their own behaviour.
 **/
Figure.prototype.onMouseEnter=function()
{
};


/**
 * Callback method for the mouse leave event. Usefull for mouse hover-effects.
 * 
 **/
Figure.prototype.onMouseLeave=function()
{
};

/**
 * Don't call them manually. This will be done by the framework.<br>
 * Will be called if the object are moved via drag and drop.
 * Sub classes can override this method to implement additional stuff. Don't forget to call
 * the super implementation via <code>Figure.prototype.onDrag.call(this);</code>
 * @private
 **/
Figure.prototype.onDrag = function()
{
  this.x = this.draggable.getLeft();
  this.y = this.draggable.getTop();

  // enable the  blending o the first real move of the object
  //
  if(this.isMoving==false)
  {
   this.isMoving = true;
   this.alphaBeforeOnDrag = this.getAlpha();
   this.setAlpha(this.alphaBeforeOnDrag*0.5);
  }
  this.fireMoveEvent();
};

/**
 * Will be called after a drag and drop action.<br>
 * Sub classes can override this method to implement additional stuff. Don't forget to call
 * the super implementation via <code>Figure.prototype.onDragend.call(this);</code>
 * @private
 **/
Figure.prototype.onDragend = function()
{
   if(this.getWorkflow().getEnableSmoothFigureHandling()===true)
   {
      var oThis = this;
      var slowShow = function()
      {
         if(oThis.alpha<oThis.alphaBeforeOnDrag)
         {
            oThis.setAlpha(Math.min(1.0,oThis.alpha+0.05));
         }
         else
         {
            window.clearInterval(oThis.timer);
            oThis.timer = -1;
         }
      };
      if(oThis.timer>0)
         window.clearInterval(oThis.timer);
      oThis.timer = window.setInterval(slowShow,20);
  }
  else
  {
      this.setAlpha(this.alphaBeforeOnDrag);
  }
  // Element ist zwar schon an seine Position, das Command muss aber trotzdem
  // in dem CommandStack gelegt werden damit das Undo funktioniert.
  //
  this.command.setPosition(this.x, this.y);
  this.workflow.commandStack.execute(this.command);
  this.command = null;
  this.isMoving = false;
  this.workflow.hideSnapToHelperLines();
  this.fireMoveEvent();
};


/**
 * Will be called if the drag and drop action beginns. You can return [false] if you
 * want avoid that the figure can be move.
 * 
 * @param {int} x the x-coordinate of the click event
 * @param {int} y the y-coordinate of the click event
 * @type boolean
 **/
Figure.prototype.onDragstart = function(/*:int*/ x, /*:int*/ y)
{
  this.command = this.createCommand(new EditPolicy(EditPolicy.MOVE));
  return this.command!==null;
};

/**
 * Switch on/off the drag drop behaviour of this object
 *
 * @param {boolean} flag The new drag drop indicator
 **/
Figure.prototype.setCanDrag=function(/*:boolean*/flag)
{
  this.canDrag= flag;
  if(flag)
    this.html.style.cursor="move";
  else
    this.html.style.cursor="";
};

/**
 * Return [true] of the object can be moved via drag drop.
 *
 * @type boolean
 * @since 0.9.18
 **/
Figure.prototype.getCanDrag=function()
{
  return this.canDrag;
};

/**
 * Set the alpha blending of this figure. 
 *
 * @see #getAlpha
 * @param {float} percent Value between 0-1.
 **/
Figure.prototype.setAlpha=function(/*:float 0-1*/ percent)
{
  if(this.alpha===percent)
     return;

  this.alpha = Math.max(0.0,Math.min(1.0,percent));
  if(this.alpha==1.0)
  {
    this.html.style.filter = "";
    this.html.style.opacity = "";
  }
  else
  {
    this.html.style.filter = "alpha(opacity="+Math.round(this.alpha*100)+")";
    this.html.style.opacity = this.alpha;
  }
};

/**
 * Get the alpha blending of this figure. Values are always between [0,1]
 *
 * @see #setAlpha
 * @type {float}
 **/
Figure.prototype.getAlpha=function()
{
  return this.alpha;
};

/**
 * Set the new width and height of the figure. 
 *
 * @see #getMinWidth
 * @see #getMinHeight
 * @param {int} w The new width of the figure
 * @param {int} h The new height of the figure
 **/
Figure.prototype.setDimension=function(/*:int*/ w, /*:int*/ h)
{
  this.width = Math.max(this.getMinWidth(),w);
  this.height= Math.max(this.getMinHeight(),h);

  // Nothing to do if the figure not part of the current DOM tree
  //
  if(this.html===null)
    return;

  this.html.style.width  = this.width+"px";
  this.html.style.height = this.height+"px";

  this.fireMoveEvent();

  // Update the resize handles if the user change the dimension via an API call
  //
  if(this.workflow!==null && this.workflow.getCurrentSelection()==this)
  {
     this.workflow.showResizeHandles(this);
  }
};

/**
 * Set the position of the object.
 *
 * @param {int} xPos The new x coordinate of the figure
 * @param {int} yPos The new y coordinate of the figure 
 **/
Figure.prototype.setPosition=function(/*:int*/ xPos , /*:int*/ yPos )
{
//  this.x = Math.max(0,xPos);
//  this.y = Math.max(0,yPos);
  this.x= xPos;
  this.y= yPos;
  // Falls das Element noch nie gezeichnet wurde, dann braucht aus das HTML nicht 
  // aktualisiert werden
  //
  if(this.html===null)
    return;

  this.html.style.left = this.x+"px";
  this.html.style.top  = this.y+"px";

  this.fireMoveEvent();

  // Update the resize handles if the user change the position of the element via an API call.
  //
  if(this.workflow!==null && this.workflow.getCurrentSelection()==this)
     this.workflow.showResizeHandles(this);
};

/**
 * Returns the true if the figure can be resized.
 *
 * @see #setResizeable
 * @type boolean
 **/
Figure.prototype.isResizeable=function()
{
  return this.resizeable;
};

/**
 * You can change the resizeable behaviour of this object. Hands over [false] and
 * the figure has no resizehandles if you select them with the mouse.<br>
 *
 * @see #getResizeable
 * @param {boolean} flag The resizeable flag.
 **/
Figure.prototype.setResizeable=function(/*:boolean*/ flag)
{
  this.resizeable=flag;
};

/**
 * 
 * @type boolean
 **/
Figure.prototype.isSelectable=function()
{
  return this.selectable;
};


/**
 * You can change the selectable behaviour of this object. Hands over [false] and
 * the figure has no selection handles if you try to select them with the mouse.<br>
 *
 * @param {boolean} flag The selectable flag.
 **/
Figure.prototype.setSelectable=function(/*:boolean*/ flag)
{
  this.selectable=flag;
};

/**
 * Return true if the object doesn't care about the aspect ratio.
 * You can change the hight and width indipendent.
 * @type boolean
 */
Figure.prototype.isStrechable=function()
{
  return true;
};

/**
 * Return false if you avoid that the user can delete your figure.
 * Sub class can override this method.
 * @type boolean
 **/
Figure.prototype.isDeleteable=function()
{
  return this.deleteable;
};

/**
 * Return false if you avoid that the user can delete your figure.
 * 
 * @param {boolean} flag Enable or disable flag for the delete operation
 **/
Figure.prototype.setDeleteable=function(/*:boolean */flag)
{
  this.deleteable = flag;
};


/**
 * Set the flag if this object can snap to grid or geometry.
 * A window of dialog should set this flag to false.
 * @param {boolean} flag The snap to grid/geometry enable flag.
 *
 **/
Figure.prototype.setCanSnapToHelper=function(/*:boolean */flag)
{
  this.canSnapToHelper = flag;
};

/**
 * Returns true if the figure cna snap to any helper like a grid, guide, geometrie
 * or something else.
 *
 * @type boolean
 **/
Figure.prototype.getCanSnapToHelper=function()
{
  return this.canSnapToHelper;
};

/**
 *
 * @type Point
 **/
Figure.prototype.getSnapToGridAnchor=function()
{
  return this.snapToGridAnchor;
};

/**
 *
 * @type Point
 **/
Figure.prototype.setSnapToGridAnchor=function(/*:Point*/ point)
{
  this.snapToGridAnchor = point;
};

/**
 * @type Dimension
 **/
Figure.prototype.getBounds=function()
{
  return new Dimension(this.getX(),this.getY(),this.getWidth(),this.getHeight());
};


/**
 * @type int
 **/
Figure.prototype.getWidth=function()
{
  return this.width;
};

/**
 * @type int
 **/
Figure.prototype.getHeight=function()
{
  return this.height;
};

/**
 * @returns The y-offset to the parent figure.
 * @type int
 **/
Figure.prototype.getY=function()
{
    return this.y;
};

/**
 * @returns the x-offset to the parent figure
 * @type int
 **/
Figure.prototype.getX=function()
{
    return this.x;
};

/**
 * @returns The Y coordinate in relation the Canvas.
 * @type int
 **/
Figure.prototype.getAbsoluteY=function()
{
  return this.y;
};

/**
 * @returns The X coordinate in relation to the canvas
 * @type int
 **/
Figure.prototype.getAbsoluteX=function()
{
  return this.x;
};

/**
 * This method will be called from the framework if the objects is selected and the user press any key.
 * Sub class can override this method to implement their own stuff.
 * 
 * @param {int} keyCode The code of the pressed key
 **/
Figure.prototype.onKeyDown=function(/*:int*/ keyCode, /*:boolean*/ ctrl)
{
  if(keyCode==46)
     this.workflow.getCommandStack().execute(this.createCommand(new EditPolicy(EditPolicy.DELETE)));

  // redirect any CTRL key strokes to the parent workflow/canvas
  //
  if(ctrl)
     this.workflow.onKeyDown(keyCode,ctrl);
};

/**
 * Returns the position of the figure.
 *
 * @type Point
 * @deprecated
 **/
Figure.prototype.getPosition=function()
{
  return new Point(this.x, this.y);
};


Figure.prototype.isOver = function (/*:int*/ iX ,/*:int*/ iY)
{
    var x = this.getAbsoluteX();
    var y = this.getAbsoluteY();
    var iX2 = x + this.width;
    var iY2 = y + this.height;
    return (iX >= x && iX <= iX2 && iY >= y && iY <= iY2);
};

/**
 * @param {Figure} figure The figure to monitor
 *
 **/
Figure.prototype.attachMoveListener = function(/*:Figure*/ figure)
{
  if(figure===null || this.moveListener===null)
    return;

  this.moveListener.add(figure);
};


/**
 * @param {Figure} figure The figure to remove the monitor
 *
 **/
Figure.prototype.detachMoveListener = function(/*:Figure*/ figure) 
{
  if(figure===null || this.moveListener===null)
    return;

  this.moveListener.remove(figure);
};

/**
 * @private
 **/
Figure.prototype.fireMoveEvent=function()
{
  this.setDocumentDirty();
  var size= this.moveListener.getSize();
  for(var i=0;i<size;i++)
  {
    this.moveListener.get(i).onOtherFigureMoved(this);
  }
};

/**
 * Set the primary model object that this Figure represents. This method is used 
 * by an EditPartFactory when creating an Figure.
 * 
 * @param {AbstractObjectModel} model The model
 * @since 0.9.15
 * @final
 */
Figure.prototype.setModel=function(/*:AbstractObjectModel*/ model)
{
   if(this.model!==null)
      this.model.removePropertyChangeListener(this);

   this.model = model;

   if(this.model!==null)
      this.model.addPropertyChangeListener(this);
};


/**
 * Returns the primary model object that this Figure represents.
 * 
 * @type AbstractObjectModel
 * @since 0.9.15
 * @final
 */
Figure.prototype.getModel=function()
{
   return this.model;
};


/**
 * Falls man sich zuvor an einem Object mit attacheMoveListener(..) registriert hat,
 * wird man hierüber dann informiert wenn sich das Objekt bewegt hat.
 *
 * @param {Figure} figure The figure which has changed its position
 * @private
 */
Figure.prototype.onOtherFigureMoved=function(/*:Figure*/ figure)
{
};

/**
 * This method will be called if the figure has changed any postion, color, dimension or something else.
 *
 * @private
 **/
Figure.prototype.setDocumentDirty=function()
{
  if(this.workflow!==null)
    this.workflow.setDocumentDirty();
};


/**
 * Utility function to disable text selection on the handsover element
 *
 * @private
 **/
Figure.prototype.disableTextSelection=function(/*:HTMLElement*/ element)
{
  element.onselectstart = function() {return false;};
  element.unselectable = "on";
  element.style.MozUserSelect = "none";
  element.onmousedown=function(){return false;};
};


/**
 * Returns the Command to perform the specified Request or null.
  *
 * @param {EditPolicy} request describes the Command being requested
 * @return null or a Command
 * @type Command 
 * @since 0.9.15
 **/
Figure.prototype.createCommand=function(/*:EditPolicy*/ request)
{
  if(request.getPolicy() == EditPolicy.MOVE)
  {
    if(!this.canDrag)
      return null;
    return new CommandMove(this);
  }

  if(request.getPolicy() == EditPolicy.DELETE)
  {
    if(!this.isDeleteable())
       return null;
    return new CommandDelete(this)
  }
  if(request.getPolicy() == EditPolicy.RESIZE)
  {
    if(!this.isResizeable())
       return null;
    return new CommandResize(this)
  }
  return null;
};



