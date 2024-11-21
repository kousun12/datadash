import {javascript} from "npm:@codemirror/lang-javascript";
import {sql} from "npm:@codemirror/lang-sql";
import {EditorView, keymap} from "npm:@codemirror/view";
import {basicSetup} from "npm:codemirror";

export function Editor({
  value = "",
  style = "font-size: 14px;",
  lang = "javascript",
} = {}) {
  const parent = document.createElement("div");
  const editorStyle = `
  max-height: 400px;
  overflow-y: auto;
  ${style}
`;
  parent.style = editorStyle;
  parent.value = value;

  const langExt = lang === "sql" ? sql() : javascript();

  const save = () => {
    parent.value = editor.state.doc.toString();
  };

  const editor = new EditorView({
    parent,
    doc: value,
    extensions: [
      basicSetup,
      langExt,
      keymap.of([
        // {key: "Shift-Enter", preventDefault: true, run},
        // {key: "Mod-s", preventDefault: true, run}
      ])
    ]
  });

  parent.addEventListener("input", (event) => event.isTrusted && event.stopImmediatePropagation());

  return parent;
}