starHoverEvent = function(selector) {
    $(selector).hover(function() {
        prevAll = $(selector).prevAll().addBack();
        prevAll.removeClass("unchecked");
        prevAll.addClass("hovered");
        
    }, function() {
        prevAll = $(selector).prevAll().addBack();
        prevAll.removeClass("hovered");
        prevAll.addClass("unchecked");
    });

    $(selector).click(function() {
        prevAll = $(selector).prevAll().addBack();
        prevAll.addClass("checked");
        $(selector).nextAll().removeClass("checked");
    });
};

starHoverEvent("#user-rating-one")
starHoverEvent("#user-rating-two")
starHoverEvent("#user-rating-three")
starHoverEvent("#user-rating-four")
starHoverEvent("#user-rating-five")
