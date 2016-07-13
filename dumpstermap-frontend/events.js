/**
 * Created by m on 30.12.15.
 */

// Register events
/*map.on('move', function () {
 updateListing();
 });*/

map_container.map.on('click',
    function (e) {
        $('#sidebar').hide();
    }
);

$(document).on('click', '#btn-show-dumpster-feedback', function (event) {
    $('#dumpster-feedback').show();
    $('#btn-show-dumpster-feedback').hide();
});
$(document).on('click', '#btn-cancel-dumpster-feedback', function (event) {
    $('#dumpster-feedback').hide();
    $('#btn-show-dumpster-feedback').show();
});
$(document).on('click', '#btn-comment', function (event) {
    event.preventDefault();
    var name = $("#submit-name").val();
    var opinion = $("#submit-opinion").val();
    var comment = $("#submit-comment").val();
    var dumpster_id = getDumpsterId();

    //update view
    var update_comments = function () {
        var html = templates.marker_popup_comments({
            'name': name,
            'comment': comment,
            'date': 'Just now'
        });
        $(html).hide().appendTo("#comment_list").fadeIn(500);
    };
    send_comment(dumpster_id, opinion, comment, name, update_comments);

});

var new_place_marker;
var adding_new = false;
$(document).on('click', '#btn-add-dumpster', function (event) {
    event.preventDefault();
    adding_new = true;

    // Show sidebar & create form
    var html = templates.add_dumpster_template();
    $('#sidebar-content').html(html);
    $('#sidebar').show();

    // Remove old marker
    if (new_place_marker != null)
        map_container.map.removeLayer(new_place_marker);

    // Create marker to show on map
    var latlng = map_container.map.getCenter();

    new_place_marker = createMarker(
        latlng.lat,
        latlng.lng,
        {
            "title": "Now place the marker!",
            "description": "",
            "marker-color": "#F42786",
            "marker-size": "small",
            "marker-symbol": "waste-basket",
        }
    );
    new_place_marker.options.draggable = true;
    new_place_marker.addTo(map_container.map);

    new_place_marker.openPopup();


});
$(document).on('click', '#btn-cancel', function (event) {
    $("#sidebar").hide();
    map_container.map.removeLayer(new_place_marker);
});
function createMarker(lat, lng, properties) {
    var geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat]
        },
        "properties": properties
    };
    var marker = L.mapbox.featureLayer()
        .setGeoJSON(geojson)
        .getLayers()[0];
    return marker;
}
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$(document).on('click', '#btn-submit-dumpster', function (event) {
    event.preventDefault();
    var title = $("#add-source-title").val();
    var opinion = $("#add-opinion").val();
    var name = $("#add-name").val();
    var comment = $("#add-comment").val();
    var lat = new_place_marker.getLatLng().lat;
    var lng = new_place_marker.getLatLng().lng;
    success = function (data, textStatus, jqXHR) {
        template = templates.marker_popup(data['properties']);
        $('#sidebar-content').html(template);
        $('#sidebar').show();
        alert("Thanks, the place has been added!")
        map_container.map.removeLayer(new_place_marker);
        dumpsters.layer.redraw();
        // todo: Remove marker from map or set new color
        // todo: Show modal dialog
    };
    error = function (jqXHR, textStatus, errorThrown) {
        if (jqXHR['responseText'] == '{"voting_set":[{"comment":["This field may not be blank."]}]}') {
            message = "Comment may not be blank."
        }
        $("#add-dumpster-warning").html(message).show();
    };
    add_dumpster(title, lng, lat, opinion, comment, name, on_success = success, on_error = error);
});
