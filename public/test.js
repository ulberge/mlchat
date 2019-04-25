$(function() {
  const layer = 'mixed4d';

  const ears = [15];
  const legs = [215];
  const snout = [21];

  const path = '/public/test';
  const folder11 = path + '/dog_1_1/';
  const folder12 = path + '/dog_1_2/';
  const folder13 = path + '/dog_1_3/';
  const folder21 = path + '/dog_2_1/';
  const folder22 = path + '/dog_2_2/';
  const folder23 = path + '/dog_2_3/';
  const imgs = {
    full: 'dog.jpg',
    noears: 'dog_noears.jpg',
    nolegs: 'dog_nolegs.jpg',
    nosnout: 'dog_nosnout.jpg',
    noears_nolegs: 'dog_noears_nolegs.jpg',
    noears_nosnout: 'dog_noears_nosnout.jpg',
    nolegs_nosnout: 'dog_nolegs_nosnout.jpg',
    noears_nolegs_nosnout: 'dog_noears_nolegs_nosnout.jpg',
  }

  const tests = [
    {
      name: 'Reveal Ears',
      description: 'Hide just ears, then show',
      imgs: [
        folder13 + 'blank.jpg',
        folder11 + imgs.noears,
        folder11 + imgs.full,
        folder13 + 'blank.jpg',
        folder12 + imgs.noears,
        folder12 + imgs.full,
        folder13 + 'blank.jpg',
        folder13 + imgs.noears,
        folder13 + imgs.full,
        folder13 + 'blank.jpg',
        folder21 + imgs.noears,
        folder21 + imgs.full,
        folder13 + 'blank.jpg',
        folder22 + imgs.noears,
        folder22 + imgs.full,
        folder13 + 'blank.jpg',
        folder23 + imgs.noears,
        folder23 + imgs.full
      ],
      expectedResults: [
        { suggestions: [ears, legs, snout], improvements: [] },
        { suggestions: [legs, snout], improvements: [ears] },
      ]
    },
    // {
    //   name: 'Reveal Legs',
    //   description: 'Hide just legs, then show',
    //   imgs: [
    //     folder11 + imgs.nolegs,
    //     folder11 + imgs.full,
    //     folder12 + imgs.nolegs,
    //     folder12 + imgs.full,
    //     folder13 + imgs.nolegs,
    //     folder13 + imgs.full,
    //     folder21 + imgs.nolegs,
    //     folder21 + imgs.full,
    //     folder22 + imgs.nolegs,
    //     folder22 + imgs.full,
    //     folder23 + imgs.nolegs,
    //     folder23 + imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, legs, snout], improvements: [] },
    //     { suggestions: [ears, snout], improvements: [legs] },
    //   ]
    // },
    // {
    //   name: 'Reveal Snout',
    //   description: 'Hide just snout, then show',
    //   imgs: [
    //     folder11 + imgs.nosnout,
    //     folder11 + imgs.full,
    //     folder12 + imgs.nosnout,
    //     folder12 + imgs.full,
    //     folder13 + imgs.nosnout,
    //     folder13 + imgs.full,
    //     folder21 + imgs.nosnout,
    //     folder21 + imgs.full,
    //     folder22 + imgs.nosnout,
    //     folder22 + imgs.full,
    //     folder23 + imgs.nosnout,
    //     folder23 + imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, legs, snout], improvements: [] },
    //     { suggestions: [ears, legs], improvements: [snout] },
    //   ]
    // },
    // {
    //   name: 'Multiple Reveal Test 1',
    //   description: 'start with features hidden. add ears, add legs, add snout',
    //   imgs: [
    //     folder11 + imgs.noears_nolegs_nosnout,
    //     folder11 + imgs.nolegs_nosnout,
    //     folder11 + imgs.nosnout,
    //     folder11 + imgs.full,
    //     folder12 + imgs.noears_nolegs_nosnout,
    //     folder12 + imgs.nolegs_nosnout,
    //     folder12 + imgs.nosnout,
    //     folder12 + imgs.full,
    //     folder13 + imgs.noears_nolegs_nosnout,
    //     folder13 + imgs.nolegs_nosnout,
    //     folder13 + imgs.nosnout,
    //     folder13 + imgs.full,
    //     folder21 + imgs.noears_nolegs_nosnout,
    //     folder21 + imgs.nolegs_nosnout,
    //     folder21 + imgs.nosnout,
    //     folder21 + imgs.full,
    //     folder22 + imgs.noears_nolegs_nosnout,
    //     folder22 + imgs.nolegs_nosnout,
    //     folder22 + imgs.nosnout,
    //     folder22 + imgs.full,
    //     folder23 + imgs.noears_nolegs_nosnout,
    //     folder23 + imgs.nolegs_nosnout,
    //     folder23 + imgs.nosnout,
    //     folder23 + imgs.full,
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, legs, snout], improvements: [] },
    //     { suggestions: [legs, snout], improvements: [ears] },
    //     { suggestions: [snout], improvements: [legs, ears] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
    // {
    //   name: 'Multiple Reveal Test 2',
    //   description: 'start with features hidden. add legs, add snout, add ears',
    //   imgs: [
    //     folder11 + imgs.noears_nolegs_nosnout,
    //     folder11 + imgs.noears_nosnout,
    //     folder11 + imgs.noears,
    //     folder11 + imgs.full,
    //     folder12 + imgs.noears_nolegs_nosnout,
    //     folder12 + imgs.noears_nosnout,
    //     folder12 + imgs.noears,
    //     folder12 + imgs.full,
    //     folder13 + imgs.noears_nolegs_nosnout,
    //     folder13 + imgs.noears_nosnout,
    //     folder13 + imgs.noears,
    //     folder13 + imgs.full,
    //     folder21 + imgs.noears_nolegs_nosnout,
    //     folder21 + imgs.noears_nosnout,
    //     folder21 + imgs.noears,
    //     folder21 + imgs.full,
    //     folder22 + imgs.noears_nolegs_nosnout,
    //     folder22 + imgs.noears_nosnout,
    //     folder22 + imgs.noears,
    //     folder22 + imgs.full,
    //     folder23 + imgs.noears_nolegs_nosnout,
    //     folder23 + imgs.noears_nosnout,
    //     folder23 + imgs.noears,
    //     folder23 + imgs.full,
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, legs, snout], improvements: [] },
    //     { suggestions: [ears, snout], improvements: [legs] },
    //     { suggestions: [ears], improvements: [legs, snout] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
    // {
    //   name: 'Multiple Reveal Test 3',
    //   description: 'start with features hidden. add snout, add ears, add legs',
    //   imgs: [
    //     imgs.noears_nolegs_nosnout,
    //     imgs.noears_nolegs,
    //     imgs.nolegs,
    //     imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, legs, snout], improvements: [] },
    //     { suggestions: [legs, ears], improvements: [snout] },
    //     { suggestions: [legs], improvements: [snout, ears] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
    // {
    //   name: 'Midway Reveal Test 1',
    //   description: 'start w/ ears, add legs, add snout',
    //   imgs: [
    //     imgs.nolegs_nosnout,
    //     imgs.nosnout,
    //     imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [legs, snout], improvements: [ears] },
    //     { suggestions: [snout], improvements: [legs, ears] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
    // {
    //   name: 'Midway Reveal Test 2',
    //   description: 'start w/ legs, add ears, add snout',
    //   imgs: [
    //     imgs.noears_nosnout,
    //     imgs.nosnout,
    //     imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [ears, snout], improvements: [legs] },
    //     { suggestions: [snout], improvements: [legs, ears] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
    // {
    //   name: 'Midway Reveal Test 3',
    //   description: 'start w/ snout, add legs, add ears',
    //   imgs: [
    //     imgs.nolegs_nosnout,
    //     imgs.nosnout,
    //     imgs.full
    //   ],
    //   expectedResults: [
    //     { suggestions: [legs, ears], improvements: [snout] },
    //     { suggestions: [ears], improvements: [legs, snout] },
    //     { suggestions: [], improvements: [ears, legs, snout] }
    //   ]
    // },
  ];

  function getIconStr(idAttr) {
    const spriteN = idAttr[0];
    const details = idAttr[1] !== undefined ? `[${idAttr[1]}]` : '';
    const x = (-110 * (spriteN % 22)) + 'px';
    const y = (-110 * Math.floor(spriteN / 22)) + 'px';
    let style = 'background-position: ' + x + ' ' + y + '; ';
    const icon_url = 'url(\'https://storage.googleapis.com/lucid-static/building-blocks/googlenet_spritemaps/sprite_' + layer + '_channel_alpha.jpeg\')';
    style += 'background-image: ' + icon_url + ';';
    const elStr = `<div style="display:inline-block;"><div class="viz_sprite sprite${spriteN}" style="${style}"></div><div>${spriteN}: ${details}</div></div>`;
    return elStr;
  }

  function getResultsRow(results, className) {
    const { suggestions, improvements } = results;
    const divS = $(`<div class="test-parts-row ${className}"><span class="partLabel">S: </span></div>`);
    suggestions.forEach(id => {
      const iconStr = getIconStr(id);
      divS.append($(iconStr));
    });

    const divI = $(`<div class="test-parts-row ${className}"><span class="partLabel">I: </span></div>`);
    improvements.forEach(id => {
      const iconStr = getIconStr(id);
      divI.append($(iconStr));
    });
    return [ divS, divI ];
  }

  function isOutputCorrect(expected, actual) {
    const { suggestions, improvements } = expected;
    if (suggestions.length !== actual.suggestions.length || improvements.length !== actual.improvements.length) {
      return false;
    }
    let isCorrect = true;
    const actSIds = actual.suggestions.map(actS => actS[0]);
    suggestions.forEach(s => {
      const expId = s[0];
      if (!actSIds.includes(expId)) {
        isCorrect = false;
      }
    });
    const actIIds = actual.improvements.map(actI => actI[0]);
    improvements.forEach(i => {
      const expId = i[0];
      if (!actIIds.includes(expId)) {
        isCorrect = false;
      }
    });
    return isCorrect;
  }

  async function runTest(test) {
    // add test to page
    const { name, description, imgs, expectedResults } = test;
    console.log(name, ' run test');
    await reset();
    const divName = $(`<div>${name}</div>`);
    const divDesc = $(`<div>${description}</div>`);
    const divHeader = $('<div class="test-header col-md-2"></div>');
    divHeader.append(divName);
    divHeader.append(divDesc);

    const divParts = $('<div class="test-parts col-md-8"></div>');
    const container = $('.testContainer');
    const divTestRow = $('<div class="test-row col-md-12"></div>');
    container.append(divTestRow);
    divTestRow.append(divHeader);
    divTestRow.append(divParts);

    let passed = 0;
    let total = 0;
    console.log(name, ' check images: ', imgs.length);
    for (let i = 0; i < imgs.length; i++) {
      const src = imgs[i];
      console.log(name, ' check image: ', src);
      const divImg = $(`<div><img src="${src}" /></div>`);
      console.log('i', i);
      // const [ divExpS, divExpI ] = getResultsRow(expectedResults[i], '');

      const divPart = $('<div class="test-part col-md-3"></div>');
      divPart.append(divImg);
      // divPart.append(divExpS);
      // divPart.append(divExpI);
      divParts.append(divPart);

      // send image to server and get results
      const results = await judge(src);
      console.log(name, ' received results for image: ', src);
      // const results = { suggestions: [ears, legs, snout], improvements: [] };
      const [ divActS, divActI ] = getResultsRow(results, 'actual');
      divPart.append(divActS);
      // divPart.append(divActI);

      // if (isOutputCorrect(expectedResults[i], results)) {
      //   passed += 1;
      // }
      // total += 1;
    }
    console.log(name, ' finished checking images');

    // const message = passed === total ? '<span style="color: green">Passed</span>' : `<span style="color: red">Failed: ${total-passed}/${total}</span>`;
    const message = 'finished';
    const divResults = $(`<div class="test-results col-md-2">${message}</div>`);
    divTestRow.append(divResults);
  }

  function reset() {
    console.log('reset');
    return new Promise(resolve => {
      $.post('/test/reset', resolve);
    });
  }

  function judge(src) {
    console.log('judge', src);
    return new Promise(resolve => {
      const data = {
        url: src,
        layer: layer
      };
      $.post('/test/judge', data, function(result) {
        const [ suggestions, improvements ] = result;
        resolve({ suggestions, improvements });
      });
    });
  }

  async function runTests() {
    for (let i = 0; i < tests.length; i++) {
      console.log('run test #: ' + (i + 1));
      await runTest(tests[i]);
      console.log('finished test #: ' + (i + 1));
    }
  }

  runTests();
});
