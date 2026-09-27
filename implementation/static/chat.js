"use strict";
const $ = id => document.getElementById(id);
let conversationId = crypto.randomUUID();
let pending = false;

function notice(message) { $("notice").textContent = message; }
function inspect(data) { $("trace").textContent = JSON.stringify(data, null, 2); }
async function api(path, method = "GET", body) {
  const key = $("apiKey").value.trim();
  if (!key) throw new Error("Enter your configured API key first.");
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 65000);
  try {
    const response = await fetch(path, {method, signal: controller.signal,
      headers: {"X-API-Key": key, "Content-Type": "application/json"},
      body: body === undefined ? undefined : JSON.stringify(body)});
    const data = await response.json();
    inspect(data);
    if (!response.ok) {
      if (data.generation_status === "unavailable") return data;
      throw new Error(data.error || "Request failed");
    }
    return data;
  } finally { clearTimeout(timer); }
}
async function run(action) {
  if (pending) return;
  pending = true;
  document.querySelectorAll("button").forEach(b => b.disabled = true);
  try { await action(); } catch (e) { notice(e.name === "AbortError" ? "Request timed out; inspect memories before retrying." : e.message); }
  finally { pending = false; document.querySelectorAll("button").forEach(b => b.disabled = false); }
}
function message(who, text) {
  const node = document.createElement("div"); node.className = "message";
  node.textContent = who + ": " + text; $("messages").append(node); node.scrollIntoView({block:"nearest"});
}
function renderMemories(items) {
  $("memories").replaceChildren();
  if (!items.length) { $("memories").textContent = "No active memories."; return; }
  items.forEach(item => {
    const card = document.createElement("article"); card.className = "memory";
    const content = document.createElement("div"); content.textContent = item.content;
    const meta = document.createElement("p"); meta.className = "meta";
    meta.textContent = item.metadata.memory_type + " · v" + (item.metadata.version || 1)
      + " · expires " + (item.metadata.expires_at || "legacy: unset")
      + " · source " + (item.metadata.source || "legacy: unset");
    const edit = document.createElement("button"); edit.textContent = "Edit / correct";
    const editor = document.createElement("div");
    edit.onclick = () => {
      editor.replaceChildren();
      const input = document.createElement("textarea"); input.value = item.content;
      input.maxLength = 4000; input.setAttribute("aria-label", "Corrected memory");
      const hint = document.createElement("p"); hint.textContent = "Confirm to replace stored content and its vector. Expiration stays unchanged.";
      const save = document.createElement("button"); save.textContent = "Confirm correction";
      save.onclick = () => run(async () => {
        await api("/memory/" + encodeURIComponent(item.id), "PUT", {text:input.value, consent:true});
        await refresh(); notice("Correction saved; previous content is no longer active.");
      });
      const cancel = document.createElement("button"); cancel.textContent = "Cancel";
      cancel.onclick = () => editor.replaceChildren();
      editor.append(input, hint, save, cancel); input.focus();
    };
    const del = document.createElement("button"); del.textContent = "Delete";
    del.onclick = () => {
      editor.replaceChildren();
      const hint = document.createElement("p"); hint.textContent = "This permanently removes this memory record and vector. This cannot be undone.";
      const confirm = document.createElement("button"); confirm.textContent = "Confirm permanent deletion";
      confirm.onclick = () => run(async () => {
        await api("/memory/" + encodeURIComponent(item.id), "DELETE");
        await refresh(); notice("Deleted.");
      });
      const cancel = document.createElement("button"); cancel.textContent = "Cancel";
      cancel.onclick = () => editor.replaceChildren();
      editor.append(hint, confirm, cancel);
    };
    card.append(content, meta, edit, del, editor); $("memories").append(card);
  });
}
async function refresh() {
  const data = await api("/memories");
  renderMemories(data.ids.map((id,i) => ({id,content:data.documents[i],metadata:data.metadatas[i]})));
}
$("send").onclick = () => run(async () => {
  const text = $("messageInput").value.trim(); if (!text) return;
  message("You", text);
  const data = await api("/chat", "POST", {message:text,remember:$("remember").checked,conversation_id:conversationId});
  message("RecallGuard", data.response || "Generation is unavailable. Inspect memory decisions below.");
  $("messageInput").value = "";
  await refresh(); inspect(data);
  notice(data.generation_status === "unavailable" ? "Generation is unavailable. Memory write outcomes are shown in the inspector." : "Request completed.");
});
$("search").onclick = () => run(async () => {
  const data = await api("/retrieve", "POST", {query:$("query").value,top_k:5}); renderMemories(data); notice("Search completed.");
});
$("refresh").onclick = $("connect").onclick = () => run(refresh);
$("reflect").onclick = () => run(async () => {const data=await api("/reflection","POST",{});await refresh();inspect(data);notice("Maintenance completed.");});
$("newSession").onclick = () => {conversationId=crypto.randomUUID();$("messages").replaceChildren();notice("New conversation. Saved memories remain until deleted or expired.");};
fetch("/ready").then(r=>{$("status").textContent=r.ok?"Storage ready":"Storage unavailable";}).catch(()=>{$("status").textContent="Service unavailable";});
