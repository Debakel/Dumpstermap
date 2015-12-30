/**
 * Created by m on 30.12.15.
 */

// Api Calls
function send_vote(dumpster_id, voting, options) {
    $.ajax("/api/vote/" + dumpster_id + "/" + voting, options);
}
function send_comment(dumpster_id, name, comment, on_success) {
    $.post("/api/comments/add/" + dumpster_id,
        {'name': name, 'comment': comment},
        on_success
    );
}
function getDumpsterId() {
    return id = $("#dumpster_id").val();
}