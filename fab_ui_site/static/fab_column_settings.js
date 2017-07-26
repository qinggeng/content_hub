let fab_column_settings = (()=>
{
  let tidColumn = {
    value     : '编号',
    accessor  : 'tid',
    editable  : false,
    edit_type : 'textEdit',
  };
  let titleColumn = {
    value          : '标题',
    accessor       : 'task',
    editable       : true,
    edit_type      : 'textEdit',
    editor_pattern : 'inplace',
    update         : function(row, val) {
      row.task = val;
    },
  };
  let authorColumn = {
    value    : '作者',
    accessor : (row, traits)=>
    {
      let val = row.author;
      try
      {
        return traits.choices.filter(x => x.display == val)[0].val;
      }
      catch(ex)
      {
        return val;
      }
    }, 
    editable       : false,
    edit_type      : 'choice',
    editor_pattern : 'inplace',
    get choices()
    { 
      let ret = store.configCache.users.map(x=>
      {
        return {val: x.userName, display: x.realName};
      });
      return ret;
    }, 
  };
  let assignedColumn = {
    value    : '负责人',
    accessor : (row, traits)=>
    {
      let val = row.assigned;
      try
      {
        return traits.choices.filter(x => x.display == val)[0].val;
      }
      catch(ex)
      {
        return val;
      }
    }, 
    editable       : true,
    edit_type      : 'choice',
    editor_pattern : 'inplace',
    get choices()
    { 
      let ret = store.configCache.users.map(x=>
      {
        return {val: x.userName, display: x.realName};
      });
      return ret;
    }, 
    update: function(row, val) {
      val = this.choices.filter(x => x.val === val)[0].display;
      row.assigned = val;
    },
  };
  let priorityColumn = {
    value: '优先级', 
    accessor: (row, traits)=> 
    {
      let val = row.priority;
      try
      {
        return traits.choices.filter(x => x.display == val)[0].val;
      }
      catch(ex)
      {
        return val;
      }
    }, 
    editable: true, 
    edit_type: 'choice', 
    editor_pattern: 'inplace',
    get choices() 
    {
      return store.configCache.priority;
    },
    update: function(row, val) {
      val = this.choices.filter(x => x.val === val)[0].display;
      row.priority = val;
    },
  };
  let severityColumn = {
    value: '严重程度', 
    accessor: (row, traits)=> 
    {
      let val = row.severity;
      try
      {
        return traits.choices.filter(x => x.display == val)[0].val;
      }
      catch(ex)
      {
        return val;
      }
    }, 
    editable: true, 
    edit_type: 'choice', 
    editor_pattern: 'inplace',
    get choices() 
    {
      return store.configCache.severity;
    },
    update: function(row, val) {
      val = this.choices.filter(x => x.val === val)[0].display;
      row.severity = val;
    },
  };
  let projectsColumn = {
    value: '项目', 
    accessor: function (row, traits) 
    {
      try
      {
        let tags = row.tags.split(',').map(x=> x.trim());
        let values = tags.map(x=>traits.project_name_map[x]);
        return values;
      }
      catch(ex)
      {
        console.log(ex);
        return '';
      }
    }, 
    get project_name_map() {
      let ret = {};
      for (var val of this.choices)
      {
        ret[val.display] = val.val;
      }
      return ret;
    },
    editable: true, 
    edit_type: 'multiple_choise', 
    editor_pattern: 'inplace', 
    get choices() {
      let ret = store.configCache.projects.map(x =>
      {
        return {val: x.phid, display: x.name};
      });
      return ret;
    },
    update: function(row, val) {
      val = val.map(x => this.choices.filter(y => y.val == x)[0].display)
      row.tags = val.join(',');
    },
  };
  let deadlineColumn = {
    value: '计划截止时间', 
    accessor: 'deadline', 
    editable: true, 
    edit_type: 'datetime', 
    editor_pattern: 'inplace',
    default_value: 'TBD',
  };
  let descriptionColumn = {
    value          : '描述',
    accessor       : 'description',
    editable       : true,
    edit_type      : 'textEdit',
    editor_pattern : 'popup',
    update         : function(row, val) {
      row.description = val;
    },
  };

  let statusColumn = {
    value: '状态', 
    accessor: (row, traits)=> 
    {
      let val = row.status;
      try
      {
        return traits.choices.filter(x => x.display == val)[0].val;
      }
      catch(ex)
      {
        return val;
      }
    },
    update: function(row, val) {
      row.status = val;
    },
    editable: true, 
    edit_type: 'choice', 
    editor_pattern: 'inplace',
    get choices() 
    {
      return store.configCache.status;
    },
  };
  return [
    tidColumn,
    titleColumn,
    statusColumn,
    assignedColumn,
    authorColumn,
    priorityColumn,
    severityColumn,
    projectsColumn,
    deadlineColumn,
    descriptionColumn,
  ];
})();
