"use strict"
var cell_common_style = extend(solid_border, {
	'padding-left': '15px',
	'padding-right': '15px',
	'vertical-align': 'center',
});

var header_style = extend(cell_common_style, {
	'text-align': 'center',
});

var row_style = extend(cell_common_style, {
});

var table_styles = {
	header: header_style,
	row: row_style,
	table: {'border-collapse': 'collapse'},
	typed_cells: {//不同类型的单元格有不同的样式，优先级最高
	},
	typed_rows: {//不同类型的行有不同的样式，优先级高于row
	},
	typed_columns: {//不同类型的列有不同的样式，优先级高于
	},
};

var authorEnums = [
	{val: '1', display: 'author1'},
	{val: '2', display: 'author2'},
	{val: '3', display: 'author3'},
]

var projects = [
	{val: 'P1', display: 'project1'},
	{val: 'P2', display: 'project2'},
	{val: 'P3', display: 'project3'},
]

var headerData = [
	{value: '编号', accessor: 'id', editable: 'false'},
	{value: '标题', accessor: 'title', editable: 'true', edit_type: 'textEdit', editor_pattern: 'inplace'},
	{value: '作者', accessor: 'author', editable: 'true', edit_type: 'choice', editor_pattern: 'inplace', choices: authorEnums },
	{value: '优先级', accessor: 'priority', editable: 'true', edit_type: 'choice', editor_pattern: 'inplace'},
	{value: '严重程度', accessor: 'severity', editable: 'true', edit_type: 'choice', editor_pattern: 'inplace'},
	{value: '项目', accessor: 'project', editable: 'true', edit_type: 'multiple_choise', editor_pattern: 'inplace', choices: projects},
	{value: '计划截止时间', accessor: 'deadline', editable: 'true', edit_type: 'datetime', editor_pattern: 'inplace', choices: projects},
	{value: '描述', accessor: 'description', editable: 'true', edit_type: 'textEdit', editor_pattern: 'popup'},
];

var fabtableTemplate = `
<table :style='table_styles.table'>
	<tbody>
		<fabHeaderRow v-bind:headers='headers' :header_style='table_styles.header'/>
		<fabRow v-for='row in rows' :row='row' :columns='headers' :row_style='table_styles.row'/>
	</tbody>
</table>
`;

var fabHeaderRowTemplate = `
<TR>
<TH v-for='header in headers' style='border-style: solid; border-width: 1px'> {{header.value}}</TH>
</TR>
`;

var fabRowTemplate = `
<TR>
	<TD v-for='column in columns' :style='row_style'>
		<fabCell :raw_data='access(row, column)' :data_traits='column' :current_view='"raw"'/>
	</TD>
</TR>
`;

const fabCell = dataEditor;

const fabHeaderRow = {
	props: ['headers', 'header_style'],
	template: fabHeaderRowTemplate,
};

const fabRow = {
	props: ['columns', 'row', 'row_style'],
	template: fabRowTemplate,
	components: {
		fabCell: fabCell,
	},
	filters: 
	{
		access: function(row, column)
		{
			var accessor = column.accessor;
			return row[accessor];
		},
	},
	methods: {
		click: function(ev)
		{
			console.log('clicked');
		},
		access: function(row, column)
		{
			var accessor = column.accessor;
			var val = row[accessor];
			return val;
		},
	},
};

const fabtable = {
	props: ['headers', 'rows', 'header_style', 'table_styles'],
	template: fabtableTemplate,
	components: {
		fabHeaderRow: fabHeaderRow,
		fabRow: fabRow,
	},
  methods: {
    onApiPrefixChanged: function (payload) {
      console.log(j2s(payload));
    },
  },
  created: function() {
    messageCenter.subscribe(kApiPrefixChanged.id, this.onApiPrefixChanged.bind(this), this);
  },
  beforeDestroy: function () {
    //TODO unsubscribe message
  }
};
