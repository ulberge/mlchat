// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  function addIntent() {
    const url = $('#intent').attr('src');
    const data = {
      url: url
    };
    $.post('/intent/new', data, function() {
     console.log('finished adding intent'); 
    });
  }
  
  function judge() {
    const url = $('#drawing').attr('src');
    const data = {
      url: url
    };
    $.get('/judge', data, function(result) {
      console.log('received biggest diffs', result);
      
      $('#vizs').empty();
      const text = $('<span>What about something like </span>');
      $('#vizs').append(text);
      
      for (let i = 0; i < 10; i++) {
        const spriteN = result[i][0];
        const x = (-110 * (spriteN % 22)) + 'px';
        const y = (-110 * Math.floor(spriteN / 22)) + 'px';
        const id = 'viz' + i;
        const div = $('<span class="viz_sprite">');
        div.css('background-position', x + ' ' + y);
        $('#vizs').append(div);
      }
      const text2 = $('<span>?</span>');
      $('#vizs').append(text2);
    });
  }
  
  $('#judge').click(judge);
  $('#addIntent').click(addIntent);
  
});
