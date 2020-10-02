function load_ajax_url(my_url,data={}) {
  // show_loading();
  $.ajax({
    type: "GET",
    url: my_url,
    data: data,
    success: function(msg) {
      hide_error();
      $("#div-content").html(msg + "<br>");
    },
    error: function(jqXHR, textStatus, errorThrown) {
      show_error("Error #" + jqXHR.status + ": " + errorThrown);
    }
  });
}
function wipe_status() {
    $("#result").html("");
    $("#result").removeClass("alert").removeClass("alert-success").removeClass("alert-warning").removeClass("alert-danger");
}
function update_status(msg) {
    $("#result").addClass("alert");
    if(msg.indexOf('Error') > -1) {
        $("#result").removeClass("alert-success").removeClass("alert-warning").addClass("alert-danger");
    } else if(msg.indexOf('Warning:') > -1) {
        $("#result").removeClass("alert-success").removeClass("alert-danger").addClass("alert-warning");
    } else {
        $("#result").removeClass("alert-danger").removeClass("alert-warning").addClass("alert-success");
    }
   //$("#result").html('<button aria-hidden="true" data-dismiss="alert" class="close" type="button">×</button>' + msg);
   $("#result").html(msg);
   // For future use: <a class="alert-link" href="#">Alert Link</a>
}

function show_loading() {
    $("#div-alert").addClass("alert-warning").removeClass("alert-success").removeClass("alert-danger");
    $("#div-alert").html("Loading, please wait...");
    $("#div-alert").show();
  }
  function hide_error() {
    $("#div-alert").html("");
    $("#div-alert").removeClass("alert-warning").removeClass("alert-success").removeClass("alert-danger");
    $("#div-alert").hide();
  }
  function show_error(errormsg) {
    $("#div-alert").removeClass("alert-warning").removeClass("alert-success").addClass("alert-danger");
    $("#div-alert").html(errormsg);
    $("#div-alert").show();
  }
    