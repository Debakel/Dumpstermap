/**
 * Created by m on 30.12.15.
 */

// Register events
/*map.on('move', function () {
 updateListing();
 });*/
$('#featureModal').on('hidden.bs.modal', function (e) {
    $('#sidebar').show();
});
map_container.map.on('click',
    function (e) {
        if (!adding_new)
            $('#sidebar2-right').addClass("hidden");
    }
);

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

var new_dumpster;
var adding_new = false;
$(document).on('click', '#btn-add-dumpster', function (event) {
    event.preventDefault();
    adding_new = true;
    var html = templates.add_dumpster_template();
    $('#sidebar-dumpster-info').html(html);
    $('#sidebar2-right').removeClass("hidden");

    if (new_dumpster != null)
        map_container.map.removeLayer(new_dumpster);
    new_dumpster = new L.marker(map_container.map.getCenter(), {draggable: 'true'});
	map_container.map.addLayer(new_dumpster);
});

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$(document).on('click', '#btn-submit-dumpster', function (event) {
    event.preventDefault();
    var title = $("#add-source-title").val();
    var opinion = $("#add-opinion").val();
    var name = $("#add-name").val();
    var comment = $("#add-comment").val();
    var lat = new_dumpster.getLatLng().lat;
    var lng = new_dumpster.getLatLng().lng;
	success = function(data, textStatus, jqXHR ){
				template = templates.marker_popup(data['properties']);
				$('#sidebar-dumpster-info').html(template);
                $('#sidebar2-right').removeClass("hidden");
		};
	error = function(jqXHR, textStatus, errorThrown){
		alert('error:' + errorThrown);
		};
    add_dumpster(title, lng, lat, opinion, comment, name, on_success=success, on_error = error);
});
