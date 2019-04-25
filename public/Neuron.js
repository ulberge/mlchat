
// create a class that tracks data about neuron and calculates stuff
class Neuron {
  constructor() {
    this.attrHistory = [];
    this.ra = [];
  }

  addAttr = (attr) => {
    this.attrHistory.push(attr);
  }

  getAttrHistory = (windowSize = 1) => {
    this.ra = [];
    if (this.attrHistory.length >= windowSize) {
      const start = this.attrHistory.slice(0, windowSize);
      let sum = start.reduce((total, num) => total + num);
      const first = sum / windowSize;
      this.ra = [first];
      for (let i = windowSize; i < this.attrHistory.length; i++) {
        sum += this.attrHistory[i];
        sum -= this.attrHistory[i - windowSize];
        const avg = sum / windowSize;
        this.ra.push(avg);
      }
    }
    return this.ra;
  }

  getEventHistory = (canon, windowSize = 1) => {
    const attrData = this.ra;
    const eventData = [];
    for (let i = 0; i < windowSize; i++) {
      eventData.push(null);
    }

    let previousBaselineMax = 0;
    for (let i = windowSize; i < attrData.length; i++) {
      let currentBaseline = attrData[i - windowSize];

      // Dont retreat past previous baseline
      if (currentBaseline < previousBaselineMax) {
        currentBaseline = previousBaselineMax;
      } else {
        previousBaselineMax = currentBaseline;
      }

      const current = attrData[i];
      // Subtract off baseline, dont go below zero, scale by canon
      const delta = Math.max(current - currentBaseline, 0) / canon;
      eventData.push(delta);
    }

    return eventData;
  }

  getDiffHistory = (canon, windowSize = 1) => {
    const attrData = this.ra;
    const diffData = [];
    for (let i = 0; i < attrData.length; i++) {
      const diff = attrData[i] - canon;
      diffData.push(diff);
    }

    return diffData;
  }
}

