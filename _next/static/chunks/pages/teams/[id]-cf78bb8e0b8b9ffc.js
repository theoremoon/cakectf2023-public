(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[661],{7609:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/teams/[id]",function(){return n(3873)}])},3528:function(e,t,n){"use strict";n.d(t,{Z:function(){return a}});var s=n(5893),r=n(1776),i=n.n(r),a=()=>(0,s.jsx)("div",{style:{height:"100%",justifyContent:"center",alignItems:"center"},children:(0,s.jsx)("div",{style:{maxWidth:"960px",margin:"0 auto"},children:(0,s.jsx)("div",{className:i()["lds-dual-ring"]})})})},9476:function(e,t,n){"use strict";var s=n(4011),r=n(6061),i=n(9734);t.Z=e=>r.s?(0,s.s)(e):(0,i.ZP)("/scoreboard")},4055:function(e,t,n){"use strict";n.d(t,{v:function(){return c}});var s=n(7484),r=n.n(s),i=n(285),a=n.n(i);r().extend(a());let c=e=>r()(1e3*e).format("YYYY-MM-DD HH:mm:ss Z")},3873:function(e,t,n){"use strict";n.r(t),n.d(t,{__N_SSG:function(){return p},default:function(){return g}});var s=n(5893),r=n(3528),i=n(9476),a=n(4011),c=n(6061),o=n(9734),l=(e,t)=>c.s?(0,a.s)(t):(0,o.ZP)("/team/".concat(e)),d=n(5472),u=n.n(d),m=n(4055),h=n(5149),x=n(9128),f=n(4386),_=n.n(f),j=e=>{let{team:t,scorefeed:n,series:r}=e,i=u()(Object.entries(n.taskStats).map(e=>{let[t,n]=e;return{name:t,...n}}),["time"],["desc"]);return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsxs)("h1",{children:[t.country?(0,s.jsx)(h.Z,{country:t.country}):"",t.teamname,(0,s.jsxs)("span",{className:_()["team-info"],children:["Rank ",n.pos," / ",n.score," points"]})]}),(0,s.jsx)(x.Z,{chartTeams:[t.teamname],chartSeries:r}),n&&(0,s.jsxs)("table",{className:_()["score-table"],children:[(0,s.jsx)("thead",{children:(0,s.jsxs)("tr",{children:[(0,s.jsx)("th",{children:"Task"}),(0,s.jsx)("th",{children:"Score"}),(0,s.jsx)("th",{children:"Solved At"})]})}),(0,s.jsx)("tbody",{children:i.map(e=>(0,s.jsxs)("tr",{children:[(0,s.jsx)("td",{children:e.name}),(0,s.jsx)("td",{children:e.points}),(0,s.jsx)("td",{children:(0,m.v)(e.time)})]},e.name))})]})]})},p=!0,g=e=>{let{team:t,scoreboard:n,series:a}=e,{data:c}=l(t.team_id.toString(),t),{data:o}=(0,i.Z)(n);if(!c||!o)return(0,s.jsx)(r.Z,{});let d=o.filter(e=>e.team_id===c.team_id)[0];return j({team:c,scorefeed:d,series:a})}},9128:function(e,t,n){"use strict";var s=n(5893),r=n(3385);t.Z=e=>{let{chartTeams:t,chartSeries:n}=e,i=n.map((e,n)=>({name:t[n],type:"line",showSymbol:!1,data:e.map(e=>[1e3*e.time,e.score])})),a=t.map(e=>({name:e}));return(0,s.jsx)(r.Z,{option:{tooltip:{trigger:"axis",axisPointer:{type:"cross",animation:"false"}},legend:{data:a},xAxis:{type:"time"},yAxis:{type:"value"},series:i},notMerge:!0})}},5149:function(e,t,n){"use strict";var s=n(5893),r=n(3023);t.Z=e=>{let{country:t}=e,n=r.P5.countries({alpha2:t})[0];return n?(0,s.jsx)("span",{title:n.name,children:n.emoji}):(0,s.jsx)(s.Fragment,{})}},1776:function(e){e.exports={"lds-dual-ring":"loading_lds-dual-ring__qQmZi"}},4386:function(e){e.exports={"team-info":"team_team-info__EQVRJ","score-table":"team_score-table__V7Vf9"}}},function(e){e.O(0,[472,23,75,774,888,179],function(){return e(e.s=7609)}),_N_E=e.O()}]);