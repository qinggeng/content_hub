"use strict";
// import data_editor.vue

const searchEditorStyles = {
  container: extend(solid_border, {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'stretch',
    justifyContent: 'center',
  }),
  action_bar: extend({}, {
  }),
	criteria_container: extend(solid_border, {
		'display': 'flex',
		'min-height': '40px',
		'flex-direction': 'row',
    justifyContent: 'flex-start',
		'padding': '4px',
	}),
	criteria: {
		frame: extend(solid_border, {
			display: 'flex',
			'flex-direction': 'row',
			'align-items': 'center',
			
		}),
		sector: extend({}, {
			paddingLeft: '4px',
		}),
		xbtn: extend(solid_border, {
			margin: '0 4px',
			width: '18px',
			height: '18px',
			display: 'flex',
			'justify-content': 'center',
			'align-items': 'center',
			background: '#FF0000',
			color: '#FFFFFF',
			'border-radius': '10px',
			'font-size': '12px',
		}),
	}
};

let predict = field_criteria_defines.predicts;
let criteriaDefines = field_criteria_defines.criteriaDefines;
let fieldTraits = field_criteria_defines.fieldTraits;

const searchCriteriaTemplate = `
<div :style='styles.frame'>
	<data_editor 
		:raw_data='criteria.operate_on' 
		:data_traits='fieldTraits' 
		:current_view='"raw"'
	 	@edited='onFieldChosen'/>
	<data_editor 
		:raw_data='criteria.operator' 
		:data_traits='operator_traits'
    @edited='onPredictChoosen'
		:current_view='"raw"'/>
	<data_editor 
		:raw_data='criteria.operand' 
		:data_traits='current_field_trait || current_field.data_traits' 
		:current_view='"raw"' @edited='onCriteriaChanged'/>
	<!-- <span :style='styles.sector'>{{criteria.operand}}</span> -->
	<div :style='styles.xbtn' @click='requestRemoveCriteria'>
	Ⅹ
	</div>
</div>
`;

const searchEditorTemplate = `
<div :style='styles.container'>
  <div :style='styles.actionbar'>
    <input type='button' value='执行' @click='onTriggerSearch'/>
    <input type='button' value='重置'/>
  </div>
  <div :style='styles.criteria_container'>
    <input type='button' value = '新增' @click = 'onNewCriteria'/>
    <search_criteria 
      v-for='criteria in criterias' 
      :styles='styles.criteria' 
      :criteria='criteria' 
      @criteria-changed='((c, v)=>{updateCriteria(c, v)}).bind(undefined, criteria)'
      @request-remove-criteria='removeCriteria'/>
  </div>
</div>
`;

const searchCriteria =
{
	props: {
		styles: {
			type: Object,
		},
		criteria: {
			type: Object,
		},
		definitions: {
			type: Object,
			default: criteriaDefines,
		},
	},
	components: {
		data_editor: dataEditor,
	},
	filters: {
	},
  data: function() 
  {
    return {
      current_field_trait: 0,
    };
  },
	methods: {
		fieldDisplay: function (val) 
		{
			try
			{
				return this.field_map[val].display;
			}
			catch(ex)
			{
				console.log(ex);return '未知字段: '+ val;
			}
		},

		operatorDisplay: function (val) 
		{
			try
			{
				return this.definitions.predicts[val].display;
			}
			catch(ex)
			{
				return '不支持的操作符';
			}
		},

		makeOperatorTraits: function (val)
		{
			return {
				edit_type: 'choice',
        editable: true,
				choices: val.map(x=>{return {val: x.key, display: x.display};}),
			};
		},

		onFieldChosen: function(val) {
      if (val.current == val.origin)
      {
        return;
      }
			const criteria = this.criteria;
			//TODO send change message
			criteria.operate_on = val.current;
			let fieldDefine = this.field_map[val.current];
			let available_predicts = fieldDefine.available_predicts;
			let predict = available_predicts[0];
			if (undefined === predict)
			{
				criteria.operator = '';
				return;
			}
			criteria.operator = predict.key;
      if (undefined !== fieldDefine.field_editors)
      {
        criteria.operand = 
          fieldDefine.field_editors[predict.key].apply_value(criteria.operand);
      }
      else
      {
        criteria.operand = fieldDefine.applyValue(criteria.operand);
      }
		},

		onCriteriaChanged: function (val)
    {
      if (val.current == val.origin)
      {
        return;
      }
			const criteria = extend(this.criteria);
			//TODO send change message
			criteria.operand = val.current; 
      let payload = {
        current: criteria,
        origin: this.criteria,
      };
      this.criteria = criteria;
      this.$emit('criteria-changed', payload);
		},

		requestRemoveCriteria: function (ev) {
			this.$emit('request-remove-criteria', this.criteria);
		},

		onPredictChoosen: function(val) {
			this.criteria.operator = val.current;
			let fieldDefine = this.current_field;
      if (undefined !== fieldDefine.field_editors)
      {
        this.current_field_trait = fieldDefine.field_editors[val.current].data_traits;
        this.criteria.operand = 
          fieldDefine.field_editors[val.current].apply_value(this.criteria.operand);
      }
		},
	},// end of methods

	computed: {
		current_field: {
			cache: false,
			get() {
				return this.field_map[this.criteria.operate_on];
			},
		},
		current_predict: {
			cache: false,
			get() {
				return this.field_map[this.criteria.operate_on].available_predicts.filter(x => x.key == this.criteria.operator)[0];
			},
		},
		operator_traits: {
			cache: false,
			get() {
				let predict = this.field_map[this.criteria.operate_on].available_predicts;
				return this.makeOperatorTraits(predict);
			},
		},
	},

	created: function() {
		const fields = this.definitions.fields;
		this.field_map = {};
		for (const f of fields)
		{
			this.field_map[f.name] = f;
		}
	},
	template: searchCriteriaTemplate,
};

const searchEditor = 
{
	props: ['styles', 'criterias'],
	template: searchEditorTemplate,
	components: {
		search_criteria: searchCriteria,
	},
	methods: {
    updateCriteria: function(c, v)
    {
      c.operate_on = v.current.operate_on;
      c.operand = v.current.operand;
      c.operator = v.current.operator;
    },
		removeCriteria(criteria) {
			let criterias = this.criterias;
			var index = criterias.indexOf(criteria);
			let newCrierias = criterias.filter(x => x !== criteria);
			this.criterias = newCrierias;
		},
    onTriggerSearch: function(ev) {
      this.$emit('search-triggered', this.criterias);
    },
    onNewCriteria: function(ev) {
			let newCriterias = s2j(j2s(this.criterias));
      newCriterias.push({operator: 'contains', operand:'XXX', operate_on: 'title'});
			this.criterias = newCriterias;
    },
	},
};

