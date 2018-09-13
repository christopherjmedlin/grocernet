dropdownClickEvent = function(name) {
    $("#" + name + "-dropdown-button").click(function() {
        var dropdown = $("#" + name + "-dropdown")
        if (dropdown.css("display") == "block") {
            dropdown.css("display", "none")
        }
        else {
            dropdown.css("display", "block")
        }
    })
}

dropdownClickEvent("account");
