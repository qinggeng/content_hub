const kApiPrefixChanged = {
  id: 'api_prefix_changed',
};

const messageCenter = {
  subscribe: function(message_type, handler, target) {
    if (false == (message_type in this.listenedMessages))
    {
      this.listenedMessages[message_type] = {},
      window.addEventListener("message", this.dispatchMessage.bind(this), true);
    }
    this.listenedMessages[message_type][target] = handler;
  },
  dispatchMessage: function(ev) {
    try
    {
      msg = ev.data;
      let msg_type = msg.type;
      if (msg_type in this.listenedMessages)
      {
        let handlers = this.listenedMessages[msg_type]
        for (var target in handlers)
        {
          let handler = handlers[target];
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
