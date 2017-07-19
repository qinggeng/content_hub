"use strict";
const template = `
<div :style='styles.frame'>
  <input :style='styles.api' v-modle='api_prefix' type='text' :value='api_prefix' @change='api_prefix_changed'/>
</div>
`;

const styles = {
  frame: {
  },
  api: {
  },
};

const msgApiPrefixChanged = (old, n) => {
  return {
    type: 'api_prefix_changed',
    payload: {
      'last': old,
      'current': n,
    },
  };
}

const fab_setting = {
  props: {
    styles: {
      type    : Object,
      default : function(){return styles;},
    },
  },
  methods: {
    api_prefix_changed: function(ev) {
      messageCenter.publish(msgApiPrefixChanged(this.api_prefix, ev.target.value));
    },
  },
  data: function() {
    return {
      api_prefix: 'http://localhost/api/',
    };
  },
  template: template,
};
