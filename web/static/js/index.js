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

    let scale_sunflowerseeds = [5,11,19,28,37,47,57,68,79,90,102,113,125,137,150,162,175,188,201,214,227,240,254,268,281,295,309,323,337,352,366,381,395,410,425,440,455,470,485,500,515,530,546,561,577,593,608,624,640,656,672,688,704,720,736,752,769,785,802,818,835,851,868,885,902,918,935,952,969,986,1003,1020,1038,1055,1072,1090,1107,1124,1142,1159,1177,1194,1212,1230,1248,1265,1283,1301,1319,1337,1355,1373,1391,1409,1427,1445,1463,1482,1500]
    let scale_hotdog = [20,60,100,140,180,225,265,305,345,385,425,465,505,550,590,630,670,710,750,790,830,875,915,955,995,1035,1075,1115,1155,1200,1240,1280,1320,1360,1400,1440,1480,1525,1565,1605,1645,1685,1725,1765,1805,1850,1890,1930,1970,2010,2050,2090,2130,2170,2215,2255,2295,2335,2375,2415,2455,2495,2540,2580,2620,2660,2700,2740,2780,2820,2865,2905,2945,2985,3025,3065,3105,3145,3190,3230,3270,3310,3350,3390,3430,3470,3515,3555,3595,3635,3675,3715,3755,3795,3840,3880,3920,3960,4000]
    let scale_pickles = [50,80,110,140,170,200,230,260,290,320,350,380,410,440,470,500,530,560,590,620,650,680,710,740,770,805,835,865,895,925,955,985,1015,1045,1075,1105,1135,1165,1195,1225,1255,1285,1315,1345,1375,1405,1435,1465,1495,1525,1555,1585,1615,1645,1675,1705,1735,1765,1795,1825,1855,1885,1915,1945,1975,2005,2035,2065,2095,2125,2155,2185,2215,2245,2280,2310,2340,2370,2400,2430,2460,2490,2520,2550,2580,2610,2640,2670,2700,2730,2760,2790,2820,2850,2880,2910,2940,2970,3000]
    let scale_chips = [0]
    let scale_burger = [0]
    let scale_meatball = [0]

    // // Get list of player_ids on page
    // var player_ids = [];
    // $(".stats_row[player_id]").each( function() {
    //     player_ids.push($(this).attr("player_id"))
    // });

    // Iterate through each payout cell, updating with player data using id
    $(".payout_season").each( function() {
        // For each player's stat row:

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

        // Get final concession item returns using scaling weights
        var val_sunflowerseeds = num_sunflowerseeds * scale_sunflowerseeds[num_sunflowerseeds-1]
        var val_hotdog = num_hotdog * scale_hotdog[num_hotdog-1]
        var val_pickles = num_pickles * scale_pickles[num_pickles-1]
        var val_chips = num_chips * scale_chips[num_chips-1]
        var val_burger = num_burger * scale_burger[num_burger-1]
        var val_meatball = num_meatball * scale_meatball[num_meatball-1]

        // Update this player's payout column
        var payout = plyr_mult * (plyr_hits*val_sunflowerseeds + plyr_hr*val_hotdog + plyr_sb*val_pickles);
        this.innerHTML = payout;
        //this.innerHTML = formatNumberWithCommas(payout);  // TODO: Need to fix comma sorting problem to use this

    });

}
