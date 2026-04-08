import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Securitas Contacts", page_icon="🛡️", layout="wide")

# ============================================================
# The full contact directory HTML — pulls live from your Google Sheet
# ============================================================

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; background: #FAF8F7; color: #21201F; }

  .header { background: #21201F; padding: 20px 20px 16px; border-bottom: 3px solid #0040E6; }
  .header-inner { max-width: 720px; margin: 0 auto; }
  .header-tag { margin: 0 0 2px; font-size: 11px; font-weight: 600; color: #0040E6; letter-spacing: 0.08em; text-transform: uppercase; }
  .header h1 { margin: 0 0 4px; font-size: 20px; font-weight: 500; color: #FFF; letter-spacing: -0.02em; }
  .header-meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .header-stats { margin: 0; font-size: 12px; color: #9D9893; }
  .source-badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
  .source-live { background: #0040E6; color: #fff; }
  .source-local { background: #403E3C; color: #9D9893; }
  .btn-refresh { background: none; border: none; color: #9D9893; cursor: pointer; display: flex; align-items: center; gap: 4px; font-size: 10px; font-family: inherit; padding: 2px 4px; }
  .btn-refresh:hover { color: #fff; }
  .header-error { margin: 4px 0 0; font-size: 11px; color: #C34143; }
  .header-time { margin: 4px 0 0; font-size: 10px; color: #736D68; }

  .search-bar { background: #FFF; border-bottom: 1px solid #ECE9E7; padding: 12px 20px; position: sticky; top: 0; z-index: 10; }
  .search-inner { max-width: 720px; margin: 0 auto; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  .search-wrap { position: relative; flex: 1 1 260px; min-width: 180px; }
  .search-wrap svg { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); }
  .search-input { width: 100%; padding: 9px 12px 9px 38px; border: 1px solid #DEDAD7; border-radius: 8px; font-size: 13px; font-family: inherit; color: #21201F; background: #FAF8F7; outline: none; transition: border-color 0.15s; }
  .search-input:focus { border-color: #0040E6; }
  .filter-btns { display: flex; gap: 6px; }
  .filter-btn { padding: 6px 14px; border-radius: 20px; border: 1px solid #DEDAD7; background: #FFF; color: #403E3C; font-size: 12px; font-weight: 500; font-family: inherit; cursor: pointer; transition: all 0.15s; }
  .filter-btn.active { border: 1.5px solid #0040E6; background: #0040E6; color: #FFF; }

  .content { max-width: 720px; margin: 0 auto; padding: 12px 20px 20px; }
  .results-count { margin: 0 0 10px; font-size: 11px; color: #9D9893; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
  .empty { text-align: center; padding: 40px 20px; color: #9D9893; }
  .empty p:first-child { font-size: 15px; }
  .empty p:last-child { font-size: 12px; margin-top: 6px; }

  .market-card { background: #FFF; border: 1px solid #ECE9E7; border-radius: 10px; overflow: hidden; transition: box-shadow 0.15s; margin-bottom: 8px; }
  .market-card:hover { box-shadow: 0 4px 16px rgba(0,64,230,0.07); }
  .card-header { padding: 14px 16px; cursor: pointer; display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
  .card-market-name { font-size: 15px; font-weight: 600; color: #21201F; margin-bottom: 4px; }
  .card-badges { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
  .badge-24 { background: #EBF5EE; color: #007F5E; }
  .badge-limited { background: #FEF3C7; color: #92400E; }
  .card-count { font-size: 11px; color: #9D9893; }
  .chevron { color: #9D9893; margin-top: 2px; transition: transform 0.2s; }
  .chevron.open { transform: rotate(180deg); }

  .card-body { border-top: 1px solid #ECE9E7; padding: 12px 16px 16px; display: none; }
  .card-body.open { display: block; }
  .coverage-detail { font-size: 12px; color: #736D68; margin-bottom: 10px; padding: 6px 10px; background: #FAF8F7; border-radius: 6px; line-height: 1.5; }
  .coverage-detail strong { color: #403E3C; }
  .dispatch-info { font-size: 12px; color: #736D68; margin-bottom: 10px; display: flex; flex-direction: column; gap: 3px; }
  .dispatch-row { display: flex; align-items: flex-start; gap: 6px; }
  .dispatch-label { font-weight: 600; color: #403E3C; min-width: 60px; flex-shrink: 0; }
  .dispatch-row a { color: #0040E6; text-decoration: none; }
  .dispatch-row span { color: #403E3C; word-break: break-all; }
  .note-callout { font-size: 11px; color: #92400E; background: #FEF3C7; padding: 6px 10px; border-radius: 6px; margin-bottom: 10px; line-height: 1.4; display: flex; align-items: flex-start; gap: 6px; }
  .note-callout svg { flex-shrink: 0; margin-top: 1px; }

  .contact-row { padding: 8px 10px; border-radius: 7px; background: #F2F4F7; margin-bottom: 6px; }
  .contact-row:last-child { margin-bottom: 0; }
  .contact-name { font-size: 13px; font-weight: 600; color: #21201F; }
  .contact-role { font-size: 11px; color: #736D68; margin-bottom: 3px; }
  .contact-email-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .contact-email { display: inline-flex; align-items: center; gap: 4px; color: #0040E6; font-size: 12px; text-decoration: none; font-weight: 500; word-break: break-all; }
  .contact-email:hover { text-decoration: underline; }
  .contact-phone { display: inline-flex; align-items: center; gap: 4px; color: #736D68; font-size: 11px; text-decoration: none; margin-top: 2px; }
  .btn-copy { background: none; border: none; cursor: pointer; color: #9D9893; padding: 2px; display: flex; align-items: center; gap: 4px; font-size: 11px; font-family: inherit; }
  .btn-copy:hover { color: #0040E6; }
  .btn-copy.copied { color: #007F5E; }

  .no-coverage { max-width: 720px; margin: 0 auto; padding: 8px 20px 32px; }
  .no-coverage-box { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 10px; padding: 14px 16px; }
  .no-coverage-title { font-size: 13px; font-weight: 600; color: #991B1B; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
  .no-coverage-list { font-size: 12px; color: #991B1B; line-height: 1.6; }
  .no-coverage-note { font-size: 11px; color: #736D68; margin: 8px 0 0; line-height: 1.4; }
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <p class="header-tag">Opendoor × Securitas</p>
    <h1>Patrol Company Contacts</h1>
    <div class="header-meta">
      <p class="header-stats" id="headerStats"></p>
      <span id="sourceBadge"></span>
      <button class="btn-refresh" id="btnRefresh" onclick="fetchSheet()" style="display:none">Refresh</button>
    </div>
    <p class="header-time" id="headerTime"></p>
    <p class="header-error" id="headerError"></p>
  </div>
</div>

<div class="search-bar">
  <div class="search-inner">
    <div class="search-wrap">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9D9893" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input class="search-input" type="text" id="searchInput" placeholder="Search market, contact name, email, or role..." oninput="renderMarkets()">
    </div>
    <div class="filter-btns">
      <button class="filter-btn active" data-filter="All" onclick="setFilter(this)">All</button>
      <button class="filter-btn" data-filter="24/7" onclick="setFilter(this)">24/7</button>
      <button class="filter-btn" data-filter="Limited" onclick="setFilter(this)">Limited</button>
    </div>
  </div>
</div>

<div class="content">
  <p class="results-count" id="resultsCount"></p>
  <div id="marketsList"></div>
</div>

<div class="no-coverage">
  <div class="no-coverage-box">
    <div class="no-coverage-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      No Securitas Coverage Available
    </div>
    <div class="no-coverage-list">Asheville, NC · Birmingham, AL · Chattanooga, TN · Cleveland, OH · Corpus Christi, TX · Greenville, SC · Killeen, TX · Prescott, AZ</div>
    <p class="no-coverage-note">For these markets: Market Ops contact law enforcement directly, then notify T&S. Other teams coordinate via alerts-security in Slack after creating an incident report.</p>
  </div>
</div>

<script>
const GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1h0S-42KCj2dWTGEBgC0Ui7DpTHPSOg4g/gviz/tq?tqx=out:csv&gid=261003292";

const IC = {
  mail:'<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
  phone:'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
  clock:'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  copy:'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
  chevron:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
  alert:'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  sheet:'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>',
};

let markets=[],currentFilter="All",dataSource="local";

const FALLBACK=[
  {market:"Albuquerque, NM",coverage:"24/7",dispatch:"usmd@securitasinc.com",cc:"abq-patrols@opendoor.com",notes:"Include vicky.hawkins@securitasinc.com on patrol routes",contacts:[{name:"Ken Nead",role:"District Manager",email:"ken.nead@securitasinc.com",phone:"505-205-6208"},{name:"Vicky Hawkins",role:"Mobile Services Manager",email:"vicky.hawkins@securitasinc.com",phone:"505-645-2707"}]},
  {market:"Atlanta, GA",coverage:"24/7",dispatch:"usmd@securitasinc.com",cc:"atlpatrols@opendoor.com",notes:"",contacts:[{name:"Pam McGee",role:"District Manager",email:"pam.mcgee@securitasinc.com",phone:"305-753-6039"}]},
  {market:"Phoenix, AZ",coverage:"24/7",dispatch:"usmd@securitasinc.com",cc:"phxpatrols@opendoor.com",notes:"",contacts:[{name:"Ken Nead",role:"District Manager",email:"ken.nead@securitasinc.com",phone:"505-205-6208"},{name:"Vicky Hawkins",role:"Mobile Manager",email:"vicky.hawkins@securitasinc.com",phone:"505-645-2707"}]},
];

function parseCSV(text){
  const lines=text.split("\\n").map(l=>l.trim()).filter(Boolean);
  if(lines.length<2)return null;
  const headers=lines[0].split(",").map(h=>h.trim().replace(/^"|"$/g,"").toLowerCase());
  const idx=n=>headers.indexOf(n);
  const iM=idx("market"),iCov=idx("coverage"),iDisp=idx("dispatch"),iCC=idx("cc"),iN=idx("notes"),iName=idx("contactname"),iRole=idx("role"),iEmail=idx("email"),iPhone=idx("phone");
  if(iM===-1||iEmail===-1)return null;
  function splitRow(row){const f=[];let c="",q=false;for(let i=0;i<row.length;i++){const ch=row[i];if(ch==='"'){q=!q;continue}if(ch===","&&!q){f.push(c.trim());c="";continue}c+=ch}f.push(c.trim());return f}
  const map=new Map();
  for(let i=1;i<lines.length;i++){const c=splitRow(lines[i]);const m=c[iM]||"";if(!m)continue;if(!map.has(m))map.set(m,{market:m,coverage:(c[iCov]||"").trim(),dispatch:(c[iDisp]||"usmd@securitasinc.com").trim(),cc:(c[iCC]||"").trim(),notes:(c[iN]||"").trim(),contacts:[]});const nm=(c[iName]||"").trim(),em=(c[iEmail]||"").trim();if(nm&&em)map.get(m).contacts.push({name:nm,role:(c[iRole]||"").trim(),email:em,phone:(c[iPhone]||"").trim()})}
  return[...map.values()].filter(m=>m.contacts.length>0);
}

function getSheetURLs(url){
  const urls=[url];
  const m2=url.match(/spreadsheets\\/d\\/([\\w-]+)/);const gm=url.match(/gid=(\\d+)/);const gid=gm?gm[1]:"0";
  if(m2){const id=m2[1];urls.push("https://docs.google.com/spreadsheets/d/"+id+"/export?format=csv&gid="+gid);urls.push("https://docs.google.com/spreadsheets/d/"+id+"/gviz/tq?tqx=out:csv&gid="+gid)}
  return[...new Set(urls)];
}

async function fetchSheet(){
  if(!GOOGLE_SHEET_CSV_URL){markets=FALLBACK;dataSource="local";updateHeader();renderMarkets();return}
  document.getElementById("btnRefresh").textContent="Refreshing…";
  document.getElementById("headerError").textContent="";
  const urls=getSheetURLs(GOOGLE_SHEET_CSV_URL);let ok=false;
  for(const url of urls){try{const r=await fetch(url,{redirect:"follow"});if(!r.ok)continue;const t=await r.text();if(!t||t.length<20)continue;const p=parseCSV(t);if(!p||!p.length)continue;markets=p;dataSource="sheet";ok=true;document.getElementById("headerTime").textContent="Last updated: "+new Date().toLocaleTimeString();break}catch(e){continue}}
  if(!ok){document.getElementById("headerError").textContent="Sheet error: Could not fetch — showing fallback data";markets=FALLBACK;dataSource="local"}
  document.getElementById("btnRefresh").textContent="Refresh";
  updateHeader();renderMarkets();
}

function updateHeader(){
  const t=markets.reduce((n,m)=>n+m.contacts.length,0);
  document.getElementById("headerStats").textContent=markets.length+" markets · "+t+" contacts";
  const b=document.getElementById("sourceBadge");
  if(dataSource==="sheet"){b.className="source-badge source-live";b.innerHTML=IC.sheet+" Live from Google Sheet";document.getElementById("btnRefresh").style.display="flex"}
  else{b.className="source-badge source-local";b.textContent="Built-in data";document.getElementById("btnRefresh").style.display="flex"}
}

function setFilter(btn){document.querySelectorAll(".filter-btn").forEach(b=>b.classList.remove("active"));btn.classList.add("active");currentFilter=btn.dataset.filter;renderMarkets()}
function toggleCard(id){document.getElementById("body-"+id).classList.toggle("open");document.getElementById("chev-"+id).classList.toggle("open")}
function copyEmail(btn,email){navigator.clipboard.writeText(email);btn.classList.add("copied");btn.innerHTML=IC.copy+" Copied!";setTimeout(()=>{btn.classList.remove("copied");btn.innerHTML=IC.copy},1500)}
function esc(s){const d=document.createElement("div");d.textContent=s;return d.innerHTML}

function renderMarkets(){
  const q=(document.getElementById("searchInput").value||"").toLowerCase();
  const filtered=markets.filter(m=>{
    const mc=currentFilter==="All"||(currentFilter==="24/7"&&m.coverage==="24/7")||(currentFilter==="Limited"&&m.coverage!=="24/7");
    const mq=!q||m.market.toLowerCase().includes(q)||m.cc.toLowerCase().includes(q)||(m.notes||"").toLowerCase().includes(q)||m.contacts.some(c=>c.name.toLowerCase().includes(q)||c.email.toLowerCase().includes(q)||c.role.toLowerCase().includes(q));
    return mc&&mq});
  document.getElementById("resultsCount").textContent=filtered.length+" market"+(filtered.length!==1?"s":"")+(q?' matching "'+q+'"':"");
  const el=document.getElementById("marketsList");
  if(!filtered.length){el.innerHTML='<div class="empty"><p>No markets match your search.</p><p>Try a different city, state, or contact name.</p></div>';return}
  let h="";
  filtered.forEach((m,i)=>{
    const is24=m.coverage==="24/7";
    h+='<div class="market-card"><div class="card-header" onclick="toggleCard('+i+')"><div><div class="card-market-name">'+esc(m.market)+'</div><div class="card-badges"><span class="badge '+(is24?"badge-24":"badge-limited")+'">'+IC.clock+" "+(is24?"24/7":"Limited")+'</span><span class="card-count">'+m.contacts.length+" contact"+(m.contacts.length>1?"s":"")+'</span></div></div><div class="chevron" id="chev-'+i+'">'+IC.chevron+"</div></div>";
    h+='<div class="card-body" id="body-'+i+'">';
    if(!is24)h+='<div class="coverage-detail"><strong>Coverage:</strong> '+esc(m.coverage)+"</div>";
    h+='<div class="dispatch-info"><div class="dispatch-row"><span class="dispatch-label">Dispatch:</span><a href="mailto:'+esc(m.dispatch)+'">'+esc(m.dispatch)+'</a></div><div class="dispatch-row"><span class="dispatch-label">CC:</span><span>'+esc(m.cc)+"</span></div></div>";
    if(m.notes)h+='<div class="note-callout">'+IC.alert+"<span>"+esc(m.notes)+"</span></div>";
    m.contacts.forEach(c=>{
      h+='<div class="contact-row"><div class="contact-name">'+esc(c.name)+'</div><div class="contact-role">'+esc(c.role)+'</div><div class="contact-email-row"><a class="contact-email" href="mailto:'+esc(c.email)+'">'+IC.mail+" "+esc(c.email)+'</a><button class="btn-copy" onclick="copyEmail(this,\\''+esc(c.email).replace(/'/g,"\\\\'")+'\\')">' +IC.copy+"</button></div>";
      if(c.phone)h+='<a class="contact-phone" href="tel:'+esc(c.phone)+'">'+IC.phone+" "+esc(c.phone)+"</a>";
      h+="</div>"});
    h+="</div></div>"});
  el.innerHTML=h;
}
fetchSheet();
</script>
</body>
</html>
"""

# ============================================================
# Render in Streamlit
# ============================================================

components.html(HTML_PAGE, height=900, scrolling=True)
