// https://github.com/lstebner/jQuery-Ghost-Text
(function( $ ){
    /**
    * Ghost Text is used to present default text inside of an input and then clear it when the user
    * gives focus. When the user exits (blurs) the input, if they have not entered their own value
    * the ghost text is then put back in the input.
    *
    *
    * Options {
    *       ghostText: The text you want to use as the ghost text for this input
    *           default - current value when .ghostText() is called
    *
    *       ghostClass: The class to add to the input while the ghost text is present
    *           default - 'ghost-text'
    *
    *       focus: A custom callback for when the input gains focus
    *           default - null
    *
    *       blur: A custom callback for when the input is blurred
    *           default - null
    *
    *       change: A custom callback for when the input value changes
    *           default - null
    *
    *       clearOnSubmit: A boolean saying whether or not to clear the input when the parent
    *               form is submitted if it still has the default ghost text in it.
    *           default - true
    *
    *       parentForm: The ID of the parent form to attach the submit event too
    *           default - A search to find the form using $self.closest('form')
    *   }
    *
    * Methods:
    *   - init: An initialization function to set default settings and attach events
    *   - updateSettings: Update the stored settings for the object
    *   - parentFormSubmit: Called when parent form is submitted (if clearOnSubmit is true)
    *   - focus: Called on focus
    *   - blur: Called on blur
    *   - change: Call on change
    *
    *
    **/
    $.fn.ghostText = function(opts, args){
		if (this.length == 0){
			return false;
		}
		else if (this.length > 1){
			return this.each(function(){
				$(this).ghostText( opts, args );
			});
		}
	
        var $self = this;
        var val = this.val();
        
        //defaults for everything
        var defaults = {
            ghostText: val,
            ghostClass: 'ghost-text',
            focus: null,
            blur: null,
            change: null,
            clearOnSubmit: true,
            parentForm: null
        };
        
        //grab settings data
        var settings = $self.data('ghostText');
        
        //methods
        var methods = {
            //initialize
            init: function(){
                if (!opts){ opts = {}; }
                
                //set the settings using the defaults and any passed in options
                settings = defaults;
                methods.updateSettings(opts);
                
                //in case a different text was passed in that is currently in the input,
                //set the value from the settings
                $self.val( settings.ghostText );
                
                //check for needing to set a parent form submit event
                if (settings.clearOnSubmit){
                    //see if the ID of the form was passed in
                    if (settings.parentForm){
                        //use it to apply submit function
                        $( '#' + settings.parentForm.replace('#', '') ).submit(function(e){
                            methods.parentFormSubmit(e);
                        });
                    }
                    //otherwise we do a search for the closest form and assume it
                    else{
                        $self.closest('form').submit(function(){
                            methods.parentFormSubmit();
                        });
                    }
                }
                
                //add other input events
                $self.focus( function(){ methods.focus(); } );
                $self.blur( function(){ methods.blur(); } );
                $self.keyup( function(){ methods.change(); } );
                
                //check for ghostText class and add if needed
                if (!$self.hasClass( settings.ghostClass )){
                    $self.addClass( settings.ghostClass );
                }
            },
            //update the settings and stored data
            updateSettings: function(opts){
                settings = $.extend(settings, opts);
                $self.data('ghostText', settings);
            },
            //parent form submit to clear input if it's still the default on submit
            parentFormSubmit: function(){
                if ($self.val() == settings.ghostText){
                    $self.val('');
                }
            },
            //on focus clear the field if it has the ghost text in it
            focus: function(){
                val = $self.val(); 
                
                if (val == settings.ghostText){
                    $self.val('').removeClass( settings.ghostClass );
                }
                
                //check for custom supplied callback
                if (settings.focus){
                    settings.focus(val);
                }
            },
            //on blur re-insert the ghost text if the field is left empty or the ghost
            //text is still present (which actually should never happen)
            blur: function(){
                val = $self.val();
                
                if (val.replace(/\s/g, '') == '' || val == settings.ghostText){
                    $self.val( settings.ghostText ).addClass( settings.ghostClass );
                }
                
                //check for custom blur callback
                if (settings.blur){
                    settings.blur(val);
                }
            },
            //on change there is no default behavior, but a custom callback can be provided
            change: function(){
                val = $self.val();
                
                //check for custom callback
                if (settings.change){
                    settings.change(val);
                }
            }
        };
        
        //check for method call
        if (typeof(opts) == 'string'){
            //check that method is valid
            if (methods.hasOwnProperty( opts )){
                //pass any args
                return methods[opts](args);
            }
        }
        else{
            //initialize
            methods.init();
        }
        
        return $self;
    }
})( jQuery );