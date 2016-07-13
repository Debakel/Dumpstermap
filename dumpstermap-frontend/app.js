var map_container, dumpsters;
var backend_url = 'http://localhost:8000';
window.onload = init();

function init() {	
    // Set AJAX Headers for Django CSRF Protection
    setupCSRFProtection();

    // Setup Mapbox
    L.mapbox.accessToken = 'pk.eyJ1IjoiZGViYWtlbCIsImEiOiJjMWVJWEdFIn0.WtaUd8Rh0rgHRiyEZNzSjQ';

    // Create map
    map_container = new Map();
    map_container.bind_to_ui("map");

    // Create Tile Service Layer
    dumpsters = new DumpsterLayer(backend_url + '/dumpsters/tiles/{z}/{x}/{y}/?format=json');
    //dumpsters_clustered = new ClusteredDumpsterLayer('api/dumpster/tiles/clustered/{z}/{x}/{y}');
    dumpsters.addToMap(map_container.map, 0, 21);

    // Show welcome message
    //$('#modal-about').modal("show");
}
function setupCSRFProtection() {
    // Acquiring CSRF Token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    // Set header on AJAX requests
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
// ========= Helper functions ========
function is_mobile() {
    if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0, 4))) {
        return true;
    }
    else if (screen.width <= 480) {
        return true;
    }
    else {
        return false;
    }

}

// ========= Constructors ============
function ClusteredDumpsterLayer(endpoint_url) {
    this.endpoint = endpoint_url;

    // Bind to Tile Endpoint
    this.layer = new L.TileLayer.GeoJSON(this.endpoint, {
            clipTiles: true
        }, {
            pointToLayer: makeMarker
        }
    );
    function makeMarker(feature, latlng) {
        var icon = {
            "className": "dumpster-icon dumpster-clustered-icon", // class name to style
            "html": "&#9733;", // add content inside the marker
            "iconSize": null // size of icon, use null to set the size in CSS
        };
        return L.marker(latlng).setIcon(L.divIcon(icon));
    }

}
function DumpsterLayer(endpoint_url) {
    var self = this;
    this.visible = false;
    this.endpoint = endpoint_url;

    function makeMarker(feature, latlng) {
        /** All available marker-symbols here: https://www.mapbox.com/maki/ **/
        var votes = feature.properties.rating;
        var color, size, symbol;
        var icon = {
            "iconSize": null // size of icon, use null to set the size in CSS
        };
        if (votes == 0) {
            icon.className = "dumpster-icon dumpster-neutral-icon";
        }
        else if (votes < 0) {
            icon.className = "dumpster-icon dumpster-bad-icon";
        }
        else if (votes > 0) {
            icon.className = "dumpster-icon dumpster-good-icon";
            icon.html = "&#9733;";
        }

        return L.marker(latlng).setIcon(L.divIcon(icon));
    }

    function onEachDumpsterMarker(feature, layer) {
        var data = feature.properties;
        data = $.extend(data, {'id': feature.id})

        var popup = L.popup({minWidth: 333}).setContent(html);
        if (is_mobile()) {
            var html = templates.dumpster_modal_template(data);
            layer.on({
                click: function (e) {
                    $("#feature-title").html(data.name);
                    $("#feature-info").html(html);
                    $("#featureModal").modal("show");
                    $('#sidebar').hide();

                }
            });
        }
        else {
            var html = templates.marker_popup(data);
            layer.on({
                click: function (e) {
                    $('#sidebar-content').html(html);
                    $('#sidebar').removeClass("hidden");
                    $('#sidebar').show();
                    layer.feature.properties['old-color'] = layer.feature.properties['marker-color'];
                    layer.feature.properties['marker-color'] = '#ff8888';

                }
            });
        }

    }

    this.show = function () {
        if (!self.visible) {
            self.map.addLayer(self.layer);
            self.visible = true;
        }
    };

    this.hide = function () {
        if (self.visible) {
            self.map.removeLayer(self.layer);
            self.visible = false;
        }
    };
    function zoomendEventListener(feature) {
        var zoom = self.map.getZoom();
        if (zoom > self.min_zoom && zoom < self.max_zoom) {
            self.show();
        }
        else {
            self.hide();
        }
    }


    this.addToMap = function (map, min_zoom, max_zoom) {
        this.min_zoom = min_zoom;
        this.max_zoom = max_zoom;
        this.map = map;
        this.map.on('zoomend', zoomendEventListener);
        zoomendEventListener(this.map);

    };

// Bind to Tile Endpoint
    this.layer = new L.TileLayer.ClusteredGeoJSON(this.endpoint, {
            clipTiles: true,
            unique: function (feature) {
                return feature.properties.id;
            },
            showCoverageOnHover: false,
            pointToLayer: makeMarker,
            onEachFeature: onEachDumpsterMarker
        }
    );
}

function Map() {
    this.mapbox_layer = 'mapbox.streets';
    this.mapbox_id = 'debakel.in6i4ino';
    this.mapbox_accessToken = 'pk.eyJ1IjoiZGViYWtlbCIsImEiOiJjMWVJWEdFIn0.WtaUd8Rh0rgHRiyEZNzSjQ';
    this.bind_to_ui = function (div_id) {
        // Karte laden
        this.map = L.mapbox.map(div_id).setView([48.2633321, 10.8405515], 7);
        var tile_layer = L.mapbox.tileLayer(this.mapbox_layer, {
            attributionControl: false,
            attribution: '',
            id: this.mapbox_id,
            accessToken: this.mapbox_accessToken
        });
        this.map.addLayer(tile_layer);

        // Set controls
        this.map.addControl(L.control.locate());
        this.map.addControl(L.mapbox.infoControl());
        this.map.removeControl(this.map.attributionControl);
    };
    this.addLayer = function (layer) {
        this.map.addLayer(layer);
    }
}
