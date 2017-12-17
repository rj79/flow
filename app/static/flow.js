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

  this.createIssue = function() {
    var data = {'issue_type': $('#issue_type').children(':selected').attr('key'), 'title': $('#title').val(),
                'description': $('#description').val()};
    //console.log(data);
    $.post('/api/issues', data, function() {
      $('#createModal').modal('hide');
    });
  }
};

var flow = new Flow();
