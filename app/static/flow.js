"use strict";

function Flow() {
  this.getIssueTypes = function() {
    $.getJSON('/api/issue_types', function(jd) {
      if (jd) {
        var sel = $('#issue_type');
        sel.html('');
        $.each(jd, function(key, value) {
            sel.append('<option key="' + value['id'] + '">' + value['name'] + "</option>")
        });
      }
    });
  };
};

var flow = new Flow();
