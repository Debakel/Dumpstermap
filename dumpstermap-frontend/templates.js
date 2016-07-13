/**
 * Created by m on 11.05.16.
 */

setup_handlebars();
function setup_handlebars() {
    // Setup Handlebars (Load Handlebars Helpers)
    Handlebars.registerHelper('listItem', function (from, to, context, options) {
        /*
         * Item helper.
         *
         *  {{#listItem 2 6 articles}}
         *      {{> article }}
         *  {{/listItem}}
         *
         *
         *  @return n elements
         */
        var item = "";
        for (var i = from, j = to; i < j; i++) {
            item = item + options.fn(context[i]);
        }
        return item;
    });
}
// ========= Handlebars ==============
var templates = {
    'marker_popup': Handlebars.compile($("#dumpster-sidebar-template").html()),
    'dumpster_modal_template': Handlebars.compile($("#dumpster-modal-template").html()),
    'marker_popup_comments': Handlebars.compile($("#dumpster_popup_comments_template").html()),
    'add_dumpster_template': Handlebars.compile($("#add-dumpster-template").html())

};