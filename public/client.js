// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log('hello world :o')
  
  const data = {
    url: 'https://storage.googleapis.com/lucid-static/building-blocks/examples/dog_cat.png'
  };
  $.get('/judge', data, function(ns_pos) {
    console.log(ns_pos);
  });
});
