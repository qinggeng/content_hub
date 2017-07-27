'use strict';
let status_bar = (()=>{
let template = `
<div :style = 'defaultStyles.frame'>
  <div :style = 'appliedStyles.loading_indicator'>
    <span>{{'========================================='.slice(0, this.time_count)}}</span>
  </div>
</div>
`;

let frame_style = {
  position: 'fixed',
  height: '24px',
  left: '0px',
  right: '0px',
  bottom: '0px',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'flext-start',
  alignItems: 'center',
  zIndex: 1,
  background: 'rgb(224, 224, 224)',
};

let loading_indicator_style = {
  position: 'absolute',
  left: 0,
  right: 0,
  display: 'flex',
  justifyContent: 'flex-start',
  alignItems: 'center',
};

let component = {
  template: template,
  props: {
  },
  methods: {
  },
  data: function () {
    return {
      defaultStyles: {
        frame: extend(frame_style, {}),
        loading_indicator: extend(loading_indicator_style, {}),
      },
      backgroundProgressCount: 0,
      time_count: 0,
    };
  },
  computed: {
    appliedStyles: {
      cache: false,
      get () {
         let styles = {
          frame: this.defaultStyles.frame,
          loading_indicator: this.defaultStyles.loading_indicator,
        };
        styles.loading_indicator.visibility = this.backgroundProgressCount > 0 ? 'visible' : 'hidden';
        return styles;
      },
    },
  },
  created: function () {
    messageCenter.subscribe(kBackgroundProgressBegin.id, (()=>{
      this.backgroundProgressCount += 1;
    }).bind(this), this);
    messageCenter.subscribe(kBackgroundProgressEnd.id, (()=>{
      this.backgroundProgressCount -= 1;
    }).bind(this), this);
    window.setInterval(((ev) =>
    {
      this.time_count = (this.time_count + 1) % 40;
    }).bind(this), 100);
  },
};
return component;
})();
