function setCookie(cname, cvalue, cexp) {
    var d = new Date();
    d.setTime(d.getTime() + cexp*1000);
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function sortTable(table_id, column_class, data_type, dir) {
    // Simple In-Place Bubble Sort

    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = $("#" + table_id);
    switching = true;

    // Set a default sorting direction if none is specified
    if (dir != "ascending" && dir != "descending") {
        dir = "ascending";
    }

    // Make a loop that will continue until no switching has been done
    while (switching) {
        switching = false;  // Start by assuming no switches

        rows = table.children("tbody").children("tr");  // Get table rows

        // Loop through all table rows (except the first, which contains table headers)
        for (i = 0; i < (rows.length - 1); i++) {
            shouldSwitch = false;  // Start by assuming these elements shouldn't switch

            // Get the two elements you want to compare, one from current row and one from the next
            x = $(rows[i]).children("td." + column_class).text();
            y = $(rows[i + 1]).children("td." + column_class).text();
            //console.log(x);

            // Check if the two rows should switch place, based on the direction, ascending or descending
            if (dir == "ascending") {
                if (data_type == 'str') {
                    if (x.toLowerCase() > y.toLowerCase()) {
                        // if so, mark as a switch and break the loop
                        shouldSwitch = true;
                        break;
                    }
                }
                else if (data_type == 'int') {
                    if (parseInt(x) > parseInt(y)) {
                        // if so, mark as a switch and break the loop
                        shouldSwitch = true;
                        break;
                    }
                }
                // else if (data_type == 'date') {
                //     if (parseInt(x.getAttribute('unixtime')) > parseInt(y.getAttribute('unixtime'))) {
                //         // if so, mark as a switch and break the loop
                //         shouldSwitch = true;
                //         break;
                //     }
                // }
            }

            else if (dir == "descending") {
                if (data_type == 'str') {
                    if (x.toLowerCase() < y.toLowerCase()) {
                        // if so, mark as a switch and break the loop
                        shouldSwitch = true;
                        break;
                    }
                }
                else if (data_type == 'int') {
                    if (parseInt(x) < parseInt(y)) {
                        // if so, mark as a switch and break the loop
                        shouldSwitch = true;
                        break;
                    }
                }
                // else if (data_type == 'date') {
                //     if (parseInt(x.getAttribute('unixtime')) < parseInt(y.getAttribute('unixtime'))) {
                //         // if so, mark as a switch and break the loop
                //         shouldSwitch = true;
                //         break;
                //     }
                // }
            }

        }

        if (shouldSwitch) {
            // If a switch has been marked, make the switch and mark that a switch has been done
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase the count by 1
            switchcount++;
        }

        // else {
        //     // If we go through the whole list and no switching has been done AND the direction is "descending",
        //     // then we must already be sorted as "descending", so set the direction to "ascending" and run the while loop again
        //     if (switchcount == 0 && dir == "descending") {
        //         dir = "ascending";
        //         switching = true;
        //     }
        // }
        // UNUSED: This is needed if we don't specify or default to a sorting direction each time we call the function.

    }
}


function formatNumberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
