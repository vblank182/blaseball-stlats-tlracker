function preload(state) {

    if (state == true) {
        // Preload on
        $("#stats_cont").css("height", "400px");
        $("#stats_table").css("display", "none");
    }
    else {
        // Preload off
        $("#stats_cont").css("height", "");
        $("#stats_table").css("display", "");

        $(".sk-container").css("display", "none");
    }

}

function updateValues(element) {
    // Update value attr to match current input box property value
    $(element).attr("value", element.value);

    // Update cookie for this item
    saveCookie($(element).attr("name"), $(element).attr("value"))

    // Refresh payouts with new numbers
    updatePayouts();
}

function displayMultipliers() {
    // If a player has a coin multiplier, show it next to their name.
    $(".multiplier").each(function () {
        var mult = $(this).parent().parent().attr("player_mult");
        if( mult > 1 ) {
            $(this).html("×" + mult + "");  // Add multiplier text to card
        }
        else {
            $(this).css("display", "none");  // Hide multiplier card
        }
    });
}

function initBinds() {
    // Set up binding to detect item number selector changes
    $(".itm_card_num_box").on("input", function () {
        updateValues(this);
    });

    // Enable mousewheel scrolling in number selectors
    $(".itm_card_num_box").bind("mousewheel", function (event) {
        let dy = event.originalEvent.deltaY;
        if (dy < 0) {
            if (parseInt(this.value) < 99) {
                this.value = parseInt(this.value) + 1;
                updateValues(this);
            }
        } else {
            if (parseInt(this.value) > 0) {
                this.value = parseInt(this.value) - 1;
                updateValues(this);
            }
        }
        return false;
    });

    // Bind sort function to each header
    var columns = ["name", "hits", "hr", "sb", "payout_season"];
    for (let col of columns) {
        $("#stats_header_" + col).click(function () {

            // If we haven't sorted yet, or we sorted a different column last, use defaults and update SORT_LASTCOL
            if (SORT_LASTCOL != col) {
                SORT_LASTCOL = col;

                if (col == "name") {
                    var datatype = "str";
                    SORT_DIR = "ascending";  // default for names
                }
                else {
                    var datatype = "int";
                    SORT_DIR = "descending";  // default for numbers
                }
            }
            // If we've already sorted this column, just switch the sorting direction
            else {
                if (col == "name") {
                    var datatype = "str";

                    if (SORT_DIR == "") {
                        SORT_DIR = "ascending";  // default in case SORT_DIR isn't set
                    }
                    else {
                        // If we have a direction saved, switch it to the opposite direction
                        if (SORT_DIR == "ascending") { SORT_DIR = "descending"; }
                        else if (SORT_DIR == "descending") { SORT_DIR = "ascending"; }
                    }
                }
                else {
                    var datatype = "int";

                    if (SORT_DIR == "") {
                        SORT_DIR = "descending";  // default in case SORT_DIR isn't set
                    }
                    else {
                        // If we have a direction saved, switch it to the opposite direction
                        if (SORT_DIR == "ascending") { SORT_DIR = "descending"; }
                        else if (SORT_DIR == "descending") { SORT_DIR = "ascending"; }
                    }
                }
            }

            // Sort table
            sortTable("stats_table", "stats_" + col, datatype, SORT_DIR);

            // Change sort direction indicators
            $(".sortdir").each(function () {
                if (this.id == "sortdir_" + col) {
                    if (SORT_DIR == "ascending") { this.innerHTML = "▲"; }
                    else if (SORT_DIR == "descending") { this.innerHTML = "▼"; }
                }
                else {
                    this.innerHTML = "";
                }
            });


        });
    }
}

// Cookies //
function saveCookie(name, data) {
    cookie_name = "bst-" + name;
    cookie_data = data;
    cookie_lifetime = 60*60*24*365*5;  // set cookie to live for 5 years

    return setCookie(cookie_name, cookie_data, cookie_lifetime);
}

function loadCookie(name) {
    cookie_name = "bst-" + name;
    data = getCookie(cookie_name);

    return data;
}

function getItemCounts() {
    // Get all 'name' attributes to make a list of all items
    $(".itm_card_num_box").each(function() {
        item_count = loadCookie($(this).attr("name"));
        if (item_count != "") {
            $(this).attr("value", item_count);
        }
    });

}

function updatePayouts() {
    // // Get list of player_ids on page
    // var player_ids = [];
    // $(".stats_row[player_id]").each( function() {
    //     player_ids.push($(this).attr("player_id"))
    // });

    // Iterate through each payout cell, updating with player data using id
    $(".payout_season").each( function() {
        // For each player's stat row...

        // Get this player's id
        var plyr_id = $(this).parent().attr("player_id");

        // Get this player's multiplier
        var plyr_mult = $(".stats_row[player_id="+ plyr_id +"]").attr("player_mult");

        // Get relevant stats
        var plyr_hits = $(".stats_hits[player_id=" + plyr_id + "]")[0].innerHTML;
        var plyr_hr = $(".stats_hr[player_id=" + plyr_id + "]")[0].innerHTML;
        var plyr_sb = $(".stats_sb[player_id=" + plyr_id + "]")[0].innerHTML;

        // Get current concession item values
        var num_sunflowerseeds = $("#itm_val_sunflowerseeds").attr("value");
        var num_hotdog = $("#itm_val_hotdog").attr("value");
        var num_pickles = $("#itm_val_pickles").attr("value");
        var num_chips = $("#itm_val_chips").attr("value");
        var num_burger = $("#itm_val_burger").attr("value");
        var num_meatball = $("#itm_val_meatball").attr("value");

        // Update this player's payout column
        var payout = plyr_mult * (plyr_hits*num_sunflowerseeds + plyr_hr*num_hotdog + plyr_sb*num_pickles);
        this.innerHTML = payout;
        //this.innerHTML = formatNumberWithCommas(payout);  // TODO: Need to fix comma sorting problem to use this

    });

}
