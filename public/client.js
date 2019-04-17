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
    $.get('/judge', data, function(ns_pos) {
      console.log('received biggest diffs', ns_pos);
      
      for (let i = 0; i < 3; i++) {
        const spriteN = ns_pos[i];
        const x = (-110 * (spriteN % 22)) + 'px';
        const y = (-110 * Math.floor(spriteN / 22)) + 'px';
        const id = 'viz' + i;
        $('#' + id).css('background-position', x + ' ' + y);
      }
    });
  }
  
  $('#judge').click(judge);
  $('#addIntent').click(addIntent);
  
});
