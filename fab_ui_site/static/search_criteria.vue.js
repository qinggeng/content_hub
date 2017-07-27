"use strict";
// import data_editor.vue

const searchEditorStyles = {
	container: extend(solid_border, {
		'margin': '0 0 0 0',
		'display': 'flex',
		'min-height': '40px',
		'flex-direction': 'row',
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
};

const criteriaDefines = {
	predicts: predicts,
	fields: [
		{
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
				edit_type: 'textEdit',
			},
			applyValue: function(val) {
				return val;
			}
		},
		{
			name: 'priority', 
			display: '优先级', 
			available_predicts: [
				predicts.higher_than,
				// predicts.lowerThan,
				// predicts.equals,
				// predicts.higherOrEqual,
				// predicts.lowerOrEqual,
				// predicts.notContains,
				// predicts.startsWith,
				// predicts.endsWith,
				// predicts.regex,
			],
			data_traits: {
				edit_type: 'choice',
				choices: [
					{val: 100, display: 'Unbreak Now!'},
					{val: 90, display: 'Needs triage'},
					{val: 80, display: 'High'},
					{val: 70, display: 'Normal'},
					{val: 60, display: 'Low'},
					{val: 50, display: 'Wishlist'},
				],
			},
			applyValue: function(val) {
				var filtered = this.data_traits.choices.filter(x=> x.val === val);
				if (filtered.length == 0)
				{
					return this.data_traits.choices[0].val;
				}
				return val;
			}
		},
	],
};

const fieldTraits = {
	edit_type: 'choice',
	choices: criteriaDefines.fields.map(x => {return {val: x.name, display: x.display};}),
};

const searchCriteriaTemplate = `
<div :style='styles.frame'>
	<data_editor 
		:raw_data='criteria.operate_on' 
		:data_traits='fieldTraits' 
		:current_view='"raw"'
	 	@value-changed='onFieldChosen'/>
	<data_editor 
		:raw_data='criteria.operator' 
		:data_traits='operator_traits' 
		:current_view='"raw"'/>
	<data_editor 
		:raw_data='criteria.operand' 
		:data_traits='current_field.data_traits' 
		:current_view='"raw"' @value-changed='onCriteriaChanged'/>
	<!-- <span :style='styles.sector'>{{criteria.operand}}</span> -->
	<div :style='styles.xbtn' @click='requestRemoveCriteria'>
	Ⅹ
	</div>
</div>
`;

const searchEditorTemplate = `
<div :style='styles.container'>
	<search_criteria 
		v-for='criteria in criterias' 
		:styles='styles.criteria' :criteria='criteria' 
		@request-remove-criteria='removeCriteria'/>
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
				choices: val.map(x=>{return {val: x.key, display: x.display};}),
			};
		},

		onFieldChosen: function(val) {
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
			criteria.operand = fieldDefine.applyValue(criteria.operand);
		},

		onCriteriaChanged: function (val){
			const criteria = this.criteria;
			//TODO send change message
			criteria.operand = val.current;
		},

		requestRemoveCriteria: function (ev) {
			this.$emit('request-remove-criteria', this.criteria);
		},

		onPredictChoosen: function(val) {
			this.criteria.operator = val.current;
		},
	},

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
		removeCriteria(criteria) {
			let criterias = this.criterias;
			var index = criterias.indexOf(criteria);
			let newCrierias = criterias.filter(x => x !== criteria);
			this.criterias = newCrierias;
		},
	},
};

