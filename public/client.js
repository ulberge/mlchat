// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  const layer = 'mixed4c';
  let messageTimer = 0;

  function getIconStr(icon) {
    const [ id, attr ] = icon;
    const spriteN = id;
    const x = (-110 * (spriteN % 22)) + 'px';
    const y = (-110 * Math.floor(spriteN / 22)) + 'px';
    let style = 'background-position: ' + x + ' ' + y + '; ';
    style += 'top: ' + (Math.random() * 80) + 'px; ';
    style += 'right: ' + (Math.random() * 10) + 'px; ';
    const icon_url = 'url(\'https://storage.googleapis.com/lucid-static/building-blocks/googlenet_spritemaps/sprite_' + layer + '_channel_alpha.jpeg\')';
    style += 'background-image: ' + icon_url + ';';
    const elStr = '<span class="viz_sprite sprite' + spriteN + '" style="' + style + '"></span>';
    return elStr;
  }

  function getToTryMessageEl(icons, max) {
    const toShow = icons.slice(0, max);
    const options = toShow.map(getIconStr).join('');

    const toTry = [
      `<span>What about something like </span>${options}<span>?</span>`,
      `<span>Maybe </span>${options}<span> would make it look more like a dog.</span>`,
      `<span>I think it could use more </span>${options}<span> shapes in it...</span>`,
      `<span>How about more </span>${options}<span> in the figure?</span>`
    ];
    const messageEl = toTry[Math.floor(Math.random()*toTry.length)];
    return $(`<div>${messageEl}</div>`);
  }

  function getNiceJobMessageEl(icons, max) {
    const toShow = icons.slice(0, max);
    const options = toShow.map(getIconStr).join('');

    const toTry = [
      `<span>Wow, you did a good job with </span>${options}<span>!</span>`,
      `${options}<span> seems better than it was...</span>`,
      `<span>Nice work with </span>${options}<span>.</span>`,
      `<span>I like how you incorporated the </span>${options}<span> shape into it.</span>`,
    ];
    const messageEl = toTry[Math.floor(Math.random()*toTry.length)];
    return $(`<div>${messageEl}</div>`);
  }

  function renderVizualizations(container, idAttr) {
    const bad = [];
    //for (let i = 0; i < 3; i++) {
    for (let i = 0; i < idAttr.length; i++) {
      let [ id, attr ] = idAttr[i];
      if (attr.length && attr.length === 3) {
        bad.push(id);
        attr = '' + attr[0] + ', Improvement: ' + (attr[1]) + ', Var: ' + (attr[2]);
      }
      const spriteN = id;
      const x = (-110 * (spriteN % 22)) + 'px';
      const y = (-110 * Math.floor(spriteN / 22)) + 'px';
      const vizContainer = $('<div style="display: inline-block;"></div>');
      const div = $('<div class="viz_sprite sprite' + spriteN + '"></div>');
      div.css('background-position', x + ' ' + y);
      div.css('background-image', 'url("https://storage.googleapis.com/lucid-static/building-blocks/googlenet_spritemaps/sprite_' + layer + '_channel_alpha.jpeg")');
      vizContainer.append(div);
      const div2 = $('<div>Loss: ' + attr + '</div>');
      vizContainer.append(div2);
      container.append(vizContainer);
    }
    console.log(bad);
  }

  function judge(el) {
    const drawing = el.parent('.testCol').find('.colImg');
    const vizContainer = el.parent('.testCol').find('.vizCol');
    const vizContainer2 = el.parent('.testCol').find('.vizCol2');
    const url = drawing.attr('src');
    // const url = '/public/dog_eye.jpg';
    const data = {
      url: url,
      layer: layer
    };
    const start = Date.now();
    console.log('start judge');
    $.get('/judge', data, function(result) {
      const diffs = result;
      const end = Date.now();
      console.log('judged in', end - start);

      vizContainer.empty();
      renderVizualizations(vizContainer, diffs);
      // vizContainer2.empty();
      // renderVizualizations(vizContainer2, actual);
    });
  }

  $('.judge').click(function() { judge($(this)); });

  if ($('#my_camera').length) {
    Webcam.set({
      width: 300,
      height: 225,
      image_format: 'jpeg',
      jpeg_quality: 80,
      crop_width: 224,
      crop_height: 224,
      constraints: { deviceId: '64038ce11d262ba02874fb73f598dccbc7ad513c4a99163c522eb7a1f6ec4572' }
    });
    Webcam.attach('#my_camera');

    function takeSnapshot() {
      // take snapshot and get image data
      Webcam.snap(judgeDataURL);
    }

    function judgeDataURL(dataURL) {
      const data = {
        dataURL: dataURL,
        layer: layer
      };
      const start = Date.now();
      console.log('start judge dataURL');
      $.get('/judge_data_url', data, function(result) {
        const container = $('#chatbot');
        if (result && result.length > 0) {
          const [ suggestions, improvements ] = result;
          const end = Date.now();
          console.log('judged in', end - start);

          if (messageTimer === 0) {
            console.log('show new message');
            container.empty();
            if (suggestions.length > 0) {
              const messageEl = getToTryMessageEl(suggestions, 3);
              container.append(messageEl);
            }
            if (improvements.length > 0) {
              const encouragement = getNiceJobMessageEl(improvements, 3);
              container.append(encouragement);
            }
            messageTimer = 3;
          }
          messageTimer--;

          const impViz = $('#improvements');
          impViz.empty();
          renderVizualizations(impViz, improvements);

          const sugViz = $('#suggestions');
          sugViz.empty();
          renderVizualizations(sugViz, suggestions);
        }

        takeSnapshot();
      });
    }

    $('#realtime').click(takeSnapshot);
  }

  function addIntents(callback) {
    const urls = [
      // '/public/dog_full/wc2_2.jpg',
      // '/public/dog_full/wc2_5.jpg',
      // '/public/dog_full/wc2_4.jpg',
      // '/public/dog_full/wc2_8.jpg',
      '/public/dog.jpg',
    ];
    const data = {
      urls: urls.join(','),
      layer: layer
    };
    const start = Date.now();
    console.log('start add intents');
    $.post('/intent/add_all', data, function(result) {
      const end = Date.now();
      console.log('intents added in', end - start);

      $('.intents').empty();
      urls.forEach(function(url) {
        const img = $('<img src="' + url + '" />');
        $('.intents').append(img);
      });

      if (takeSnapshot) {
        takeSnapshot();
      }
    });
  }

  function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap( function(data_uri) {
      // display results in page
      document.getElementById('results').innerHTML =
        '<h2>Here is your image:</h2>' +
        '<img src="'+data_uri+'"/>';
    } );
  }
  window.take_snapshot = take_snapshot;

  // addIntents();
  if (takeSnapshot) {
    $.post('/clear', function() {
      setTimeout(takeSnapshot, 2000);
    });
  }

});
