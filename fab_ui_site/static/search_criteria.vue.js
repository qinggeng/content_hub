"use strict";

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
			'display': '包含',
		}; 
	},
	get higherThan()
	{
		return {
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
			avalablePredicts: [
				predicts.contains,
				// predicts.notContains,
				// predicts.startsWith,
				// predicts.endsWith,
				// predicts.regex,
			],
			criteria_edit_type: 'textEdit',
		},
		{
			name: 'priority', 
			display: '优先级', 
			avalablePredicts: [
				predicts.higherThan,
				// predicts.lowerThan,
				// predicts.equals,
				// predicts.higherOrEqual,
				// predicts.lowerOrEqual,
				// predicts.notContains,
				// predicts.startsWith,
				// predicts.endsWith,
				// predicts.regex,
			],
			criteria_edit_type: 'choice',
		},
	],
};

const searchCriteriaTemplate = `
<div :style='styles.frame'>
	<span :style='styles.sector'>{{fieldDisplay(criteria.operate_on)}}</span>
	<span :style='styles.sector'>{{operatorDisplay(criteria.operator)}}</span>
	<span :style='styles.sector'>{{criteria.operand}}</span>
	<div :style='styles.xbtn'>
	Ⅹ
	</div>
</div>
`;

const searchEditorTemplate = `
<div :style='styles.container'>
	<search_criteria v-for='criteria in criterias' :styles='styles.criteria' :criteria='criteria'/>
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
	filters: {
	},
	methods: {
		fieldDisplay: function (val) 
		{
			try
			{
				return this.fieldMap[val].display;
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
	},
	created: function() {
		const fields = this.definitions.fields;
		this.fieldMap = {};
		for (const f of fields)
		{
			this.fieldMap[f.name] = f;
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
};

