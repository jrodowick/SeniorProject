function join(event_id) {
  alert('You have confirmed attendance.');
  $.ajax({
    url: '/events/join/' + event_id + '/',
    type: 'GET',
    data: {
      id: event_id
    },
    error: function (xhr, textStatus, thrownError){
      alert("failure: " + xhr.statusText);
    },
    success: function(response) {
      //alert('Success')
      window.location.href = '/events/view/' + event_id + '/';
    }
  })
}

function add_google(event_id) {
  alert('You have added to your Google Calendar.');
  $.ajax({
    url: '/events/add_to_calendar/' + event_id + '/',
    type: 'GET',
    data: {
      id: event_id
    },
    error: function (xhr, textStatus, thrownError){
      alert("failure: " + xhr.statusText);
    },
    success: function(response) {
      //alert('Success')
      window.location.href = '/events/view/' + event_id + '/';
    }
  })
}
