const pptxgen = require("pptxgenjs");
const A = "/sessions/inspiring-eloquent-brown/mnt/outputs/slides_build/assets/";
const p = new pptxgen();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";

const INDIGO="1E3A8A", BLUE="2563EB", VIOLET="7C3AED", INK="0F172A",
      SLATE="334155", MUTED="64748B", MINT="93C5FD", LIGHT="BFDBFE",
      WHITE="FFFFFF", CARD="F1F5FF", CHIP="EEF3FF";
const F="Arial";
const bgT={path:A+"bg_title.png"}, bgC={path:A+"bg_content.png"};

function kicker(s,t,x,y,color){ s.addText(t.toUpperCase(),{x,y,w:8,h:0.3,fontFace:F,fontSize:13,bold:true,color,charSpacing:3,align:"left"}); }
function title(s,t,x,y,w,color,size){ s.addText(t,{x,y,w,h:1.1,fontFace:F,fontSize:size||34,bold:true,color:color||INK,align:"left",valign:"top",lineSpacingMultiple:1.0}); }
function bullets(s,items,x,y,w,h,color){
  s.addText(items.map((t,i)=>({text:t,options:{bullet:{code:"2022",indent:16},breakLine:true,paraSpaceAfter:10}})),
    {x,y,w,h,fontFace:F,fontSize:16,color:color||SLATE,align:"left",valign:"top",lineSpacingMultiple:1.05});
}
function chip(s,x,y,w,t){
  s.addShape(p.ShapeType.roundRect,{x,y,w,h:0.5,fill:{color:CHIP},line:{color:BLUE,width:0.75},rectRadius:0.25});
  s.addText(t,{x,y,w,h:0.5,fontFace:F,fontSize:13,bold:true,color:INDIGO,align:"center",valign:"middle",margin:0});
}

// ---------- 1 TITLE ----------
let s=p.addSlide(); s.background=bgT;
kicker(s,"Chapter 2  ·  Search Semantically",0.7,1.1,MINT);
title(s,"Keyword /\nLexical Search",0.7,1.6,8,WHITE,54);
s.addText("Match the words — fast. The workhorse behind decades of search.",{x:0.72,y:3.9,w:7.4,h:0.9,fontFace:F,fontSize:22,color:LIGHT,align:"left"});
s.addText("Dr. Mahdi Habibi",{x:0.72,y:6.7,w:6,h:0.4,fontFace:F,fontSize:13,color:MINT,align:"left"});
s.addNotes("Chapter 2 introduces keyword (lexical) search: matching the literal words of a query against documents, fast. It's still everywhere and a strong baseline. We'll build the inverted index, TF-IDF, and BM25.");

// ---------- 2 THE TASK ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Where we are",0.7,0.55,BLUE);
title(s,"Connect a query to the right documents — in milliseconds",0.7,0.95,12,INK,32);
bullets(s,[
 "A user gives a query; we must return the documents that match.",
 "It has to be fast — potentially over millions of documents.",
 "Keyword search scores documents by their shared words.",
 "Two ideas make it work: an index (speed) + a scoring function (quality)."
],0.7,2.35,7.2,3.6);
s.addImage({path:A+"diagram_pipeline.png",x:0.6,y:5.55,w:9.6,h:1.5});
s.addNotes("Framing: retrieval must be fast and relevant. Speed comes from the inverted index; relevance from BM25.");

// ---------- 3 INTUITION ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Intuition",0.7,0.55,BLUE);
title(s,"Start simple: count the shared words",0.7,0.95,12,INK,32);
s.addText([{text:"Query:  ",options:{bold:true,color:INK}},{text:"what color is the grass",options:{italic:true,color:BLUE}}],
  {x:0.7,y:2.0,w:11,h:0.4,fontFace:F,fontSize:17});
const docs=[["the grass is green",3,BLUE],["the sky is blue",2,SLATE],["the capital of canada is ottawa",2,SLATE],["a whale is a mammal",1,SLATE]];
let y=2.55;
docs.forEach(([t,c,col],i)=>{
  s.addShape(p.ShapeType.roundRect,{x:0.7,y,w:9.4,h:0.72,fill:{color:i===0?"E7EEFF":CARD},line:{type:"none"},rectRadius:0.1});
  s.addText([{text:`D${i}  `,options:{bold:true,color:MUTED}},{text:t,options:{color:INK}}],
    {x:1.0,y,w:8,h:0.72,fontFace:F,fontSize:16,valign:"middle",margin:0});
  s.addShape(p.ShapeType.ellipse,{x:11.15,y:y+0.11,w:0.5,h:0.5,fill:{color:col}});
  s.addText(String(c),{x:11.15,y:y+0.11,w:0.5,h:0.5,fontFace:F,fontSize:18,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
  y+=0.85;
});
s.addText("D0 wins — it repeats the query's words. But common words like “the” and “is” dominate the count. We need to weight them.",
  {x:0.7,y:6.4,w:11.3,h:0.7,fontFace:F,fontSize:15,italic:true,color:MUTED});
s.addNotes("Shared-word counting is the seed of keyword search, but stopwords pollute it — motivating IDF.");

// ---------- 4 TOKENIZATION ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Step 1",0.7,0.55,BLUE);
title(s,"Tokenization: turn text into comparable tokens",0.7,0.95,12,INK,32);
const steps=[["1","Lowercase","“Grass” = “grass”"],["2","Split","on non-letters"],["3","Stop-words","drop the, is, of"],["4","Stem","running → run"]];
const cx=[2.1,5.0,7.9,10.8];
steps.forEach(([n,hd,sub],i)=>{
  const x=cx[i];
  s.addShape(p.ShapeType.ellipse,{x:x-0.6,y:2.5,w:1.2,h:1.2,fill:{color:i%2?VIOLET:BLUE}});
  s.addText(n,{x:x-0.6,y:2.5,w:1.2,h:1.2,fontFace:F,fontSize:40,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
  s.addText(hd,{x:x-1.35,y:3.95,w:2.7,h:0.4,fontFace:F,fontSize:18,bold:true,color:INK,align:"center"});
  s.addText(sub,{x:x-1.35,y:4.35,w:2.7,h:0.5,fontFace:F,fontSize:13,color:MUTED,align:"center"});
  if(i<3) s.addShape(p.ShapeType.line,{x:x+0.65,y:3.1,w:1.6,h:0,line:{color:SLATE,width:2.5,endArrowType:"triangle"}});
});
s.addText("Tokenize the query the SAME way as the documents — or matches silently vanish.",
  {x:0.7,y:5.6,w:11.3,h:0.6,fontFace:F,fontSize:16,italic:true,color:SLATE});
s.addNotes("Normalization must be identical for query and docs. Stop-words and stemming are optional but common.");

// ---------- 5 INVERTED INDEX ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Step 2",0.7,0.55,BLUE);
title(s,"The inverted index: how search is instant",0.7,0.95,6.4,INK,32);
bullets(s,[
 "Map every term → the documents that contain it.",
 "Built once, ahead of time (at indexing).",
 "A query becomes a single lookup, not a full scan.",
 "This is why results come back in milliseconds."
],0.7,2.3,5.6,3.6);
s.addImage({path:A+"diagram_index.png",x:6.7,y:1.9,w:6.0,h:4.1});
s.addNotes("term->postings inverts the usual doc->words direction, enabling fast lookups.");

// ---------- 6 TF-IDF ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Step 3",0.7,0.55,BLUE);
title(s,"TF-IDF: weight words by how informative they are",0.7,0.95,12,INK,32);
function card(x,badge,hd,body,col){
  s.addShape(p.ShapeType.roundRect,{x,y:2.3,w:5.5,h:2.3,fill:{color:CARD},line:{type:"none"},rectRadius:0.12});
  s.addShape(p.ShapeType.ellipse,{x:x+0.35,y:2.65,w:1.0,h:1.0,fill:{color:col}});
  s.addText(badge,{x:x+0.35,y:2.65,w:1.0,h:1.0,fontFace:F,fontSize:20,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
  s.addText(hd,{x:x+1.55,y:2.7,w:3.7,h:0.5,fontFace:F,fontSize:20,bold:true,color:INK,valign:"middle"});
  s.addText(body,{x:x+0.4,y:3.75,w:4.8,h:0.7,fontFace:F,fontSize:15,color:SLATE});
}
card(0.7,"TF","Term Frequency","Frequent in a document → probably matters to it.",BLUE);
card(7.1,"IDF","Inverse Doc Frequency","Rare across the corpus → more distinctive & useful.",VIOLET);
s.addText("TF-IDF = TF × IDF  —  frequent here AND rare overall  =  a high score.",
  {x:0.7,y:5.0,w:8,h:0.5,fontFace:F,fontSize:17,bold:true,color:INDIGO});
s.addImage({path:A+"formula_idf.png",x:8.7,y:4.85,w:3.7,h:0.9});
s.addNotes("TF rewards local frequency; IDF rewards global rarity; the product ranks for the right reason.");

// ---------- 7 WORKED EXAMPLE ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Worked example",0.7,0.55,BLUE);
title(s,"Why “is” scores nothing and “grass” wins",0.7,0.95,12,INK,32);
const rows=[
 [{text:"term",options:{bold:true,color:WHITE,fill:{color:INDIGO}}},{text:"df (docs with it)",options:{bold:true,color:WHITE,fill:{color:INDIGO}}},{text:"IDF = ln(N / df)",options:{bold:true,color:WHITE,fill:{color:INDIGO}}}],
 ["is","5 of 5","0.00"],["the","3 of 5","0.51"],["grass","1 of 5","1.61"]];
s.addTable(rows,{x:0.7,y:2.35,w:7.2,colW:[2.2,2.5,2.5],rowH:0.6,fontFace:F,fontSize:16,color:INK,align:"center",valign:"middle",border:{type:"solid",color:"D6DEF5",pt:1}});
s.addShape(p.ShapeType.roundRect,{x:8.4,y:2.35,w:4.2,h:2.4,fill:{color:"E7EEFF"},line:{type:"none"},rectRadius:0.12});
s.addText([{text:"score(D0) ≈ 2.12\n",options:{bold:true,fontSize:24,color:INDIGO}},{text:"driven almost entirely by “grass”.\n“is” is in every doc → IDF 0 → adds nothing.",options:{fontSize:15,color:SLATE}}],
  {x:8.6,y:2.55,w:3.8,h:2.0,fontFace:F,align:"left",valign:"top"});
s.addText("N = 5 documents.  IDF = ln(N / df): common terms → ~0, rare terms → large.",
  {x:0.7,y:5.6,w:11.5,h:0.5,fontFace:F,fontSize:15,italic:true,color:MUTED});
s.addNotes("The numbers are asserted in the Chapter 2 notebook. 'is' contributes 0 because ln(5/5)=0.");

// ---------- 8 BM25 (dark) ----------
s=p.addSlide(); s.background=bgT;
kicker(s,"Step 4",0.7,0.7,MINT);
title(s,"BM25: the workhorse ranking function",0.7,1.1,12,WHITE,34);
s.addShape(p.ShapeType.roundRect,{x:0.9,y:2.5,w:11.5,h:1.9,fill:{color:WHITE},line:{type:"none"},rectRadius:0.14});
s.addImage({path:A+"formula_bm25.png",x:1.3,y:2.75,w:10.7,h:1.4});
chip(s,0.9,4.8,3.4,"k1  —  term saturation");
chip(s,4.6,4.8,3.9,"b  —  length normalization");
s.addText("Diminishing returns for repeated terms, and fairness for long documents. The default first-stage ranker for decades — fast, robust, no training.",
  {x:0.9,y:5.7,w:11.4,h:0.9,fontFace:F,fontSize:16,color:LIGHT});
s.addNotes("BM25 fixes TF-IDF's two weaknesses: saturation (k1) and length normalization (b).");

// ---------- 9 PITFALLS ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Pitfalls & gotchas",0.7,0.55,BLUE);
title(s,"Where keyword search goes wrong",0.7,0.95,12,INK,32);
const pit=[["Mismatched tokenization","Query and docs must be normalized the same way, or matches disappear."],
 ["Over-aggressive stop-words","Dropping “not” or “no” can flip meaning."],
 ["Raw counts, no length norm","Long documents dominate. Use BM25, not plain TF."],
 ["Expecting synonyms","Keyword search can't match meaning — that needs embeddings (Ch 3–6)."]];
let yy=2.35;
pit.forEach(([hd,ds])=>{
  s.addShape(p.ShapeType.ellipse,{x:0.7,y:yy,w:0.6,h:0.6,fill:{color:VIOLET}});
  s.addText("!",{x:0.7,y:yy,w:0.6,h:0.6,fontFace:F,fontSize:24,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
  s.addText([{text:hd+"  ",options:{bold:true,color:INK}},{text:"—  "+ds,options:{color:SLATE}}],
    {x:1.5,y:yy-0.05,w:10.8,h:0.7,fontFace:F,fontSize:16,valign:"middle"});
  yy+=1.02;
});
s.addNotes("Most of these are avoidable with careful preprocessing; synonyms are the fundamental limit.");

// ---------- 10 KEY TERMS ----------
s=p.addSlide(); s.background=bgC;
kicker(s,"Key terms",0.7,0.55,BLUE);
title(s,"The vocabulary of keyword search",0.7,0.95,12,INK,32);
const terms=["lexical search","tokenization","stop words","stemming","inverted index","postings","term frequency (TF)","document frequency (df)","IDF","TF-IDF","BM25","term saturation","length normalization"];
let cxp=0.7, cyp=2.4;
terms.forEach(t=>{
  const w=0.28+t.length*0.115;
  if(cxp+w>12.6){cxp=0.7;cyp+=0.72;}
  chip(s,cxp,cyp,w,t); cxp+=w+0.25;
});
s.addText("Full definitions in the course GLOSSARY.",{x:0.7,y:5.9,w:8,h:0.4,fontFace:F,fontSize:14,italic:true,color:MUTED});
s.addNotes("These terms recur across the course; the glossary defines each simply.");

// ---------- 11 CLOSING (dark) ----------
s=p.addSlide(); s.background=bgT;
kicker(s,"Check your understanding",0.7,0.7,MINT);
title(s,"Test yourself, then move on",0.7,1.1,12,WHITE,34);
bullets(s,[
 "Why is it called an inverted index, and what problem does it solve?",
 "In the worked example, why does “is” contribute nothing?",
 "What two problems does BM25 fix, and which parameter controls each?"
],0.72,2.4,11.5,2.4,LIGHT);
s.addShape(p.ShapeType.roundRect,{x:0.7,y:5.5,w:6.4,h:0.9,fill:{color:WHITE},line:{type:"none"},rectRadius:0.12});
s.addText([{text:"Next  →  ",options:{bold:true,color:VIOLET}},{text:"Chapter 3: From Text to Vectors",options:{bold:true,color:INDIGO}}],
  {x:0.9,y:5.5,w:6,h:0.9,fontFace:F,fontSize:18,valign:"middle",margin:0});
s.addText("github.com/mdhabibi/llm-search-handbook",{x:7.4,y:5.75,w:5.4,h:0.5,fontFace:F,fontSize:14,color:MINT,align:"right"});
s.addNotes("Recap and hand-off to Chapter 3, where meaning-vectors solve the synonym problem.");

p.writeFile({fileName:"/sessions/inspiring-eloquent-brown/mnt/outputs/slides_build/Chapter-02-Keyword-Search.pptx"})
 .then(f=>console.log("WROTE",f));
