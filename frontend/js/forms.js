import {request, showError} from "./api.js";

const form = document.querySelector("form[data-kind]");
let readData;

if (form?.dataset.kind === "record") {
  const schemas = JSON.parse(document.querySelector("#schemas").textContent);
  const fields = document.querySelector("#fields");
  const raw = document.querySelector("#record-json");
  const rawLabel = document.querySelector("#json-label");
  const toggle = document.querySelector("#toggle-json");
  const type = form.elements.object_type_id;
  let jsonMode = false;
  let readers = [];

  function input(schema, value, required) {
    const label = document.createElement("label");
    const control = document.createElement(schema.enum || schema.type === "boolean" ? "select" : "input");
    label.textContent = schema.title || "Значение";
    if (required) label.append(" *");
    if (control.tagName === "SELECT") {
      control.add(new Option("Выберите значение", ""));
      for (const option of schema.enum || [true, false]) {
        control.add(new Option(typeof option === "boolean" ? option ? "Да" : "Нет" : String(option), JSON.stringify(option)));
      }
      control.value = value === undefined ? "" : JSON.stringify(value);
    } else {
      control.type = ["integer", "number"].includes(schema.type) ? "number" : "text";
      if (control.type === "number") control.step = schema.type === "integer" ? "1" : "any";
      if (schema.minimum !== undefined) control.min = schema.minimum;
      if (schema.maximum !== undefined) control.max = schema.maximum;
      if (schema.minLength !== undefined) control.minLength = schema.minLength;
      if (schema.maxLength !== undefined) control.maxLength = schema.maxLength;
      control.value = value ?? "";
    }
    control.required = required;
    label.append(control);
    if (schema.description) {
      const hint = document.createElement("small");
      hint.textContent = schema.description;
      label.append(hint);
    }
    return {label, read: () => control.value === "" ? undefined : control.tagName === "SELECT" ? JSON.parse(control.value) : control.type === "number" ? Number(control.value) : control.value};
  }

  function simple(schema) {
    return schema && ["string", "integer", "number", "boolean"].includes(schema.type)
      && !["$ref", "allOf", "anyOf", "oneOf", "if", "const"].some(key => key in schema);
  }

  function render(data) {
    const schema = schemas[type.value];
    const properties = schema.properties || {};
    readers = [];
    fields.replaceChildren();
    const supported = Object.keys(data).every(key => key in properties)
      && !["$ref", "allOf", "anyOf", "oneOf", "if", "patternProperties"].some(key => key in schema)
      && Object.values(properties).every(field => simple(field) || field.type === "array" && simple(field.items));
    jsonMode = !supported;
    fields.hidden = jsonMode;
    rawLabel.hidden = !jsonMode;
    toggle.hidden = !supported;
    toggle.textContent = "Редактировать JSON";
    raw.value = JSON.stringify(data, null, 2);
    if (!supported) return;
    for (const [key, property] of Object.entries(properties)) {
      const required = (schema.required || []).includes(key);
      const value = Object.hasOwn(data, key) ? data[key] : property.default;
      if (property.type === "array") {
        const group = document.createElement("fieldset");
        const legend = document.createElement("legend");
        legend.textContent = (property.title || key) + (required ? " *" : "");
        const rows = document.createElement("div");
        let entries = [];
        function add(value) {
          const field = input(property.items, value, true);
          const row = document.createElement("div");
          row.className = "array-row";
          const remove = document.createElement("button");
          remove.type = "button";
          remove.className = "secondary";
          remove.textContent = "Убрать";
          remove.onclick = () => { entries = entries.filter(entry => entry !== field); row.remove(); };
          entries.push(field);
          row.append(field.label, remove);
          rows.append(row);
        }
        const button = document.createElement("button");
        button.type = "button";
        button.className = "secondary";
        button.textContent = "Добавить значение";
        button.onclick = () => add(undefined);
        group.append(legend, rows, button);
        for (const item of value || []) add(item);
        fields.append(group);
        readers.push([key, () => entries.length || required || value !== undefined ? entries.map(entry => entry.read()) : undefined]);
      } else {
        const field = input({...property, title: property.title || key}, value, required);
        fields.append(field.label);
        readers.push([key, field.read]);
      }
    }
  }

  readData = () => jsonMode ? JSON.parse(raw.value) : Object.fromEntries(readers.map(([key, read]) => [key, read()]).filter(([, value]) => value !== undefined));
  toggle.onclick = () => {
    try {
      if (jsonMode) render(JSON.parse(raw.value));
      else {
        raw.value = JSON.stringify(readData(), null, 2);
        jsonMode = true;
        fields.hidden = true;
        for (const control of fields.querySelectorAll("input, select")) control.disabled = true;
        rawLabel.hidden = false;
        toggle.textContent = "Показать поля";
      }
    } catch (error) { showError(form, error); }
  };
  let previousType = type.value;
  type.onchange = () => {
    try {
      const data = readData();
      render(data);
      previousType = type.value;
    } catch (error) { type.value = previousType; showError(form, error); }
  };
  render(JSON.parse(document.querySelector("#record-data").textContent));
}

if (form) form.addEventListener("submit", async event => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  form.querySelector(".error").hidden = true;
  try {
    const name = form.elements.name.value;
    const isType = form.dataset.kind === "type";
    const payload = isType
      ? {name, parent_id: form.elements.parent_id.value || null, instance_schema: JSON.parse(form.elements.instance_schema.value)}
      : {name, object_type_id: form.elements.object_type_id.value, data: readData()};
    const base = `/api/v1/${isType ? "object-types" : "records"}`;
    const id = form.dataset.id;
    const result = await request(id ? `${base}/${id}` : base, id ? "PATCH" : "POST", payload);
    location.href = isType ? `/?object_type_id=${result.id}` : `/records/${result.id}`;
  } catch (error) { showError(form, error); }
  finally { button.disabled = false; }
});

for (const button of document.querySelectorAll("[data-delete]")) {
  button.onclick = async () => {
    if (!confirm("Удалить? Это действие нельзя отменить.")) return;
    button.disabled = true;
    try {
      await request(button.dataset.delete, "DELETE");
      location.href = button.dataset.redirect;
    } catch (error) { showError(button.closest(".panel"), error); }
    finally { button.disabled = false; }
  };
}
