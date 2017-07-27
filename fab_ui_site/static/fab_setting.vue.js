"use strict";
const template = `
<div :style='styles.frame'>
  <input :style='styles.api' v-modle='api_prefix' type='text' :value='api_prefix' @change='api_prefix_changed'/>
  <input type = 'button' value = '刷新数据' @click='on_update_config'/>
  <input type = 'button' value = '提交修改' @click='on_commit_change'/>
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
  computed: {
    apis: {
      get () {
        return {
          projects: this.api_prefix + 'projects',
          users: this.api_prefix + 'users',
          searches: this.api_prefix + 'search',
          id2j: this.api_prefix + 'id2j',
          configs: this.api_prefix + 'configs',
          commit: this.api_prefix + '/task-batch-edit-form',
        };
      },
    },
  },
  methods: {
    api_prefix_changed: function(ev) {
      this.api_prefix = ev.target.value;
      messageCenter.publish(msgApiPrefixChanged(this.api_prefix, ev.target.value));
    },
    getConfigInBackgound(api, continuous) {
      messageCenter.publish({
        type: kBackgroundProgressBegin.id, 
        payload: {},
      });
      fetch(api)
      .then(resp =>
      {
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
        if (resp.ok)
        {
          return resp.json();
        }
        else
        {
          throw `get ${api} failed!`;
        }
      })
      .then(continuous)
      .catch(ex=>{
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
        console.log(ex);
      });
    },
    updateUserConfig: function () {
      this.getConfigInBackgound(this.apis.users, (users)=>
      {
        messageCenter.publish({
          type: kUserListLoaded.id,
          payload: users,
        });
      });
    },
    updateProjectConfig: function() {
      this.getConfigInBackgound(this.apis.projects, (projects)=>
      {
        messageCenter.publish({
          type: kProjectsLoaded.id,
          payload: projects,
        });
      });
    },
    updateConfig: function () {
      this.getConfigInBackgound(this.apis.configs, (configs) =>
      {
        j2s(configs);
        messageCenter.publish({
          type: kSeverityLoaded.id,
          payload: configs.severity,
        });
        messageCenter.publish({
          type: kStatusLoaded.id,
          payload: configs.status,
        });
        messageCenter.publish({
          type: kPriorityLoaded.id,
          payload: configs.priority,
        });
      });
    },
    updateSearch: function () {
      messageCenter.publish({
        type: kBackgroundProgressBegin.id, 
        payload: {},
      });
      fetch(this.apis.searches)
      .then(resp=>
      {
        if(resp.ok)
        {
          return resp.text();
        }
        throw new 'can not get search result';
      })
      .then(ids=>{
        return fetch(this.apis.id2j + '?ids=' + ids.trim());
      })
      .then(resp=>
      {
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
        if(resp.ok)
        {
          return resp.json();
        }
        throw new 'can not get task result';
      })
      .then(ret=>
      {
        messageCenter.publish({
          type: kSearchUpdated.id,
          payload: ret,
        });
      })
      .catch(ex => {
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
        console.log(ex);
      });
    },
    on_commit_change: function (ev)
    {
      let delta = [];
      for(var i = 0; i < store.searchResult.length; i++)
      {
        let lhs = j2s(store.searchResult[i]);
        let rhs = j2s(store.originalSearchResult[i]);
        if (lhs !== rhs)
        {
          delta.push(s2j(lhs));
        }
      }
      if (delta.length == 0)
      {
        console.log('nothing to commit');
        return;
      }
      messageCenter.publish({
        type: kBackgroundProgressBegin.id, 
        payload: {},
      });
      fetch(this.apis.commit, {
        method: 'POST',
        body: j2s(delta),
        'content-type': 'application/json',
      })
      .then(((resp)=>
      {
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
      }).bind(this))
      .catch(ex => {
        messageCenter.publish({
          type: kBackgroundProgressEnd.id, 
          payload: {},
        });
        console.log(ex);
      });
    },
    on_update_config: function (ev) 
    {
      this.updateUserConfig();
      this.updateProjectConfig();
      this.updateConfig();
      this.updateSearch();
    },
  },
  data: function() {
    return {
      api_prefix: 'http://192.168.10.34:8020/api/',
    };
  },
  template: template,
};
