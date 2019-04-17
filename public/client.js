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
    $.post('/intent/new', data);
  }
  
  function judge() {
    const url = $('#drawing').attr('src');
    const data = {
      url: url
    };
    $.get('/judge', data, function(ns_pos) {
      console.log(ns_pos);
      
      for (let i = 0; i < 3; i++) {
        const sprite = ns_pos[i];
        const x = -110 * (spriteN'px';
        const y = 'px';
      }
      const spritemap_url = '';
      
           background-position: -2310px -110px;
    <div class="sprite" style="
        background-position: -{{sprite_size*(attr.n%sprite_n_wrap)}}px -{{sprite_size*Math.floor(attr.n/sprite_n_wrap)}}px;
      "></div>

    });
  }
  
  $('#judge').click(judge);
  $('#addIntent').click(addIntent);
  
});
