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

let headerData = fab_column_settings;

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
		<fabCell 
      :raw_data='access(row, column)' 
      :data_traits='column' 
      @edited='((r, c, v)=>{onEdited(r, c, v)}).bind(undefined, row, column)'
      :current_view='"raw"'/>
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
      if (typeof(accessor) === 'string')
      {
        return row[accessor];
      }
      if (typeof(accessor) === 'function')
      {
        return accessor(row);
      }
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
      if (typeof(accessor) === 'string')
      {
        return row[accessor];
      }
      if (typeof(accessor) === 'function')
      {
        return accessor(row, column);
      }
		},
    onEdited: function(row, column, args) {
      try
      {
        column.update(row, args.current);
      }
      catch(ex)
      {
        console.log(ex);
      }
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
    onSearchUpdated: function (payload) {
      // this.rows = payload;
      this.rows = store.searchResult;
    },
  },
  created: function() {
    messageCenter.subscribe(kApiPrefixChanged.id, this.onApiPrefixChanged.bind(this), this);
    messageCenter.subscribe(kSearchResultUpdated.id, this.onSearchUpdated.bind(this), this);
  },
  beforeDestroy: function () {
    //TODO unsubscribe message
  }
};
