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

sendRatingAPIRequest = function(rating) {
    ratingReq = new XMLHttpRequest();

    ratingReq.addEventListener("error", function() {
        alert("ERROR; Your rating couldn't be saved. Try again later.");
    });

    ratingReq.open("POST", "/api/v1/vendors/rate");
    ratingReq.setRequestHeader("Content-Type", "application/json");
    vendor_id = parseInt(window.location.pathname.split('/')[2])
    postContent = JSON.stringify({"rating": rating, 
                                  "vendor_id": vendor_id})
    console.log(postContent)
    ratingReq.send(postContent);
}

starHoverEvent("#user-rating-one");
starHoverEvent("#user-rating-two");
starHoverEvent("#user-rating-three");
starHoverEvent("#user-rating-four");
starHoverEvent("#user-rating-five");

$("#user-rating-one").click(function() {sendRatingAPIRequest(1)});
$("#user-rating-two").click(function() {sendRatingAPIRequest(2)});
$("#user-rating-three").click(function() {sendRatingAPIRequest(3)});
$("#user-rating-four").click(function() {sendRatingAPIRequest(4)});
$("#user-rating-five").click(function() {sendRatingAPIRequest(5)});
