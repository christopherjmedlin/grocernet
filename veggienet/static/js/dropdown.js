dropdownClickEvent = function(name) {
    $("#" + name + "-dropdown-button").click(function(event) {
        var dropdown = $("#account-dropdown")
        if (dropdown.css("display") == "block") {
            dropdown.css("display", "none")
        }
        else {
            dropdown.css("display", "block")
        }

        event.stopPropagation();
    })
}

$('html').click(function() {
    $(".dropdown").css("display", "none");
})

dropdownClickEvent("mobile-account")
dropdownClickEvent("account");
