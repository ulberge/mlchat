// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  const layer = 'mixed4d';
  const layerSize = 528;
  const className = 'Labrador retriever';
  let timePoint = 0;

  const color = {
    red: 'rgb(255, 99, 132',
    orange: 'rgb(255, 159, 64',
    yellow: 'rgb(255, 205, 86',
    green: 'rgb(75, 192, 192',
    blue: 'rgb(54, 162, 235',
    purple: 'rgb(153, 102, 255',
    grey: 'rgb(201, 203, 207'
  };
  const neuronIds = [436, 11, 428, 422, 477, 374, 308]
  const neuronIdsNames = ['ears 1', 'ears 2', 'legs 1', 'legs 2', 'snout 1', 'snout 2', 'snout 3']
  const neuronDataColor = [color.red, color.red, color.green, color.green, color.purple, color.purple, color.purple];
  const neurons = {};
  const canon = [0.7972949500000003, 0.5474324339999999, 0.7222752219999999, 0.19582462799999995, 0.631989314, 0.9711769339999995, 0.40474974];
  const windowSize = 2;
  const datasetsMap = {};
  for (let i = 0; i < layerSize; i++) {
    neurons[i] = new Neuron();
  }

  const chartCtx = document.getElementById('attrChart').getContext('2d');
  const attrChartConfig = {
      type: 'line',
      data: {
        labels: [],
        datasets: []
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Channel Attr'
            }
          }]
        }
      }
  };
  const attrChart = new Chart(chartCtx, attrChartConfig);

  const diffChartCtx = document.getElementById('diffChart').getContext('2d');
  const diffChartConfig = {
      type: 'line',
      data: {
        labels: [],
        datasets: []
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Diff with Canon'
            }
          }]
        }
      }
  };
  const diffChart = new Chart(diffChartCtx, diffChartConfig);

  const eventChartCtx = document.getElementById('eventChart').getContext('2d');
  const eventChartConfig = {
      type: 'line',
      data: {
        labels: [],
        datasets: []
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Attr minus Baseline'
            }
          }]
        }
      }
  };
  const eventChart = new Chart(eventChartCtx, eventChartConfig);

  function renderData(data, chart, config) {
    const datasets = [];
    Object.keys(data).forEach((key, i) => {
      const datasetConfig = {
          label: neuronIdsNames[i],
          data: data[key],
          backgroundColor: neuronDataColor[i] + ', 0.2)',
          borderColor: neuronDataColor[i] + ', 0.5)',
          fill: false,
          lineTension: 0
      };
      datasets.push(datasetConfig);
    });

    config.data.datasets = datasets;
    const labels = [];
    for (let i = 0; i <= timePoint; i++) {
      labels.push(i);
    }
    config.data.labels = labels;
    chart.update();
  }

  function updateNeurons(channelAttr) {
    channelAttr.forEach((attr, i) => {
      neurons[i].addAttr(attr);
    });
  }

  function getAttrData(neuronIds) {
    const ra = {};
    neuronIds.forEach(id => {
      const history = neurons[id].getAttrHistory(windowSize);
      if (history && history.length > 0) {
        ra[id] = history;
      }
    });

    return ra;
  }

  function getDiffData() {
    // subtract the canon
    const diffData = {};
    neuronIds.forEach((id, i) => {
      diffData[id] = neurons[id].getDiffHistory(canon[i], windowSize);
    });

    return diffData;
  }

  function getEventData() {
    // subtract the attrData from the moment a windowSize ago
    const eventData = {};
    neuronIds.forEach((id, i) => {
      eventData[id] = neurons[id].getEventHistory(canon[i], windowSize);
    });

    return eventData;
  }

  function renderVizualizations(container, idAttr) {
    //for (let i = 0; i < 3; i++) {
    for (let i = 0; i < idAttr.length; i++) {
      let [ id, attr ] = idAttr[i];
      if (attr.length && attr.length === 3) {
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
  }

  function takeSnapshot() {
    // take snapshot and get image data
    Webcam.snap(judgeDataURL);
  }

  let running = false;

  function judgeDataURL(dataURL) {
    const data = {
      dataURL: dataURL,
      layer: layer,
      className: className
    };
    const start = Date.now();
    console.log('start judge dataURL');
    $.get('/judge_data_url', data, function(result) {
      if (result) {
        updateNeurons(result);

        const attrData = getAttrData(neuronIds);
        if (Object.keys(attrData).length > 0) {
          console.log('results', Object.keys(attrData).map(key => attrData[key][attrData[key].length - 1]));
          // console.log('results', attrData.map(data => data[data.length - 1]));
          renderData(attrData, attrChart, attrChartConfig);

          const diffData = getDiffData();
          renderData(diffData, diffChart, diffChartConfig);

          const eventData = getEventData();
          renderData(eventData, eventChart, eventChartConfig);
          timePoint += 1;
        }
      }

      if (running) {
        takeSnapshot();
      }
    });
  }

  // function runMachine() {
  //   console.log('test');
  //   takeSnapshot();
  //   setTimeout(runMachine, 200);
  // }

  function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap( function(data_uri) {
      $('#snapshots').append(`<div style="display: inline-block;margin: 10px;"><img style="width: 120px" src="${data_uri}"/><div>Time: ${timePoint}</div></div>`);
    } );
  }
  window.take_snapshot = take_snapshot;

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

    $('#toggleRun').click(() => {
      running = !running;
      if (running) {
        take_snapshot();
        takeSnapshot();
      }
    });
    // setTimeout(() => takeSnapshot(), 2000);
    // setTimeout(() => runMachine(), 2000);
  }

});
