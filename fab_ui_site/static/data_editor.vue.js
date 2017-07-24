"use strict"
const dataEditor = (function(){
	var typedAccessors = {
		choice: (val, traits)=> {
			var choices = traits.choices;
			for (var c of choices)
			{
				if (c.val == val)
				{
					return c.display;
				}
			}
			return val;
		},
		textEdit: (val, traits)=>{return val},
		multiple_choise: (val, traits)=> {
			var choices = traits.choices.reduce((x, y)=>{x[y.val]=y.display; return x}, {});
			return val.map(x=> choices[x]).join(', ');
		},
		datetime: (val, traits) =>{
			var d = new Date(val);
			const padding = (s, l, c)=>
			{
			  var paddingLength = Math.max(0, l - s.length);
			  for (var i = 0; i < paddingLength; i++)
			  {
				s = c + s;
			  }
			  return s;
			};
			var str = d.toUTCString();
			var year = String(d.getFullYear());
			var mon = String(d.getMonth() + 1);
			var day = String(d.getDate());
			var h = String(d.getHours());
			var mm = String(d.getMinutes());
			var date = year + '-' + padding(mon, 2, '0') + '-' + padding(day, 2, '0');
			var time = padding(h, 2, '0') + ':' + padding(mm, 2, '0');
			return date + ' ' + time;
		},
	};

	const dataEditor = {
		props: ['raw_data', 'current_view', 'data_traits'],
		template: `<component :is='current_view' :display_data='formatVal(raw_data, data_traits)' @request-edit='onRequestEdit' @edited='onEdited' :raw_data='raw_data' :data_traits='data_traits'/>`,
		methods: {
			formatVal(val, traits)
			{
				try
				{
					return typedAccessors[traits.edit_type](val, traits);
				}
				catch(ex)
				{
					//console.log(traits.edit_type);
					//console.log(ex);
				}
				return val;
			},
			onRequestEdit: function(ev, args) {
				this.current_view = this.data_traits.edit_type;
			},
			onEdited: function(args) {
				var val = args;
				const oldVal = this.raw_data;
				this.$emit('value-changed', {last: oldVal, current: val});
				this.raw_data = val;
				this.display_data = this.formatVal(val, this.data_traits);
				this.current_view = 'raw';
			},
		},
		components: {
			raw: {
				props: ['display_data'],
				template: `<span @click='clicked'>{{display_data}}</span>`,
				methods: {
					clicked: function(ev) {
						this.$emit('request-edit');
					}
				},
			},
			highlighted: {
				props: ['display_data'],
				template: `<span style='color: #FF0000'>{{display_data}}</span>`,
			},
			textEdit: {
				props: ['display_data'],
				mounted: function(el) {
					this.$el.focus();
					this.$el.select();
				},
				methods: {
					onBlur: function(ev) {
						this.$emit('edited', this.$el.value);
					},
				},
				template: `<input type = "text" :value='display_data' @blur='onBlur'/>`,
			},
			choice: {
				props: ['display_data', 'raw_data', 'data_traits'],
				mounted: function(el) {
					this.$el.focus();
				},
				methods: {
					onBlur: function(ev) {
						this.$emit('edited', this.$el.value);
					},
				},
				template: `
					<select @blur='onBlur' :value='raw_data'>
					<option v-for = 'opt of data_traits.choices' :value='opt.val'>{{opt.display}}</oitpion>
					</select>`,
			},
			multiple_choise: {
				props: ['display_data', 'raw_data', 'data_traits'],
				mounted: function(el) {
					this.$el.focus();
				},
				methods: {
					onBlur: function(ev) {
						var opts = this.$el.options;
						var value = [];
						for (var opt of opts)
						{
							if (opt.selected)
							{
								value.push(opt.value);
							}
						}
						this.$emit('edited', value);
					},
				},
				template: `
					<select @blur='onBlur' multiple='multiple'>
					<option v-for = 'opt of data_traits.choices' :value='opt.val' :selected='raw_data.indexOf(opt.val) != -1'>{{opt.display}}</oitpion>
					</select>`,
			},
			datetime: {
				props: ['display_data'],
				mounted: function(el) {
					this.$el.focus();
					this.$el.select();
				},
				methods: {
					onBlur: function(ev) {
						try
						{
							var dt = strptime(this.$el.value, '%Y-%m-%d %H').toUTCString();
							this.$emit('edited', dt);
						}
						catch(ex)
						{
							this.$el.style.borderStyle='solid';
							this.$el.style.borderColor='#FF0000';
							this.$el.style.backgroundColor='#FFE0E0';
							this.$el.focus();
						}
					},
				},
				template: `<input type = "text" :value='display_data' @blur='onBlur'/>`,
			},
		},
	};
	return dataEditor;
})();
