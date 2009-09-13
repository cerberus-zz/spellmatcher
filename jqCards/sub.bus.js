jQuery(function(){
    $(document).data("subs", []);
});

jQuery.sub = {
    reset:function(){
        $(document).data("subs", []);
    },
    getSubscriptions:function(){
        return $(document).data("subs");
    },
    subscribe:function(event, callback) {
        jQuery.sub.getSubscriptions().push({key: event, callback: callback})
    },
    publish:function(event, obj){
        subs = jQuery.sub.getSubscriptions();
        for (i=0; i<subs.length; i++){
            subscription = subs[i];
            if (subscription.key == event){
                subscription.callback(obj);
            }
        }
    },
};
