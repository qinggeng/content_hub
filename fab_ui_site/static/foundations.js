var extend = (base, deriving) =>
{
  var derived = JSON.parse(JSON.stringify(base));
  for (var key in deriving)
  {
    derived[key] = deriving[key];
  }
  return derived;
}

const j2s = JSON.stringify;
const s2j = JSON.parse;
/*
*/
//function strptime(str, fmt)
var strptime = (str, fmt) =>
{
  const placeHolders = [
    [(x, y)=>x.setYear(y), '%Y', '(\\d{2,4})'],
    [(x, y)=>x.setMonth(y - 1), '%m', '(\\d{1,2})'],
    [(x, y)=>x.setDate(y), '%d', '(\\d{1,2})'],
    [(x, y)=>x.setHours(y), '%H', '(\\d{1,2})'],
    [(x, y)=>x.setMinutes(y), '%M', '(\\d{1,2})'],
    [(x, y)=>x.setSeconds(y), '%S', '(\\d{1,2})'],
    [(x, y)=>x.setTime(y), '%s', '(\\d+)'],
  ];
  const ph = placeHolders;
  const phIndex = ph.map(x => [x[0], fmt.search(x[1]), x[2], x[1]])
            .filter(x => x[1] != -1)
            .sort((x, y)=> x[1] >y[1]);
  const patternStr = phIndex.reduce((x, y)=> x.replace(y[3], y[2]), fmt);
  const pattern = new RegExp(patternStr);
  const m = pattern.exec(str);
  var d = new Date(0);
  for (var p in phIndex)
  {
    var setter = phIndex[p][0];
    var groupIndex = Number(p) + 1;
    setter(d, Number(m[groupIndex]));
  }
  return d;
}

let strftime = (dt, fmt)=>
{
  const placeHolders = [
    [(x, y)=>y.replace('%Y', x.getFullYear()), '%Y'],
    [(x, y)=>y.replace('%m', String(x.getMonth() + 1)), '%m'],
    [(x, y)=>y.replace('%d', String(x.getDate())), '%d'],
    [(x, y)=>y.replace('%H', String(x.getHours())), '%H'],
    [(x, y)=>y.replace('%M', String(x.getMinutes())), '%M'],
    [(x, y)=>y.replace('%S', String(x.getSeconds())), '%S'],
    [(x, y)=>y.replace('%s', String(x.getTime())), '%s'],
  ];
  const ph = placeHolders;
  for (var f of placeHolders)
  {
    let formatter = f[0];
    fmt = formatter(dt, fmt);
  }
  return fmt;
}

var solid_border = {
  'border-style': 'solid',
  'border-width': '1px',
};
