"use strict";
let field_criteria_defines = (() => {

  const predicts = {
    get contains() 
    {
      return {
        'key': 'contains',
        'display': '包含',
      }; 
    },
    get higher_than()
    {
      return {
        'key': 'higher_than',
        'display': '高于',
      }; 
    },
    get lower_than()
    {
      return {
        key: 'lower_than',
        display: '低于',
      };
    },
    get belongs_to()
    {
      return {
        key: 'belongs_to',
        display: '属于',
      };
    },
  };

  let field_definition_full_text = (()=>
  {
    return {
      name: 'title', 
      display: '标题', 
      available_predicts: [
        predicts.contains,
        // predicts.notContains,
        // predicts.startsWith,
        // predicts.endsWith,
        // predicts.regex,
      ],
      data_traits: {
        edit_type : 'textEdit',
        editable  : true,
        update    : function(val){},
      },
      applyValue: function(val) {
        return val;
      }
    };
  })();

  let field_definition_priority = (()=>
  {
    let field_editors = {};
    field_editors[predicts.belongs_to.key] =
    {
      data_traits:
      {
        edit_type: 'multiple_choice',
        editable: true,
        update   : function(val){},
        get choices() 
        {
          return store.configCache.priority;
        },
      },
      apply_value: function(val) 
      {
        if (typeof val != 'Array')
        {
          val = Number(val);
          if (isNaN(val))
          {
            return [];
          }
          return [val];
        }
        return val;
      },
    };
    field_editors[predicts.higher_than.key] =
    {
      data_traits:
      {
        edit_type: 'choice',
        editable: true,
        update   : function(val){},
        get choices() 
        {
          return store.configCache.priority;
        },
      },
      apply_value: function(val) {
        var filtered = this.data_traits.choices.filter(x=> x.val === val);
        if (filtered.length == 0)
        {
          return this.data_traits.choices[0].val;
        }
        return val;
      }
,
    };
    return {
      name      : 'priority',
      display   : '优先级',
      available_predicts: [
        predicts.higher_than,
        predicts.belongs_to,
        // predicts.lower_than,
        // predicts.equals,
        // predicts.higherOrEqual,
        // predicts.lowerOrEqual,
        // predicts.notContains,
        // predicts.startsWith,
        // predicts.endsWith,
        // predicts.regex,
      ],
      field_editors: field_editors,
      data_traits: {
        edit_type: 'choice',
        editable: true,
        update   : function(val){},
        get choices() 
        {
          return store.configCache.priority;
        },
      },
      applyValue: function(val) {
        var filtered = this.data_traits.choices.filter(x=> x.val === val);
        if (filtered.length == 0)
        {
          return this.data_traits.choices[0].val;
        }
        return val;
      }
    };
  })();

  let field_definition_project = (()=>
  {
    return {
      name: 'project',
      display: '项目',
      available_predicts: [
        predicts.belongs_to,
      ],
      data_traits: 
      {
        edit_type: 'multiple_choice',
        editable: true,
        update: function (val) {},
        get choices ()
        {
          return store.configCache.projects.map(x=> ({val: x.name, display: x.name}));
        },
      },
      applyValue: function(val)
      {
        return val;
      },
    };
  })();

  const criteriaDefines = {
    predicts: predicts,
    fields: [
      field_definition_full_text,
      field_definition_priority,
      field_definition_project,
    ],
  };

  const fieldTraits = {
    edit_type: 'choice',
    editable: true,
    choices: criteriaDefines.fields.map(x => {return {val: x.name, display: x.display};}),
  };

  return {predicts, criteriaDefines, fieldTraits};
})();
