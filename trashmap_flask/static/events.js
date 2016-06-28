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
        $('#sidebar2-right').addClass("hidden");
    }
);
$(document).on('click', '.btn-vote', function () {
    send_vote(getDumpsterId(), $(this).attr('voting'),
        //Ajax options
        {
            // callback on success
            success: function (json) {
                //TODO: check result
                $(this).addClass('active');
                // count up
                var element = $(this).children("span[name=count]");
                var value = parseInt(element.text()) + 1;
                element.text(value);
            },
            context: $(this)
        }
    );
});
$(document).on('click', '#btn_comment', function (event) {
    event.preventDefault();
    var name = $("#txt_name").val();
    var comment = $("#txt_comment").val();
    var id = getDumpsterId();

    //update view
    var update_comments = function () {
        var html = templates.marker_popup_comments({
            'name': name,
            'comment': comment,
            'date': 'Today'
        });
        $(html).hide().appendTo("#comment_list").fadeIn(500);
    };

    send_comment(id, name, comment, update_comments);


});

$(document).on('click', '#toggle-red', function (event) {
    toggle_group(groups['red']);
});
$(document).on('click', '#toggle-green', function (event) {
    toggle_group(groups['green']);
});
$(document).on('click', '#toggle-grey', function (event) {
    toggle_group(groups['grey']);
});
$(document).on('click', '#btn-add-dumpster', function (event) {
    load_geojson("/api/dumpster/all");
    // Show instructions
    $('#add-dumpster-modal').modal("show");
});
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});