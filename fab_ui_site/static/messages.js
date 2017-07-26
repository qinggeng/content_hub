const kApiPrefixChanged = {
  id: 'api_prefix_changed',
};

const kUserListLoaded = {
  id: 'user_changed',
};

const kProjectsLoaded = {
  id: 'projects_changed',
};

const kSearchUpdated = {
  id: 'search_updated',
};

const kSearchResultUpdated = {
  id: 'search_result_updated',
};

const kBackgroundProgressBegin = {
  id: 'background_progress_begin',
};

const kBackgroundProgressEnd = {
  id: 'background_progress_end',
};

const kPriorityLoaded = {
  id: 'priority_config_updated',
};

const kSeverityLoaded = {
  id: 'severity_config_loaded',
};

const kStatusLoaded = {
  id: 'status_config_loaded',
};

const messageCenter = {
  subscribe: function(message_type, handler, target) {
    if (false == (message_type in this.listenedMessages))
    {
      this.listenedMessages[message_type] = [];
    }
    this.listenedMessages[message_type].push({
      target: target,
      handler: handler,
    })
  },
  dispatchMessage: function(ev) {
    try
    {
      msg = ev.data;
      let msg_type = msg.type;
      if (msg_type in this.listenedMessages)
      {
        let handlers = this.listenedMessages[msg_type]
        for (var dest of handlers)
        {
          let handler = dest.handler;
          try
          {
            handler(msg.payload);
          }
          catch(ex)
          {
          }
        }
      }
    }
    catch(ex)
    {
      console.log(ex);
    }
  },
  publish: function(message) {
    window.postMessage(message, '*');
  },
  listenedMessages: {},
};
window.addEventListener("message", messageCenter.dispatchMessage.bind(messageCenter), true);
